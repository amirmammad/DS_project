
# Data Structure Project
# Search Engine(Phase 1)
# Collabrators: Seyyed Amirmohammad Mirshamsi, Mohammadhossein Damad

import numpy 

from collections import Counter
from whoosh.analysis import SimpleAnalyzer, StopFilter


class Line:
    def __init__(self, line, idf, dim=None):
        self.tokenized_line = self.tokenize_line(line)
        if dim == None:
            self.dim = tuple(set(self.tokenized_line))
        else:
            self.dim = dim
        self.tf = self.calculate_tf()
        self.idf = idf
        

    def calculate_tf(self):
        word_counter = Counter()
        for term in self.tokenized_line:
            if term in self.dim:
                word_counter[term] += 1
        tf = dict()
        for term in word_counter:
            tf[term] = word_counter[term] / len(self.tokenized_line)
        return tf


    @staticmethod
    def tokenize_line(line):
        '''Create a SimpleAnalyzer with default stop words
           Tokenize the query using the analyzer'''
        analyzer = SimpleAnalyzer() | StopFilter()
        tokens = [token.text for token in analyzer(line)]
        return tokens



class Document:
    def __init__(self, doc, dim):
        self.line_vector_list = list()
        self.dim = dim
        self.doc_level_idf = 0 #weshould add somethong here
        for line in doc.split("\n"):
            self.line_vector_list.append(Line(line))
        self.doc_vector = self.sum(self.line_vector_list)



class Program:
    def __init__(self, query, doc_list):
        self.query = Line(query)
        self.doc_dict = dict()
        for doc in doc_list:
            self.doc_dict[doc] = Document(doc, query.dim)
    

    def doc_idf_calculator(self): #this function should be repaired
        term_counter = Counter()
        for term in self.query.dim:
            pass
        doc_idf = dict()



if __name__ == "__main__" :
    query = str(input("Enter the query"))
    doc_list = input("Enter the document numbers").split(" ")
    system = Program(query, doc_list)


