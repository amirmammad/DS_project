
# Data Structure Project
# Search Engine(Phase 1)
# Collabrators: Seyyed Amirmohammad Mirshamsi, Mohammadhossein Damad

import os
from math import log, sqrt
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
docs_text = Counter()

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
                idf[term] = log((len(doc_lines)) / 0.001) # contains + 1 or not ?
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
    
    #calculating idf of vector of query_1 in range of all of the documents of testcase(check if we should count query as a document or not!)
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
                idf[term] = log((len(doc_list)) / 0.001) # contains + 1 or not ?
            else:
                idf[term] = log((len(doc_list)) / (doc_counter[term])) # contains + 1 or not ?
        return idf

    #calculating tf of vector of query_1 in range of all of the words of all of the documents of testcase(check if we should count query words or not!)
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
        # this should be or not ?
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

    #calculating idf of vector of query_2 in range of all of the paragraphs of the most related document(check if we should count query as a paragraph or not!)
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
                idf[term] = log((len(doc_lines)) / 0.001) # contains + 1 or not ?
            else:
                idf[term] = log((len(doc_lines)) / ((term_counter[term]))) # contains + 1 or not ?
        return idf

    #calculating tf of vector of query_2 in range of all of the words of the most related document(check if we should count query words or not!)
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
        #this should be or not ?
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
    def __init__(self, query, doc_list):
        self.query_1 = Query_1(doc_list)
        self.doc_dict = dict()
        for doc_num in doc_list:
            self.doc_dict[doc_num] = Document(docs_text[doc_num])
        self.docs_cosines = self.calculate_docs_cosines()
        self.most_related_doc_number = max(self.docs_cosines, key = lambda x: self.docs_cosines[x])
        self.most_related_doc_text = self.doc_dict[self.most_related_doc_number].doc_text 
        print("document_id = " + self.most_related_doc_number)
        self.query_2 = Query_2(self.most_related_doc_text)
        self.max_doc_lines_vector_list = list()
        self.most_related_doc_lines_idf = self.line_2_idf_calculator(self.most_related_doc_text)
        self.max_doc_lines = self.most_related_doc_text.split("\n")
        for line_text in self.max_doc_lines:
            self.max_doc_lines_vector_list.append(Line_2(self.most_related_doc_lines_idf, line_text))
        self.lines_cosines = self.calculate_lines_cosines(self.max_doc_lines_vector_list)
        print("pararaph " + str(self.lines_cosines.index(max(self.lines_cosines)) + 1))

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
                idf[term] = log((len(doc_words)) / 0.001) # contains + 1 or not ?
            else:    
                idf[term] = log(len(doc_words) / (term_counter[term]))
        return idf

    #calculating cosines between docs vectors and query_1 vector
    def calculate_docs_cosines(self):
        docs_and_query_zarb_dakhly = Counter()
        for doc_num in self.doc_dict:
            for term in dim:
                docs_and_query_zarb_dakhly[doc_num] += self.doc_dict[doc_num].doc_vector[term] * self.query_1.vector[term]
        query_square_sum = 0
        for term in dim:
            query_square_sum += self.query_1.vector[term] ** 2
        docs_square_sum = Counter()
        for doc_num in self.doc_dict:
            for term in dim:
                docs_square_sum[doc_num] += self.doc_dict[doc_num].doc_vector[term] ** 2
        docs_cosines = Counter()
        for doc_num in self.doc_dict:
            temp = sqrt(docs_square_sum[doc_num]) * sqrt(query_square_sum)
            if temp == 0:
                docs_cosines[doc_num] = -1
            else:
                docs_cosines[doc_num] = docs_and_query_zarb_dakhly[doc_num] / temp
        docs_cosines_dict = dict()
        for doc_num in docs_cosines:
            docs_cosines_dict[doc_num] = docs_cosines[doc_num]
        return docs_cosines_dict

    #calculating cosines between the vector of paragraphs of the most related document and query_2 vector
    def calculate_lines_cosines(self, max_doc_lines_vector_list):
        lines_and_query_zarb_dakhly = list()
        for line_vector in max_doc_lines_vector_list:
            lines_and_query_zarb_dakhly.append(0)
        for line_vector in max_doc_lines_vector_list:
            for term in dim:
                lines_and_query_zarb_dakhly[max_doc_lines_vector_list.index(line_vector)] += self.query_2.vector[term] * line_vector.vector[term]
        query_2_square_sum = 0
        for term in dim:
            query_2_square_sum += self.query_2.vector[term] ** 2
        lines_square_sum = list()
        for line_vector in max_doc_lines_vector_list:
            lines_square_sum.append(0)
        for line_vector in max_doc_lines_vector_list:
            for term in dim:
                lines_square_sum[max_doc_lines_vector_list.index(line_vector)] += line_vector.vector[term] ** 2
        lines_cosines = list()
        for line_vector in max_doc_lines_vector_list:
            lines_cosines.append(0)
        for line_vector in max_doc_lines_vector_list:
            temp = sqrt(lines_square_sum[max_doc_lines_vector_list.index(line_vector)]) * sqrt(query_2_square_sum)
            if temp == 0:
                lines_cosines[max_doc_lines_vector_list.index(line_vector)] = -1
            else:
                lines_cosines[max_doc_lines_vector_list.index(line_vector)] = lines_and_query_zarb_dakhly[max_doc_lines_vector_list.index(line_vector)] / temp
        return lines_cosines

#giving inputs and running the program
if __name__ == "__main__" :
    query = str(input("Enter the query : "))
    dim = set(tokenize(query))
    doc_list = input("Enter the document numbers : ").split()
    for doc_num in doc_list:
        docs_text[doc_num] = open(os.getcwd() + "\\data\\document_" + doc_num + ".txt").read()
    system = Program(query, doc_list)
