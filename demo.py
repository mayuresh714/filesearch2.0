
from file_metadata import  get_all_metadata
from new_sql import sql_ops
from work_with_model import transformer_ops
from playground import search_ops ,jaccard_sim,cosine_sim


 

model_obj = transformer_ops("GPT_125M")
db_obj = sql_ops("filesearch2.db")
search_obj = search_ops(k = 10 )


path = r"C:\Users\shree\Downloads"


lis =  get_all_metadata(folder_path=path)
db_obj.create_table()
db_obj.insert_many_data(lis)
rows = db_obj.select_null_encoding()
db_obj.update_encoding_column(rows=rows,encoding_func= model_obj.encode_single_doc)


stop = 1
while bool(stop):
    query = input("enter query: ")
    print("query :" ,query)
    obj =  search_obj.get_top_k_docs(query,db_obj=db_obj,model_obj= model_obj,k=10,similarity_func= cosine_sim)
    res = list(obj)
    for file in db_obj.get_result_per_ids(res[0]):
        print(file)
        print()
    print("/*"*50,"\n")
    stop = input("should i stop?press enter to stop/1 to continue")




