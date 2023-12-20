
# Data Structure Project
# Search Engine(Phase 1)
# Collabrators: Seyyed Amirmohammad Mirshamsi, Mohammadhossein Damad

import os
from math import log, sqrt
from collections import Counter
from whoosh.analysis import SimpleAnalyzer, StopFilter

#class for each paragraph
class Line:
    def __init__(self, doc, idf, dim):
        self.tokenized_doc = Program.tokenize_line(doc)
        self.dim = dim
        self.tf = self.calculate_tf()
        self.idf = idf
        self.vector = self.calculate_vector()
        
    #calculating each paragraph tf
    def calculate_tf(self):
        term_counter = Counter()
        for term in self.dim:
            term_counter[term] = 0
        for term in self.tokenized_doc:
            if term in self.dim:
                term_counter[term] += 1
        tf = dict()
        for term in term_counter:
            tf[term] = term_counter[term]
        return tf

    #build the vector of each paragraph
    def calculate_vector(self):
        tf_idf = dict()
        for term in self.dim:
            tf_idf[term] = self.tf[term] * self.idf[term]
        return tf_idf


#class for each document
class Document:
    def __init__(self, doc, dim):
        self.line_vector_list = list()
        self.dim = dim
        self.idf = self.line_idf_calculator(doc)
        for line in doc.split("\n"):
            self.line_vector_list.append(Line(doc, self.idf, self.dim))
        self.doc_vector = self.sum(self.line_vector_list)

    #calculating each paragraph idf
    def line_idf_calculator(self, doc):
        term_counter = Counter()
        num_par = len(doc.split("\n"))
        for term in self.dim:
            for line in doc.split("\n"):
                if term in line:
                    term_counter[term] += 1
        idf = dict()
        for term in self.dim:
            if term_counter[term] == 0:
                term_counter[term] = 1
            idf[term] = log(num_par / term_counter[term])
        return idf

    #calculates the sum of paragraphs vectors and gives the doc vector
    def sum(self, line_vector_list):
        vector_sum = Counter()
        for line in line_vector_list:
            for term in self.dim:
                vector_sum[term] += line.vector[term]
        vector_sum_dict = dict()
        for term in vector_sum:
            vector_sum_dict[term] = vector_sum[term]
        return vector_sum_dict

#class for query
class Query:
    def __init__(self, query, doc_list):
        self.dim = set(Program.tokenize_line(query))
        self.idf = self.query_idf_calculator(self.dim, doc_list)
        self.tf = self.query_tf_calculator(query, self.dim, doc_list)
        self.vector = self.calculate_vector()
    
    #calculating query idf
    def query_idf_calculator(self, dim, doc_list):
        doc_counter = Counter()
        for term in self.dim:
            for doc_num in doc_list:
                if term in Program.tokenize_line(open(os.getcwd() + "\\data\\document_" + doc_num + ".txt").read()):
                    doc_counter[term] += 1
        idf = dict()
        for term in self.dim:
            idf[term] = log(len(doc_list) / (doc_counter[term] + 1))
        return idf

    #calculating query tf
    def query_tf_calculator(self, query, dim, doc_list):
        term_counter = Counter()
        for term in self.dim:
            term_counter[term] = 0
        for doc_num in doc_list:
            doc_words = Program.tokenize_line(open(os.getcwd() + "\\data\\document_" + doc_num + ".txt").read())
            for term in doc_words:
                if term in self.dim:
                    term_counter[term] += 1
        query_words = Program.tokenize_line(query)
        for term in query_words:
            if term in self.dim:
                term_counter[term] += 1
        tf = dict()
        for term in term_counter:
            tf[term] = term_counter[term]
        return tf

    #build the vector of query
    def calculate_vector(self):
        tf_idf = dict()
        for term in self.dim:
            tf_idf[term] = self.tf[term] * self.idf[term]
        return tf_idf

#class for running program
class Program:
    def __init__(self, query, doc_list):
        self.query = Query(query, doc_list)
        self.doc_dict = dict()
        for doc in doc_list:
            doc_text = open(os.getcwd() + "\\data\\document_" + doc + ".txt").read()
            self.doc_dict[doc] = Document(doc_text, self.query.dim)
        self.docs_cosine = self.calculate_cosine()
        print(max(self.docs_cosine, key = lambda x: self.docs_cosine[x]))

    #calculating cosines
    def calculate_cosine(self):
        docs_and_query_zarb_dakhly = Counter()
        for doc in self.doc_dict:
            for term in self.query.dim:
                docs_and_query_zarb_dakhly[doc] += self.doc_dict[doc].doc_vector[term] * self.query.vector[term]
        query_square_sum = 0
        for term in self.query.dim:
            query_square_sum += self.query.vector[term] ** 2
        docs_square_sum = Counter()
        for doc in self.doc_dict:
            for term in self.query.dim:
                docs_square_sum[doc] += self.doc_dict[doc].doc_vector[term] ** 2
        docs_cosine = Counter()
        for doc in self.doc_dict:
            temp = sqrt(docs_square_sum[doc]) * sqrt(query_square_sum)
            if temp == 0:
                docs_cosine[doc] = -1
            else:
                docs_cosine[doc] = docs_and_query_zarb_dakhly[doc] / temp
        docs_cosine_dict = dict()
        for doc_num in docs_cosine:
            docs_cosine_dict[doc_num] = docs_cosine[doc_num]
        return docs_cosine_dict


    #tokenizing
    @staticmethod
    def tokenize_line(line):
        '''Create a SimpleAnalyzer with default stop words
           Tokenize the query using the analyzer'''
        analyzer = SimpleAnalyzer() | StopFilter()
        tokens = [token.text for token in analyzer(line)]
        return tokens


if __name__ == "__main__" :
    query = str(input("Enter the query : "))
    doc_list = input("Enter the document numbers : ").split()
    system = Program(query, doc_list)
