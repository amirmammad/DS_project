import json
from tqdm import tqdm
import main_mh
import os

#u should change here
file_path = os.getcwd() + "\\data.json"


if __name__ == "__main__":
    with open(file_path, 'r') as file:
        data_list = json.load(file)
    true_counter = 0
    for data in tqdm(data_list, desc="Processing JSON data"):
        #u should change here
        system = main_mh.Program(data["query"], data["candidate_documents_id"])
        if system.most_related_doc_number == int(data["document_id"]):
            true_counter += 1
    true_percentage = (true_counter / len(data_list)) * 100
    print(true_counter)
    print()