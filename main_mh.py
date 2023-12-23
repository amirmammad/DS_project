
# Data Structure Project
# Search Engine(Phase 1)
# Collabrators: Seyyed Amirmohammad Mirshamsi, Mohammadhossein Damad

import os
from math import log, sqrt
from difflib import SequenceMatcher
from collections import Counter
from whoosh.analysis import SimpleAnalyzer, StopFilter

#static methods
#tokenizing
def tokenize(text):
    analyzer = SimpleAnalyzer() | StopFilter()
    tokens = [token.text for token in analyzer(text)]
    return tokens

#static fields
query = str()
dim = set()
docs_text = dict()

#class for calculating vector of each paragraph of each document
class Line_1:
    def __init__(self, idf, tf):
        self.tf = tf
        self.idf = idf
        self.vector = self.build_line_1_vector()

    #building the vector of the paragraph
    def build_line_1_vector(self):
        tf_idf = dict()
        for term in dim:
            tf_idf[term] = self.tf[term] * self.idf[term]
        return tf_idf

#class for calculating vector of each document
class Document:
    def __init__(self, doc_text):
        self.doc_text = doc_text
        self.doc_lines_idf = self.line_1_idf_calculator(doc_text)
        self.doc_lines_tf = self.line_1_tf_calculator(tokenize(doc_text))
        self.line_vector_list = list()
        for line in doc_text.split("\n"):
            self.line_vector_list.append(Line_1(self.doc_lines_idf, self.doc_lines_tf))
        self.doc_vector = self.sum_line_vectors()

    #calculating idf of vector of each paragraph of each document in range of all of the paragraphs of the document of that paragraph
    def line_1_idf_calculator(self, doc_text):
        term_counter = Counter()
        doc_lines = doc_text.split("\n")
        for term in dim:
            for line in doc_lines:
                if term in tokenize(line):
                    term_counter[term] += 1
        idf = dict()
        for term in dim:
            if term_counter[term] == 0:
                idf[term] = log((len(doc_lines)) / 0.001)
            else:
                idf[term] = log(len(doc_lines) / (term_counter[term]))
        return idf

    #calculating tf of vector of each paragraph of each document in range of all of the words of the document of that paragraph
    def line_1_tf_calculator(self, tokenized_doc_text):
        term_counter = Counter()
        for term in dim:
            term_counter[term] = 0
        for term in tokenized_doc_text:
            if term in dim:
                term_counter[term] += 1
        tf = dict()
        for term in term_counter:
            tf[term] = term_counter[term]
        return tf 

    #calculating the sum of paragraphs vectors of the document and building the document vector
    def sum_line_vectors(self):
        doc_vector = Counter()
        for line in self.line_vector_list:
            for term in dim:
                doc_vector[term] += line.vector[term]
        doc_vector_dict = dict()
        for term in doc_vector:
            doc_vector_dict[term] = doc_vector[term]
        return doc_vector_dict

#class for calculating vector of query when comparing to vector of documents
class Query_1:
    def __init__(self, doc_list):
        self.idf = self.query_1_idf_calculator(doc_list)
        self.tf = self.query_1_tf_calculator(doc_list)
        self.vector = self.build_query_1_vector()
    
    #calculating idf of vector of query_1 in range of all of the documents of testcase
    def query_1_idf_calculator(self, doc_list):
        doc_counter = Counter()
        for term in dim:
            for doc_num in doc_list:
                tokenized_doc_text = tokenize(docs_text[doc_num])
                if term in tokenized_doc_text:
                    doc_counter[term] += 1
        idf = dict()
        for term in dim:
            if doc_counter[term] == 0:
                idf[term] = log((len(doc_list)) / 1)
            else:
                idf[term] = log(len(doc_list) / doc_counter[term])
        return idf

    #calculating tf of vector of query_1 in range of all of the words of all of the documents of testcase
    def query_1_tf_calculator(self, doc_list):
        term_counter = Counter()
        for term in dim:
            term_counter[term] = 0
        for doc_num in doc_list:
            doc_words = tokenize(docs_text[doc_num])
            for term in doc_words:
                if term in dim:
                    term_counter[term] += 1
        query_words = tokenize(query)
        for term in query_words:
            if term in dim:
                term_counter[term] += 1 
        tf = dict()
        for term in term_counter:
            tf[term] = term_counter[term]
        return tf

    #building the vector of query_1
    def build_query_1_vector(self):
        tf_idf = dict()
        for term in dim:
            tf_idf[term] = self.tf[term] * self.idf[term]
        return tf_idf

