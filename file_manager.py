import os
import database as db


def open_doc(doc_name, path):
    all_files = os.listdir(path)
    if doc_name in all_files:
        os.system("notepad.exe "+path+doc_name)
        return True
    else:
        return False


def get_collection_names(path):
    files = os.listdir(path)
    files_without_extension = [item.split('.')[0] for item in files]
    return files_without_extension
