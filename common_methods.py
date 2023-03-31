import os

## global variables
parent_dir = os.path.dirname( os.path.abspath(__file__))

def make_file_content(row):
    """ the row has following metadata about file : (as per order)
    row is a tuple and it will look like this
    (name, type, size,  created_time,accessed_time, modified_time, file_path)
    we will use this info to develop a paragraph describing about a file 
    we are doing this becoz we want to encode that content into vectorspace

    Generate file content for the given row of metadata.
    """
    name, file_type, size, created_time, accessed_time, modified_time, file_path = row
    
    # Generate a human-readable size string
    if size < 1024:
        size_str = str(size) + " bytes"
    elif size < 1048576:
        size_str = str(round(size / 1024, 2)) + " KB"
    else:
        size_str = str(round(size / 1048576, 2)) + " MB"
    
    
    # Generate the file content string
    content = f"This is a {file_type} file named {name} with a size of {size_str}. " \
              f"It was created on {created_time}, last accessed on {accessed_time}, " \
              f"and last modified on {modified_time}. The file is located at {file_path}."
    
    return content


if __name__ == "__main__":
    # row = ("mk.py","pdf",230,"Tue Mar  7 10:01:25 2023","Tue Mar  7 10:01:25 2023","Wed Oct 21 22:55:37 2020",r"C:\Users\shree\OneDrive\Documents\21142_DEL_Comparator_expt.no. 05.pdf")
    # print(make_file_content(row))
    print(parent_dir)