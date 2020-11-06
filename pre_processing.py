import tokenization
import indexing
import database as db


def run_once():
    db.drop_database("IR_database")
    collection_key_words = tokenization.tokenizier()
    indexing.create_incidence_matrix(collection_key_words)


run_once()
