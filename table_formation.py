# from playground import get_top_k_docs
from file_metadata import  get_all_metadata
from new_sql import create_table,insert_many_data,select_null_encoding,create_connection,execute_query
from work_with_model import encode_single_doc
import sqlite3
import json


# q = "final year documents"
# get_top_k_docs(q,k = 5)

 

def dump(vector):
    return json.dumps( vector.tolist())



def update_encoding_column( rows ):
    """
    here take input of list of tuples each single tuple consistes of fileid,filename
    """
    conn = create_connection()

    query = "UPDATE metadata SET encoding = ? WHERE file_id = ?"

    for row in rows:
        encoding = encode_single_doc(row[1]) ## here i am using only file name for vectorisation
        params = ( dump(encoding) ,row[0])
        execute_query(conn, query, params)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    path = r"C:\Users\shree\Downloads"
    lis =  get_all_metadata(folder_path=path)
    create_table()
    insert_many_data(lis)
    rows = select_null_encoding()
    update_encoding_column(rows=rows)

