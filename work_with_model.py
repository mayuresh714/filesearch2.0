import numpy as np
import pickle
import os
import torch
# from transformers import AutoTokenizer, AutoModelForSequenceClassification
import transformers
from functools import lru_cache



def save_pickle_obj(obj,path):
    with open(path, 'wb') as f:
        pickle.dump(obj, f)

@lru_cache
def load_pickle_obj(path):
    with open( path, 'rb') as f:
        return  pickle.load(f)


class transformer_ops:

    def __init__(self,name):
        self.__parent_dir       = os.path.dirname(os.path.abspath(__file__))
        self.__is_model_present = False
        self.__model_name       = name
        self.__model_path       = None
        self.__tokenizer_path   = None
        self.__loaded_model     = None
        self.__loaded_tokenizer = None
        self.transformers_module = transformers
        self.setter()

    def access_model_for_tesing(self):
        if not self.__loaded_model or not self.__loaded_tokenizer:
            self.load_model_pickle()
        return (self.__loaded_tokenizer,self.__loaded_model)
    
    def set_models_rare_case(self,tokenizer,model):
        self.__loaded_model = model
        self.__loaded_tokenizer= tokenizer


    
    def setter(self):
        self.__model_path     =  os.path.join(self.__parent_dir,"models")
        self.__tokenizer_path =  os.path.join(self.__parent_dir,"models")
        
        self.__model_name = self.__model_name.replace("/","@")
            
        model_folder = os.path.join(self.__model_path,self.__model_name)

        if not os.path.exists(model_folder):
            os.makedirs(model_folder)
        else:
            if not os.path.exists(os.path.join(model_folder,"model.pkl")):
                print("Directory already exists but model not downloaded")
            else:
                print("Directory already exists and model also downloaded")
                self.__is_model_present = True

        self.__model_path     =  os.path.join(model_folder,"model.pkl")
        self.__tokenizer_path =  os.path.join(model_folder,"tokenizer.pkl")
        # print(__model_path, "\n",__tokenizer_path)

    def get_data_for_testing_purpose(self):
        print(self.__is_model_present)
        print(self.__model_name)
        print(self.__model_path)
        print(self.__tokenizer_path)

    #Mean Pooling - Take average of all tokens
    def mean_pooling(self,model_output, attention_mask):
        token_embeddings = model_output.last_hidden_state
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    # #Encode text
    # def encode(texts):
    #     # Tokenize sentences
    #     encoded_input = tokenizer(texts, padding=True, truncation=True, return_tensors='pt')

    #     # Compute token embeddings
    #     with torch.no_grad():
    #         model_output = model(**encoded_input, return_dict=True)

    #     # Perform pooling
    #     embeddings = mean_pooling(model_output, encoded_input['attention_mask'])

    #     # Normalize embeddings
    #     embeddings = F.normalize(embeddings, p=2, dim=1)
        
    #     return embeddings

    #Encode text
    def encode_from_official_doc_by_HF(self,texts,do_normalize = False):
       
        # Tokenize sentences
        encoded_input = self.__loaded_tokenizer(texts, padding=True, truncation=True, return_tensors='pt')

        # Compute token embeddings
        with torch.no_grad():
            model_output = self.__loaded_model(**encoded_input, return_dict=True)

        # Perform pooling
        embeddings = self.mean_pooling(model_output, encoded_input['attention_mask'])
        
        # Normalize embeddings
        if do_normalize:
            embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
        
        return embeddings[0]
    

    def download_and_save_model_pickle(self,model_name,tokenizer_class,model_class):
        if self.__is_model_present:
            print(f"{model_name} already exists no need to download again ...")
        else:
            tokenizer =   getattr(transformers, tokenizer_class).from_pretrained(model_name) 
            model     =   getattr(transformers,model_class).from_pretrained(model_name)
            # print(__model_path)
            save_pickle_obj(obj = tokenizer,path= self.__tokenizer_path)
            save_pickle_obj(obj = model,path= self.__model_path)





    def load_model_pickle(self):
        if self.__loaded_model is None:
            self.__loaded_model = load_pickle_obj(self.__model_path)
        if self.__loaded_tokenizer is None:
            self.__loaded_tokenizer = load_pickle_obj(self.__tokenizer_path)
        


    def encode_single_doc(self,text):
        self.load_model_pickle()
        # Tokenize the text and convert to input format for the model
        input_ids = self.__loaded_tokenizer(text, return_tensors='pt').input_ids
        
        # Generate the vector representation using the model
        with torch.no_grad():
            outputs = self.__loaded_model(input_ids)
            embeddings = outputs.pooler_output
            
        # Return the vector representation as a numpy array
        # print(len(embeddings.numpy()[0]))
        return embeddings.numpy()[0]








# ////////////////*****************************************************************************************/////////////////////////

# def download_and_save_model_bin(model_name):
#     # Define the model name and path
   
#     save_path = "models/{}".format(model_name)

#     # Create the directory to store the tokenizer and model
#     if not os.path.exists(save_path):
#         os.makedirs(save_path)
#         os.makedirs("{}/model".format(save_path))
#         os.makedirs("{}/tokenizer".format(save_path))

#     # Download the tokenizer and model
#     tokenizer = AutoTokenizer.from_pretrained(model_name)
#     model = AutoModelForSequenceClassification.from_pretrained(model_name)

#     # Save the tokenizer and model to their respective directories
#     tokenizer.save_pretrained("{}/tokenizer".format(save_path))
#     model.save_pretrained("{}/model".format(save_path))


# @lru_cache
# def load_model_bin(model_name = "sentence-transformers/paraphrase-MiniLM-L3-v2"):
#     load_path = "models/{}".format(model_name)

#     # Load the tokenizer and model
#     loaded_tokenizer = AutoTokenizer.from_pretrained("{}/tokenizer".format(load_path))
#     loaded_model = AutoModelForSequenceClassification.from_pretrained("{}/model".format(load_path))
#     print(loaded_model is None)
#     return (loaded_model,loaded_tokenizer)



# def encode_model_bin(text):
#     # Tokenize the text and convert to input format for the model
#     __loaded_model,__loaded_tokenizer = load_model_bin()
#     input_ids = __loaded_tokenizer(text, return_tensors='pt').input_ids
    
#     # Generate the vector representation using the model
#     with torch.no_grad():
#         outputs = __loaded_model(input_ids)
#         embeddings = outputs.pooler_output
        
#     # Return the vector representation as a numpy array
#     # print(len(embeddings.numpy()[0]))
#     return embeddings.numpy()[0]

# //////////////////*****************//////////////////////////////////////****************************************************












if __name__ == "__main__":
    print("ok")
    # vec = encode_single_doc("the cat is strong")
    # print(len(vec))
