import sqlite3
import numpy as np
import os
 
import json

__file_path = os.path.abspath(__file__)
__parent_dir = os.path.dirname(__file_path)
__db_name = "filesearch.db"
__db_path = os.path.join(__parent_dir, __db_name)



def create_connection():
    try:
        conn = sqlite3.connect(__db_path)
        return conn
    except sqlite3.Error as e:
        print(e)
    return None

def execute_query(conn, query, params=()):
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except sqlite3.Error as e:
        print(e)
    return None

def execute_many(conn, query, list_of_params):
    try:
        cursor = conn.cursor()
        cursor.executemany(query, list_of_params)
        cursor.close()
    except sqlite3.Error as e:
        print(e)

def create_table():
    conn = create_connection()
    query ='''
      CREATE TABLE  if not exists metadata (
          file_id integer primary key autoincrement,
          file_name text,
          file_type text,
          file_size integer,
          creation_date text, 
          accessed_date text,
          modification_date text,
          file_location text,
          keywords text default "not yet",
          encoding text default null
      )
    '''
    execute_query(conn, query)
    conn.commit()
    conn.close()

def insert_data(file_name, file_path, created_date, modified_date, size):
    conn = create_connection()
    query = "INSERT INTO metadata ( file_name,file_type,file_size,creation_date,accessed_date,modification_Date,file_location ) VALUES (?,?,?,?,?,?,?)" 

    params = (file_name, file_path, created_date, modified_date, size)
    execute_query(conn, query, params)
    conn.commit()
    conn.close()

def insert_many_data(list_of_data ):
    conn = create_connection()
    query = "INSERT INTO metadata ( file_name,file_type,file_size,creation_date,accessed_date,modification_Date,file_location ) VALUES (?,?,?,?,?,?,?)" 

    execute_many(conn, query, list_of_data)
    conn.commit()
    conn.close()


def add_single_encoding(file_id, encoding):
    conn = create_connection()
    query = "UPDATE metadata SET encoding = ? WHERE file_id = ?"

    params = (encoding, file_id)
    execute_query(conn, query, params)
    conn.commit()
    conn.close()


def select_null_encoding():
    conn = create_connection()
    query = "SELECT file_id,file_name FROM metadata WHERE encoding IS NULL"

    rows = execute_query(conn, query)
    conn.close()

    return rows


def load(obj):
    return json.loads(obj)


def fetch_id_and_encoding():
    try:
        conn = create_connection()
        cursor = conn.cursor()

        query = "select file_id,encoding from metadata"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()

        # Convert the encoding column to numpy arrays
        lis = []
        for row in rows:
            lis.append((row[0] , load(row[-1]) ))
            # print(len(lis[-1][-1]))
        return lis
 
    except sqlite3.Error as e:
        print(e)
    return None



def get_result_per_ids(id_list):
    conn = create_connection()
    query = "SELECT file_name,file_type,file_location,file_size,creation_date,modification_date FROM metadata WHERE file_id = ?"

    for id in id_list:
        row = execute_query( conn, query , (str(id),) )
        yield row[0]

    conn.close()

if __name__ == "__main__":
    rows = fetch_id_and_encoding()
    print(list(rows)[:2])

    