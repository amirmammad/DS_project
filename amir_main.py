
# Data Structure Project
# Search Engine(Phase 1)
# Collabrators: Seyyed Amirmohammad Mirshamsi, Mohammadhossein Damad

from math import log, sqrt
from difflib import SequenceMatcher
from collections import Counter
from whoosh.analysis import SimpleAnalyzer, StopFilter

dir_path = "C:/Users/amrmr/OneDrive/Desktop/data"
class Line:
    def __init__(self, line, dim):
        self.text = line
        self.dim = dim
        self.tf = self.calculate_tf()
        self.vector = dict()
        

    def calculate_tf(self):
        term_counter = Counter()
        for term in self.dim:
            term_counter[term] = 0
        for term in self.tokenize_line(self.text):
            if term in self.dim:
                term_counter[term] += 1
        tf = dict()
        for term in term_counter:
            tf[term] = term_counter[term] / len(self.tokenize_line(self.text))
        return tf


    @staticmethod
    def tokenize_line(line):
        '''Create a SimpleAnalyzer with default stop words
           Tokenize the query using the analyzer'''
        analyzer = SimpleAnalyzer() | StopFilter()
        tokens = [token.text for token in analyzer(line)]
        return tokens


class Document:
    def __init__(self, doc_num, dim=None):
        self.line_list = list()
        if dim is None:
            self.dim = set(Line.tokenize_line(doc_num))
            text = doc_num
        else:
            self.dim = dim
            text = open(f"{dir_path}/document_{doc_num}.txt", "r", encoding='utf-8').read()
        for line in text.split("\n"):
            self.line_list.append(Line(line, self.dim))
        self.idf = self.line_idf_calculator()
        self.line_vector_calculator()
        self.vector = self.vector_sum()



    @property
    def text(self):
        text = str()
        for line in self.line_list:
            text += line.text
        return text


    def line_idf_calculator(self):
        term_counter = Counter()
        num_par = 0
        for line in self.line_list:
            num_par += 1
            for term in self.dim:
                if line.tf[term] != 0:
                    term_counter[term] += 1
        idf = dict()
        for term in self.dim:
            idf[term] = log(num_par/ (term_counter[term] + 1))
        return idf

    
    def line_vector_calculator(self):
        for line in self.line_list:
            for term in self.dim:
                line.vector[term] = line.tf[term] * self.idf[term]


    def vector_sum(self):
        vector_sum = dict()
        for term in self.dim:
            vector_sum[term] = 0
            for line in self.line_list:
                vector_sum[term] += line.vector[term]
        return vector_sum


class Program_1:
    def __init__(self, query, doc_list):
        self.query = Document(query)
        self.doc_dict = dict()
        for doc_num in doc_list:
            self.doc_dict[doc_num] = Document(doc_num, self.query.dim)
    
    @property
    def nearest_doc(self):
        return self.max_comparator(self.query, self.doc_dict, type="doc")
    
    
    @property
    def nearest_par(self):
        return self.max_comparator(self.query, self.doc_dict[self.nearest_doc].line_list, type="par")


    def max_comparator(self, query, search_domain, type):
        similarity_score_dict = dict()
        for instance in search_domain:
            if type == "doc":
                similarity_score_dict[instance] = 0.6 * (self.cosine_similarity(query.vector, search_domain[instance].vector)) + 0.4 * (SequenceMatcher(None, query.text, search_domain[instance].text).ratio())
            else:
                similarity_score_dict[search_domain.index(instance)] = 0.4 * (self.cosine_similarity(query.vector, instance.vector)) + 0.6 * (SequenceMatcher(None, query.text, instance.text).ratio())
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
    print(system.nearest_doc)
    print(system.nearest_par)
