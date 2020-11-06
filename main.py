import os
import database as db
import file_manager as fm
import tokenization as tok
import vector_space as vs


def phrase_query(query):
    dictionary = db.load_terms()
    result = tok.merge(query, dictionary)
    result2 = []
    if result is None:
        return []
    for doc_id in result:
        result2.append((doc_id, 1))
    return result2


def free_text_query(query):
    query_vector = vs.create_query_vector(query)
    result = []
    for i in range(25):
        doc_vector = db.load_vector(i)
        rank = vs.sim(query_vector, doc_vector)
        if rank != 0:
            result.append((i, rank))
    result.sort(key=lambda x: x[1], reverse=True)
    return result


def print_result(result):
    if result is not None:
        docs_names = []
        for doc_id, rank in result:
            doc_name = db.load_filename(doc_id)
            docs_names.append((doc_name, rank))
        while True:
            os.system('cls')
            print("\n")
            print("    Result is :\n")
            for i, (doc_name, rank) in enumerate(docs_names):
                print("        document "+str(doc_name)+" with rank "+str(round(rank, 4))+" (to open it enter ("+str(i+1)+")).")
            choice = input("\n    Or Enter (q) to go back.\n\n    ")
            if choice == 'q':
                break
            if 1 <= int(choice) <= len(result):
                open_flag = fm.open_doc(docs_names[int(choice)-1][0], "Collection/")
                if open_flag:
                    os.system('cls')
                    print("\n")
                    input("    file opened\n\n    Enter any key to continue. ")
                else:
                    os.system('cls')
                    print("\n")
                    input("    Cannot open this document right now.\n\n    Enter any key to continue. ")
            else:
                os.system('cls')
                print("\n")
                input("    PLEASE ENTER YOUR CHOICE CORRECTLY\n\n    Enter any key to continue. ")
    else:
        os.system('cls')
        print("\n")
        input("    No result founded.\n\n    Enter any key to continue. ")


if __name__ == '__main__':
    db.connect_to_database("IR_database")
    while True:
        os.system('cls')
        print("\n")
        print("    Hello, welcome to our IR system\n")
        choice = input("    Please choose your query type \n\n"
                       "    Enter (1) for phrase query\n"
                       "    Enter (2) for free text query\n"
                       "    Enter (q) to close the program\n\n    "
                       )
        if choice == '1':
            os.system('cls')
            print("\n")
            query = input("    Enter your query: ")
            result = phrase_query(query)
            print_result(result)
        elif choice == '2':
            os.system('cls')
            print("\n")
            query = input("    Enter your query: ")
            result = free_text_query(query)
            print_result(result)
        elif choice == 'q':
            break
        else:
            os.system('cls')
            print("\n")
            input("    PLEASE ENTER YOUR CHOICE CORRECTLY\n\n    Enter any key to continue. ")
    os.system('cls')
    print("\n")
    input("    Thanks for using our program, we hope you enjoy it.    ")
