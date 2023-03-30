
from file_metadata import  get_all_metadata
from new_sql import sql_ops
from work_with_model import transformer_ops
from playground import search_ops ,jaccard_sim,cosine_sim
from  transformers import AutoModel,AutoTokenizer
 
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/multi-qa-MiniLM-L6-cos-v1")
model = AutoModel.from_pretrained("sentence-transformers/multi-qa-MiniLM-L6-cos-v1")


 

model_obj = transformer_ops("sentence-transformers@multi-qa-MiniLM-L6-cos-v1")
model_obj.set_models_rare_case(tokenizer=tokenizer,model=model)
db_obj = sql_ops("filesearch3.db")
search_obj = search_ops(k = 10 )



def index( path = r"C:\Users\shree\Downloads"):
    lis =  get_all_metadata(folder_path=path)
    db_obj.create_table()
    db_obj.insert_many_data(lis)
    rows = db_obj.select_null_encoding()
    db_obj.update_encoding_column(rows=rows,encoding_func= model_obj.encode_from_official_doc_by_HF)

def run_demo():
    
    # while bool(stop):
    query = input("enter query: ")
    print("query :" ,query)
    obj =  search_obj.get_top_k_docs(query,
                                     db_obj=db_obj,
                                     k=10,
                                     similarity_func= jaccard_sim,
                                     encoding_func=model_obj.encode_from_official_doc_by_HF)
    res = list(obj)
    for file in db_obj.get_result_per_ids(res[0]):
        print(file)
        print()
    print("/*"*50,"\n")
    # stop = input("should i stop?press enter to stop/1 to continue")


def menu_driven_test_purpose():
    stop = 1
    while bool(stop):
        inp = input("enter your choice\n1.index\n2.run demo\n")
        if inp == "1":
            path = input("please proveide folder path you want to index: \n")
            index(path=path)
        elif inp == "2":
            run_demo()
        else:
            print("please enter correct choice")
        stop = input("should i stop?press enter to stop/1 to continue")

if __name__ == "__main__":
    menu_driven_test_purpose()
