import pymongo
import os

def connect_to_database(database_name):
    global my_client
    global my_db
    my_client = pymongo.MongoClient("mongodb://localhost:27017/")
    my_db = my_client[database_name]
    my_client.close()


def drop_database(database_name):
    my_client = pymongo.MongoClient("mongodb://localhost:27017/")
    my_client.drop_database(database_name)


def save_posting_list(_id, posting_list):
    my_dict = {"id": _id, "posting_list": posting_list}
    my_col = my_db["posting_list"]
    my_col.insert_one(my_dict)


def save_term(_id, term, df):
    my_dict = {"id": _id, "term": term, "df": df}
    my_col = my_db["terms"]
    my_col.insert_one(my_dict)


def save_vector(doc_id, vector):
    my_dict = {"doc_id": doc_id, "vector": vector}
    my_col = my_db["vectors"]
    my_col.insert_one(my_dict)


def save_filename(doc_id, filename):
    my_dict = {"id": doc_id, "filename": filename}
    my_col = my_db["files"]
    my_col.insert_one(my_dict)


def load_posting_list(_id):
    my_col = my_db["posting_list"]
    result = my_col.find({"id": _id})
    if result.count() == 0:
        return None
    dic = result.__getitem__(0)
    return dic['posting_list']


def load_terms():
    my_col = my_db["terms"]
    result = my_col.find()
    if result.count() == 0:
        return None
    dics = []
    for i in range(result.count()):
        dics.append(result.__getitem__(i))
    terms = []
    for dic in dics:
        terms.append((dic['term'], dic['id']))
    return terms


def load_vector(doc_id):
    my_col = my_db["vectors"]
    result = my_col.find({"doc_id": doc_id})
    if result.count() == 0:
        return None
    dic = result.__getitem__(0)
    return dic['vector']


def load_filename(doc_id):
    my_col = my_db["files"]
    result = my_col.find({"id": doc_id})
    if result.count() == 0:
        return None
    dic = result.__getitem__(0)
    return dic['filename']


def load_df(term_id):
    my_col = my_db["terms"]
    result = my_col.find({"id": term_id})
    if result.count() == 0:
        return None
    dic = result.__getitem__(0)
    return dic['df']


def get_number_of_documents():
    files = os.listdir("Collection/")
    return len(files)



