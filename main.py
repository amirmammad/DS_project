
# Data Structure Project
# Search Engine(Phase 1)
# Collabrators: Seyyed Amirmohammad Mirshamsi, Mohammadhossein Damad


from whoosh.analysis import SimpleAnalyzer, StopFilter


def tokenize_query(query):
    # Create a SimpleAnalyzer with default stop words
    analyzer = SimpleAnalyzer() | StopFilter()

    # Tokenize the query using the analyzer
    tokens = [token.text for token in analyzer(query)]
    return tokens


if __name__ == "__main__" :
    query = str(input())
    print(tokenize_query(query))
