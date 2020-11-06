import re
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from functools import reduce
import database as db
import file_manager as fm


stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
              "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself",
              "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these",
              "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do",
              "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while",
              "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before",
              "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again",
              "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each",
              "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than",
              "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]


def get_document(path, filename, doc_id, t):
    db.connect_to_database("IR_database")
    db.save_filename(doc_id, filename+".txt")
    global stop_words
    file = open(path+filename+".txt", t)
    counter = 0
    document = []
    for line in file:
        field = re.findall(r"\w+", line)
        for word in field:
            counter += 1
            word = word.lower()
            if word not in stop_words:
                key_word = (word, doc_id, counter)
                document.append(key_word)
    return document


def normalization(word):
    lemmatizer = WordNetLemmatizer()
    ps = PorterStemmer()

    term = lemmatizer.lemmatize(word)
    term = ps.stem(term)
    return term


def tokenizier():
    path = "Collection/"
    # collection = ["A Dark Brown Dog" , "A Pair of Silk Stockings" , "About Love","An Angel in Disguise",
    # "An Occurrence at Owl Creek Bridge","Araby","Army",
    # "Cousin Tribulation's Story","Desiree's Baby","Ex Oblivione","Hearts And Hands","How the Camel Got His Hump",
    # "Lost Hearts","On The Day of the Crucifixion",
    # "Regret","The Brave Tin Soldier","The Cactus","The Cat","The Gift of the Magi","The Haunted Mind",
    # "The Luck of Roaring Camp","The Monkey's Paw","The Skylight Room","The Story of An Hour",
    # "The Tale of Peter Rabbit"]
    collection = fm.get_collection_names(path)
    collection_key_words = []
    for index, document in enumerate(collection):
        key_words_in_one_document = get_document(path, document, index, "r")
        #  normalized_key_words = []
        for word_info in key_words_in_one_document:
            word = normalization(word_info[0])
            collection_key_words.append((word, word_info[1], word_info[2]))
    return collection_key_words


def pre_processed_query(query):
    post_query = []
    counter = 0
    field = re.findall(r"\w+", query)
    for word in field:
        counter += 1
        word = word.lower()
        global stop_words
        if word not in stop_words:
            word = normalization(word)
            post_query.append((word, counter))
    return post_query


def find_term(word, dictionary):
    for item in dictionary:
        if item[0] == word:
            return item[1]


def get_id(post_query, dictionary):
    term_position_id = []
    for item in post_query:
        _id = find_term(item[0], dictionary)
        if _id is None:
            return -1
        position = item[1]
        term_position_id.append((position, _id))
    return term_position_id


def find_common(all_doc):
    res = list(reduce(lambda i, j: i & j, (set(x) for x in all_doc)))
    return res


def positional_intersect(pl1, pl2, d):
    answer = []
    for x, y in zip(range(len(pl1)), range(len(pl2))):
        #  tuple of first->last doc
        tuple1 = pl1[x]
        tuple2 = pl2[y]
        if tuple1[0] == tuple2[0]:
            intersection_list = []
            positions1 = tuple1[1]
            positions2 = tuple2[1]
            i = 0
            j = 0
            while i < len(positions1) and j < len(positions2):
                if positions2[j] - positions1[i] == d:
                    intersection_list.append(positions2[j])
                    i += 1
                    j += 1
                elif positions1[i] > positions2[j]:
                    j += 1
                else:
                    i += 1
            answer.append((tuple1[0], intersection_list))
    return answer


def merge(query, dictionary):
    query_terms = pre_processed_query(query)
    term_position_id = get_id(query_terms, dictionary)
    if term_position_id == -1:
        return None
    query_postings = []
    for word in term_position_id:
        posting_list = db.load_posting_list(word[1])
        query_postings.append((word[0], posting_list))
    differences = []
    for i in range(len(query_postings) - 1):
        diff = query_postings[i + 1][0] - query_postings[i][0]
        differences.append(diff)
    all_doc = []
    for item in query_postings:
        term_doc = []
        for tup in item[1]:
            term_doc.append(tup[0])
        all_doc.append(term_doc)
    common_docs = find_common(all_doc)
    common_postings = []
    for item in query_postings:
        term = []
        for tup in item[1]:
            if tup[0] in common_docs:
                term.append((tup[0], tup[1]))
        common_postings.append(term)
    result_docs = []
    if len(common_postings) > 1:
        result = positional_intersect(common_postings[0], common_postings[1], differences[0])
        for i, d in zip(range(2, len(common_postings)), range(1, len(differences))):
            result = positional_intersect(result, common_postings[i], differences[d])
        for item in result:
            if len(item[1]) != 0:
                result_docs.append(item[0])
    else:
        for term in common_postings:
            for item in term:
                if len(item[1]) != 0:
                    result_docs.append(item[0])
    return result_docs