#class for calculating vector of query when comparing to vectors of paragraphs of the most related document
class Query_2:
    def __init__(self, doc_text):
        self.idf = self.query_2_idf_calculator(doc_text)
        self.tf = self.query_2_tf_calculator(doc_text)
        self.vector = self.build_query_2_vector()

    #calculating idf of vector of query_2 in range of all of the paragraphs of the most related document
    def query_2_idf_calculator(self, doc_text):
        term_counter = Counter()
        doc_lines = doc_text.split("\n")
        for term in dim:
            for line in doc_lines:
                if term in tokenize(line):
                    term_counter[term] += 1
        idf = dict()
        for term in dim:
            if term_counter[term] == 0:
                idf[term] = log((len(doc_lines)) / 1)
            else:
                idf[term] = log(len(doc_lines) / term_counter[term])
        return idf

    #calculating tf of vector of query_2 in range of all of the words of the most related document
    def query_2_tf_calculator(self, doc_text):
        term_counter = Counter()
        for term in dim:
            term_counter[term] = 0
        doc_words = tokenize(doc_text)
        for term in doc_words:
            if term in dim:
                term_counter[term] += 1
        query_words = tokenize(query)
        for term in query_words:
            if term in dim:
                term_counter[term] += 1
        tf = dict()
        for term in term_counter:
            tf[term] = term_counter[term]
        return tf

    #building the vector of query_2
    def build_query_2_vector(self):
        tf_idf = dict()
        for term in dim:
            tf_idf[term] = self.tf[term] * self.idf[term]
        return tf_idf

#class for calculating vector of each paragraph of the most related document
class Line_2:
    def __init__(self, idf, line_text):
        self.line_text = line_text
        self.idf = idf
        self.tf = self.line_2_tf_calculator(tokenize(line_text))
        self.vector = self.build_line_2_vector()

    #calculating tf of vector of each paragraph of the most related document in range of all of the words of that paragraph
    def line_2_tf_calculator(self, line_words):
        term_counter = Counter()
        for term in dim:
            term_counter[term] = 0
        for term in line_words:
            if term in dim:
                term_counter[term] += 1
        tf = dict()
        for term in term_counter:
            tf[term] = term_counter[term]
        return tf

    #building the vector of the paragraph
    def build_line_2_vector(self):
        tf_idf = dict()
        for term in dim:
            tf_idf[term] = self.tf[term] * self.idf[term]
        return tf_idf

#class for running program
class Program:
    def __init__(self, Query, doc_list):
        query = Query
        dim = set(tokenize(query))
        for doc_num in doc_list:
            docs_text[doc_num] = open(os.getcwd() + "\\data\\document_" + str(doc_num) + ".txt", "r", encoding='utf-8').read()
        self.query_1 = Query_1(doc_list)
        self.doc_dict = dict()
        for doc_num in doc_list:
            self.doc_dict[doc_num] = Document(docs_text[doc_num])
        self.most_related_doc_number = self.max_comparator(self.doc_dict, type="doc")
        self.most_related_doc_text = self.doc_dict[self.most_related_doc_number].doc_text 
        print(self.most_related_doc_number)
        self.query_2 = Query_2(self.most_related_doc_text)
        self.most_related_doc_lines_vector_list = list()
        self.most_related_doc_lines_idf = self.line_2_idf_calculator(self.most_related_doc_text)
        self.most_related_doc_lines = self.most_related_doc_text.split("\n")
        for line_text in self.most_related_doc_lines:
            self.most_related_doc_lines_vector_list.append(Line_2(self.most_related_doc_lines_idf, line_text))
        print(self.max_comparator(self.most_related_doc_lines_vector_list, type="par") + 1)
    
    #calculating idf of vector of each paragraph of the most related document in range of all of the words of the most related document
    def line_2_idf_calculator(self, doc_text):
        term_counter = Counter()
        for term in dim:
            term_counter[term] = 0
        doc_words = tokenize(doc_text)
        for term in doc_words:
            if term in dim:
                term_counter[term] += 1
        idf = dict()
        for term in term_counter:
            if term_counter[term] == 0:
                idf[term] = log((len(doc_words)) / 0.001)
            else:
                idf[term] = log(len(doc_words) / (term_counter[term]))
        return idf

    #finding the most similar document and paragraph with cosines and sequencematcher
    def max_comparator(self, search_domain, type):
        similarity_score_dict = dict()
        for instance in search_domain:
            if type == "doc":
                similarity_score_dict[instance] = 0.29 * (self.cosine_similarity(self.query_1.vector, search_domain[instance].doc_vector)) + 0.71 * (SequenceMatcher(None, query, search_domain[instance].doc_text).ratio())
            else:
                similarity_score_dict[search_domain.index(instance)] = 0.84 * (self.cosine_similarity(self.query_2.vector, instance.vector)) + 0.16 * (SequenceMatcher(None, query, instance.line_text).ratio())
        similarity_score_list = sorted(similarity_score_dict.items(), key=lambda x: x[1], reverse=True)
        return similarity_score_list[0][0]

    #calculating cosines
    @staticmethod
    def cosine_similarity(vec1, vec2):
        dot_product = sum(vec1[key] * vec2[key] for key in vec1.keys())
        magnitude1 = sqrt(sum(value ** 2 for value in vec1.values()))
        magnitude2 = sqrt(sum(value ** 2 for value in vec2.values()))
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        similarity = dot_product / (magnitude1 * magnitude2)
        return similarity
