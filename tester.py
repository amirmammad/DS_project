import json
from tqdm import tqdm
import main_mh
import os

file_path = os.getcwd() + "\\data.json"

if __name__ == "__main__":
    with open(file_path, 'r') as file:
        data_list = json.load(file)
    counter = 22246
    true_counter = 15258
    #data = tqdm(data_list, desc="Processing JSON data")
    #for data in tqdm(data_list, desc="Processing JSON data"):
    while counter != len(data_list):
        main_mh.Static.InputGir(data_list[counter]["query"], data_list[counter]["candidate_documents_id"])
        if main_mh.Static.most_related_doc_number == int(data_list[counter]["document_id"]):
            true_counter += 1
        counter += 1
        print(counter)
        print(true_counter)
    true_percentage = (true_counter / len(data_list)) * 100
    print(true_percentage)