
# Data Structure Project
# Search Engine(Phase 1)
# Collabrators: Seyyed Amirmohammad Mirshamsi, Mohammadhossein Damad


from whoosh.analysis import SimpleAnalyzer, StopFilter
import numpy
import math


def tokenize_text(text):
    analyzer = SimpleAnalyzer() | StopFilter()
    tokens = [token.text for token in analyzer(text)]
    return tokens


query_words = tokenize_text(str(input("Please enter your query : ")))
doc_list = str(input("Please enter the doc numbers : ")).split()
dir = "C:\\Users\\pc\\Desktop\\DS_project\\data"


def query_tf(word):
    repeat_count = 0
    for doc_num in doc_list:
        doc_words = tokenize_text(open(dir + "\\document_" + doc_num + ".txt").read())
        repeat_count += doc_words.count(word)
    return repeat_count


def query_idf(word):
    included_docs = 0
    for doc_num in doc_list:
        doc_words = tokenize_text(open(dir + "\\document_" + doc_num + ".txt").read())
        for each_word in doc_words:
            if each_word == word:
                included_docs += 1
                break
    if(included_docs == 0):
        included_docs = 1
    return len(doc_list)/included_docs


# def query_idf_in_paragraphs(word,doc_num):
#     paragraphs = open(dir + "\\document_" + doc_num + ".txt").read().split("\n")
#     included_paragraphs = 0
#     for paragraph in paragraphs:
#         paragraph_words = tokenize_text(paragraph)
#         for par_word in paragraph_words:
#             if par_word == word:
#                 included_paragraphs += 1
#                 break
#     if(included_paragraphs == 0):
#         included_paragraphs = 1
#     return len(paragraphs)/included_paragraphs


def doc_par_tf(word,paragraph_words):
    return paragraph_words.count(word)


def doc_idf(word,doc_paragraphs):
    included_paragraphs = 0
    for paragraph in doc_paragraphs:
        paragraph_words = tokenize_text(paragraph)
        for par_word in paragraph_words:
            if par_word == word:
                included_paragraphs += 1
                break
    if(included_paragraphs == 0):
        included_paragraphs = 1
    return len(doc_paragraphs)/included_paragraphs


# def doc_idf_in_words(word,paragraph_words):
#     return len(paragraph_words)/


def sum_vectors(vectors):
    vector_items = list()
    for dim in vectors[0]:
        vector_items.append(dim)
    i = 1
    while i != len(vectors):
        j = 0
        while j != len(vectors[i]):
            vector_items[j] += vectors[i][j]
            j += 1
        i += 1
    return numpy.array(vector_items)


def cosine(vec1,vec2):
    i = 0
    j = 0
    zarb_dakhely = 0
    while i != len(vec1) and j != len(vec2):
        zarb_dakhely += vec1[i] * vec2[j]
        i += 1
        j += 1
    i = 0
    vec1len = 0
    while i != len(vec1):
        vec1len += vec1[i] * vec1[i]
        i += 1
    j = 0
    vec2len = 0
    while j != len(vec2):
        vec2len += vec2[j] * vec2[j]
        j += 1
    if math.sqrt(vec1len) * math.sqrt(vec2len) == 0:
        return -1
    return zarb_dakhely/(math.sqrt(vec1len) * math.sqrt(vec2len))


if __name__ == "__main__" :
    unique_query_words = set(query_words)
    vector_items = list()
    for word in unique_query_words:
        vector_items.append(query_tf(word) * query_idf(word))
    query_vector = numpy.array(vector_items)
    doc_vectors_list = list()
    doc_pars_vectors_list = list()
    for doc_num in doc_list:
        paragraphs = open(dir + "\\document_" + doc_num + ".txt").read().split("\n")
        doc_pars_vectors = list()
        for paragraph in paragraphs:
            paragraph_words = tokenize_text(paragraph)
            vector_items = list()
            for word in unique_query_words:
                vector_items.append(doc_par_tf(word,paragraph_words) * doc_idf(word,paragraphs))
            doc_pars_vectors.append(numpy.array(vector_items))
        doc_pars_vectors_list.append(doc_pars_vectors)
        doc_vectors_list.append(sum_vectors(doc_pars_vectors))
    cosines = list()
    for vec in doc_vectors_list:
        cosines.append(cosine(vec,query_vector))
    x = cosines.index(max(cosines))
    print("document_id = " + doc_list[x])
    cosines.clear()