import math
import database as db

N = db.get_number_of_documents()


def sort_tuple(l):
    l.sort(key=lambda x: x[2])
    l.sort(key=lambda x: x[1])
    l.sort(key=lambda x: x[0])
    return l


def indexing(sorted_list):
    main_list = []
    help_list = []
    i = 0
    while True:
        if i > len(sorted_list)-1:
            main_list.append((term, help_list))
            break
        if i != 0:
            if sorted_list[i][0] != sorted_list[i - 1][0]:
                main_list.append((term, help_list))
                help_list = []
        term = sorted_list[i][0]
        while True:  # same term
            if i > len(sorted_list) - 1:
                break
            if sorted_list[i][0] != term:
                break
            doc_id = sorted_list[i][1]
            positions_list = []
            positions_list.append(sorted_list[i][2])
            i += 1
            while True:  # same doc
                if i > len(sorted_list) - 1:
                    help_list.append((doc_id, positions_list))
                    break
                if sorted_list[i][1] == doc_id and sorted_list[i][0] == term:
                    positions_list.append(sorted_list[i][2])
                    i += 1
                else:
                    help_list.append((doc_id, positions_list))
                    break
    return main_list


def find_df(main_list):
    document_frequency = []

    for tub in main_list:
        document_frequency.append((tub[0], len(tub[1])))

    return document_frequency


def find_tf(main_list):
    term_frequency = []

    for tub in main_list:
        all_tf = []

        for i in range(N):
            all_tf.append(0)

        for doc_tub in tub[1]:
            all_tf[doc_tub[0]] = len(doc_tub[1])

        term_frequency.append((tub[0], all_tf))

    return term_frequency


def idf(dfs):
    inverse_term_frequency = []

    for df in dfs:
        idf = math.log10(N/df[1])
        all_idf = []

        for i in range(N):
            all_idf.append(idf)

        inverse_term_frequency.append((df[0], all_idf))

    return inverse_term_frequency


def tf_idf(term_frequencies, inverse_term_frequencies):
    all_tf_idf_for_one_tuple = []
    tf_idf_for_all_tuples = []
    tf_idf_for_one_document = []
    final_tf_idf = []

    for tf_tub, idf_tub in zip(term_frequencies, inverse_term_frequencies):
        for i in range(N):
            all_tf_idf_for_one_tuple.append(tf_tub[1][i]*idf_tub[1][i])

        tf_idf_for_all_tuples.append(all_tf_idf_for_one_tuple)
        all_tf_idf_for_one_tuple = []

    for i in range(N):
        for j in range(len(tf_idf_for_all_tuples)):
            tf_idf_for_one_document.append(tf_idf_for_all_tuples[j][i])

        final_tf_idf.append((i, tf_idf_for_one_document))
        tf_idf_for_one_document = []

    return final_tf_idf


def get_tf_idf_matrix(collections_key_words):
    sorted_list = sort_tuple(collections_key_words)
    main_list = indexing(sorted_list)
    tfs = find_tf(main_list)
    dfs = find_df(main_list)
    idfs = idf(dfs)
    tf_idf_matrix = tf_idf(tfs, idfs)
    return tf_idf_matrix, main_list, dfs


def create_incidence_matrix(collections_key_words):
    tf_idf_matrix, main_list, dfs = get_tf_idf_matrix(collections_key_words)
    db.connect_to_database("IR_database")
    for doc_id, vector in tf_idf_matrix:
        db.save_vector(doc_id, vector)
    for i, tup in enumerate(main_list):
        db.save_term(i, tup[0], dfs[i][1])
        db.save_posting_list(i, tup[1])
