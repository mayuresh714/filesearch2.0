import sqlite3
import os
import json
from common_methods import make_file_content,parent_dir

class sql_ops:
    def __init__(self,db_name = "filesearch.db"):
        self.__parent_dir = parent_dir
        self.__db_name = db_name
        self.__db_path = os.path.join(parent_dir,"database" ,db_name)

 

    def create_connection(self):
        try:
            conn = sqlite3.connect(self.__db_path)
            return conn
        except sqlite3.Error as e:
            print(e)
        return None

    def execute_query(self,conn, query, params=()):
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            cursor.close()
            return rows
        except sqlite3.Error as e:
            print(e)
        return None

    def execute_many(self,conn, query, list_of_params):
        try:
            cursor = conn.cursor()
            cursor.executemany(query, list_of_params)
            cursor.close()
        except sqlite3.Error as e:
            print(e)

    def create_table(self):
        conn = self.create_connection()
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
        self.execute_query(conn, query)
        conn.commit()
        conn.close()

    def insert_data(self,file_name, file_path, created_date, modified_date, size):
        conn = self.create_connection()
        query = "INSERT INTO metadata ( file_name,file_type,file_size,creation_date,accessed_date,modification_Date,file_location ) VALUES (?,?,?,?,?,?,?)" 

        params = (file_name, file_path, created_date, modified_date, size)
        self.execute_query(conn, query, params)
        conn.commit()
        conn.close()

    def insert_many_data(self,list_of_data ):
        conn = self.create_connection()
        query = "INSERT INTO metadata ( file_name,file_type,file_size,creation_date,accessed_date,modification_Date,file_location ) VALUES (?,?,?,?,?,?,?)" 

        self.execute_many(conn, query, list_of_data)
        conn.commit()
        conn.close()


    def add_single_encoding(self,file_id, encoding):
        conn = self.create_connection()
        query = "UPDATE metadata SET encoding = ? WHERE file_id = ?"

        params = (encoding, file_id)
        self.execute_query(conn, query, params)
        conn.commit()
        conn.close()


    def load(self,obj):
        return json.loads(obj)


    def fetch_id_and_encoding(self):
        try:
            conn = self.create_connection()
            cursor = conn.cursor()

            query = "select file_id,encoding from metadata"
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()

            # Convert the encoding column to numpy arrays
            lis = []
            for row in rows:
                lis.append((row[0] , self.load(row[-1]) ))
                # print(len(lis[-1][-1]))
            return lis
    
        except sqlite3.Error as e:
            print(e)
        return None



    def get_result_per_ids(self,id_list):
        conn = self.create_connection()
        query = "SELECT file_name,file_type,file_location,file_size,creation_date,modification_date FROM metadata WHERE file_id = ?"

        for id in id_list:
            row = self.execute_query( conn, query , (str(id),) )
            yield row[0]

        conn.close()

    def dump(self,vector):
        return json.dumps( vector.tolist())

    def select_null_encoding(self):
        conn = self.create_connection()
        query = "SELECT file_id, file_name,file_type,file_size,creation_date,accessed_date,modification_date,file_location FROM metadata WHERE encoding IS NULL"

        rows = self.execute_query(conn, query)
        conn.close()

        return rows

    def update_encoding_column( self,rows,encoding_func):
        """
        here take input of list of tuples each single tuple consistes of all filemetadata
        """
        conn = self.create_connection()

        query = "UPDATE metadata SET encoding = ? WHERE file_id = ?"

        for row in rows:
            content = make_file_content(row[1:])
            encoding = encoding_func( content ) ## here i am using only file name for vectorisation
            params = ( self.dump(encoding) ,row[0])
            self.execute_query(conn, query, params)

        conn.commit()
        conn.close()

# if __name__ == "__main__":
#     rows = fetch_id_and_encoding()
#     print(list(rows)[:2])

    