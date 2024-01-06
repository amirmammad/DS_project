
# Data Structure Project
# Search Engine(Phase 1)
# Collabrators: Seyyed Amirmohammad Mirshamsi, Mohammadhossein Damad

from math import log, sqrt
from difflib import SequenceMatcher
from collections import Counter
import numpy
from whoosh.analysis import SimpleAnalyzer, StopFilter

dir_path = "C:/Users/amrmr/OneDrive/Desktop/data"

class Query:
    def __init__(self, text):
        self.dim = set(Line.tokenize_line(text))
        self.tf = Line.calculate_tf(text, self.dim)
        self.doc_level_vector = dict()
        self.line_level_vector = dict()


    def doc_vector_cal(self, idf):
        for term in self.dim:
            self.doc_level_vector[term] = self.tf[term] * idf[term]


    def line_vector_cal(self, idf):
        for term in self.dim:
            self.line_level_vector[term] = self.tf[term] * idf[term]



class Line:
    def __init__(self, line, dim):
        self.dim = dim
        self.tf = Line.calculate_tf(line, self.dim)
        self.vector = dict()
    

    @staticmethod
    def calculate_tf(text, dim):
        term_counter = Counter()
        tokenized_line = Line.tokenize_line(text)
        for term in dim:
            term_counter[term] = 0
            for word in tokenized_line:
                if SequenceMatcher(None, term, word).quick_ratio() >= 0.95:
                    term_counter[term] += 1
        tf = dict()
        for term in term_counter:
            tf[term] = term_counter[term] / len(tokenized_line)
        return tf

    def line_vector_cal(self, idf):
        for term in self.dim:
            self.vector[term] = self.tf[term] * idf[term]


    @staticmethod
    def tokenize_line(line):
        '''Create a SimpleAnalyzer with default stop words
           Tokenize the query using the analyzer'''
        analyzer = SimpleAnalyzer() | StopFilter()
        tokens = [token.text for token in analyzer(line)]
        return tokens


class Document:
    def __init__(self, doc_num, dim): 
        self.dim = dim
        text = open(f"{dir_path}/document_{doc_num}.txt", "r", encoding='utf-8').read()
        line_list = list()
        for line in text.split("\n"):
            line_list.append(Line(line, self.dim))
        self.line_array = numpy.array(line_list)
        self.tf = self.tf_calculator()
        self.vector = dict()


    def tf_calculator(self):
        doc_tf = dict()
        for term in self.dim:
            doc_tf[term] = 0
            for line in self.line_array:
                doc_tf[term] += line.tf[term]
        return doc_tf


    def doc_vector_cal(self, idf):
        for term in self.dim:
            self.vector[term] = self.tf[term] * idf[term]

    
    def line_level_vector_calculator(self, query):
        #calculate idf in doc level
        term_counter = Counter()
        for line in self.line_array:
            for term in self.dim:
                if line.tf[term] != 0:
                    term_counter[term] += 1
        idf = dict()
        for term in self.dim:
            idf[term] = log(len(self.line_array) / (term_counter[term] + 1))
        #calling each line and query vector calculator
        query.line_vector_cal(idf)
        for line in self.line_array:
            line.line_vector_cal(idf)



class Program_1:
    def __init__(self, query, doc_list):
        self.query = Query(query)
        self.doc_dict = dict()
        for doc_num in doc_list:
            self.doc_dict[doc_num] = Document(doc_num, self.query.dim)
        self.doc_level_vector_calculator()
        self.doc_ans = self.nearest_doc()
        self.doc_dict[self.doc_ans].line_level_vector_calculator(self.query)
        self.par_ans = self.nearest_par(self.doc_ans)


    def doc_level_vector_calculator(self):
        #calculate idf in doc level
        term_counter = Counter()
        for doc in self.doc_dict:
            for term in self.query.dim:
                if self.doc_dict[doc].tf[term] != 0:
                    term_counter[term] += 1
        idf = dict()
        for term in self.query.dim:
            idf[term] = log(len(self.doc_dict) / (term_counter[term] + 1))
        #calling each doc and query vector calculator
        self.query.doc_vector_cal(idf)
        for doc in self.doc_dict:
            self.doc_dict[doc].doc_vector_cal(idf)


    def nearest_doc(self):
        return self.max_comparator(self.query, self.doc_dict, type="doc")


    def nearest_par(self, doc_num):
        return self.max_comparator(self.query, self.doc_dict[doc_num].line_array, type="par")


    def max_comparator(self, query, search_domain, type):
        similarity_score_dict = dict()
        index = 0
        for instance in search_domain:
            if type == "doc":
                similarity_score_dict[instance] = self.cosine_similarity(query.doc_level_vector, search_domain[instance].vector)
            else:
                similarity_score_dict[index] = self.cosine_similarity(query.line_level_vector, instance.vector)
                index += 1
        similarity_score_list = sorted(similarity_score_dict.items(), key=lambda x: x[1], reverse=True)
        return similarity_score_list[0][0]


    @staticmethod
    def cosine_similarity(vec1, vec2):
        dot_product = sum(vec1[key] * vec2[key] for key in vec1.keys())
        magnitude1 = sqrt(sum(value ** 2 for value in vec1.values()))
        magnitude2 = sqrt(sum(value ** 2 for value in vec2.values()))

        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0

        similarity = dot_product / (magnitude1 * magnitude2)
        return similarity
        


if __name__ == "__main__" :
    query = str(input("Enter the query : "))
    doc_list = input("Enter the document numbers : ").split(" ")
    system = Program_1(query, doc_list)
    print(system.doc_ans)
    print(system.par_ans)
