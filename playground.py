
import numpy as np
from new_sql import create_connection,execute_query,fetch_id_and_encoding,get_result_per_ids
from  work_with_model import encode_single_doc


doc_encoding_iter = None


# def update_encoding_column( rows ):
#     """
#     here take input of list of tuples each single tuple consistes of fileid,filename
#     """
#     conn = create_connection()

#     query = "UPDATE metadata SET encoding = ? WHERE file_id = ?"

#     for row in rows:
#         encoding = encode_single_doc(row[1]) ## here i am using only file name for vectorisation
#         params = (encoding ,row[0])
#         execute_query(conn, query, params)

#     conn.commit()
#     conn.close()



def cosine_sim(array1,array2):
    # calculate dot product
    dot_product = np.dot(array1, array2)

    # calculate magnitudes
    magnitude1 = np.linalg.norm(array1)
    magnitude2 = np.linalg.norm(array2)

    # calculate cosine similarity
    return dot_product / (magnitude1 * magnitude2)

   


def similarity_score_cal(query):
    """
    A function that fetches the top k most similar items to a given input
    using a pre-trained model.
    """
    global doc_encoding_iter
    
    query_embedding = encode_single_doc(text = query)

    if doc_encoding_iter is None:
        doc_encoding_iter = fetch_id_and_encoding()
   
    for doc in doc_encoding_iter:
        file_id = doc[0]
        doc_embedding = doc[1]
        similarity_score = cosine_sim(query_embedding, doc_embedding)
        yield (file_id,similarity_score)


def get_top_k_docs(query, k=7):
    similarity_scores = similarity_score_cal(query)
    sorted_tuples = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    for i in range(0,len(sorted_tuples),k):
        yield [row[0] for row in sorted_tuples[i:i+k]]


if __name__ == "__main__":
 
#     # obj = fetch_id_and_encoding()
#     # lis = list(obj)
#     # print(len(lis[0][1]))
    q = "photos"
    print("query :" ,q)
    obj =  get_top_k_docs(q,k=10)
    res = list(next(obj))
    
    for file in get_result_per_ids(res):
        print(file)
        print()
    
    




    


    