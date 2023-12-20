
# Data Structure Project
# Search Engine(Phase 1)
# Collabrators: Seyyed Amirmohammad Mirshamsi, Mohammadhossein Damad

import os
from math import log
from collections import Counter
from whoosh.analysis import SimpleAnalyzer, StopFilter


class Line:
    def __init__(self, doc, idf, dim):
        self.tokenized_doc = self.tokenize_line(doc)
        self.dim = dim
        self.tf = self.calculate_tf()
        self.idf = idf
        self.vector = self.calculate_vector()
        

    def calculate_tf(self):
        term_counter = Counter()
        for term in self.tokenized_doc:
            if term in self.dim:
                term_counter[term] += 1
        tf = dict()
        for term in term_counter:
            tf[term] = term_counter[term]
        return tf


    def calculate_vector(self):
        tf_idf = dict()
        for term in self.dim:
            tf_idf[term] = self.tf[term] * self.idf[term]
        return tf_idf


    @staticmethod
    def tokenize_line(line):
        '''Create a SimpleAnalyzer with default stop words
           Tokenize the query using the analyzer'''
        analyzer = SimpleAnalyzer() | StopFilter()
        tokens = [token.text for token in analyzer(line)]
        return tokens


class Document:
    def __init__(self, doc, dim=None):
        self.line_vector_list = list()
        self.dim = dim
        self.idf = self.line_idf_calculator(doc)
        for line in doc.split("\n"):
            self.line_vector_list.append(Line(doc, self.idf, self.dim))
        self.doc_vector = self.sum(self.line_vector_list)


    def line_idf_calculator(self, doc):
        term_counter = Counter()
        num_par = len(doc.split("\n"))
        for term in self.dim:
            for line in doc.split("\n"):
                if term in line:
                    term_counter[term] += 1
        idf = dict()
        for term in self.dim:
            idf[term] = log(num_par / term_counter[term])
        return idf

    
    def sum(self, line_vector_list):
        vector_sum = dict()
        for line in line_vector_list:
            for term in self.dim:
                vector_sum[term] += line.vector[term]
        return vector_sum


class Query:
    def __init__(self, query, doc_list):
        self.dim = set(Line.tokenize_line(query))
        self.idf = self.query_idf_calculator(self.dim, doc_list)
        self.tf = self.query_tf_calculator(query, self.dim, doc_list)
        self.vector = self.calculate_vector()
    

    def query_idf_calculator(self, dim, doc_list):
        doc_counter = Counter()
        for term in self.dim:
            for doc_num in doc_list:
                if term in Line.tokenize_line(open(os.getcwd() + "\\data\\document_" + doc_num + ".txt").read()):
                    doc_counter[term] += 1
        idf = dict()
        for term in self.dim:
            idf[term] = log(len(doc_list) / (doc_counter[term] + 1))
        return idf


    def query_tf_calculator(self, query, dim, doc_list):
        term_counter = Counter()
        for doc_num in doc_list:
            doc_words = Line.tokenize_line(open(os.getcwd() + "\\data\\document_" + doc_num + ".txt").read())
            for term in doc_words:
                if term in self.dim:
                    term_counter[term] += 1
        query_words = Line.tokenize_line(query)
        for term in query_words:
            if term in self.dim:
                term_counter[term] += 1
        tf = dict()
        for term in term_counter:
            tf[term] = term_counter[term]
        return tf


    def calculate_vector(self):
        tf_idf = dict()
        for term in self.dim:
            tf_idf[term] = self.tf[term] * self.idf[term]
        return tf_idf


class Program:
    def __init__(self, query, doc_list):
        self.query = Query(query, doc_list)
        self.doc_dict = dict()
        for doc in doc_list:
            doc_text = open(os.getcwd() + "\\data\\document_" + doc + ".txt").read()
            self.doc_dict[doc] = Document(doc_text, query.dim)


if __name__ == "__main__" :
    query = str(input("Enter the query : "))
    doc_list = input("Enter the document numbers : ").split()
    system = Program(query, doc_list)