
from file_metadata import  get_all_metadata
from new_sql import sql_ops
from work_with_model import transformer_ops
import json


 

model = transformer_ops("GPT_125M")
model.setter()
dbops = sql_ops("filesearch.db")

def dump(vector):
    return json.dumps( vector.tolist())



def update_encoding_column( rows,db_obj ,model):
    """
    here take input of list of tuples each single tuple consistes of fileid,filename
    """
    conn = db_obj.create_connection()

    query = "UPDATE metadata SET encoding = ? WHERE file_id = ?"

    for row in rows:
        encoding = model.encode_single_doc(row[1]) ## here i am using only file name for vectorisation
        params = ( dump(encoding) ,row[0])
        db_obj.execute_query(conn, query, params)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    path = r"C:\Users\shree\OneDrive\documents"
    lis =  get_all_metadata(folder_path=path)
    create_table()
    insert_many_data(lis)
    # rows = select_null_encoding()
    # update_encoding_column(rows=rows)

