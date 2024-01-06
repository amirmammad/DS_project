import json
import amir_main
from tqdm import tqdm

#u should change here
file_path = "C:/Users/amrmr/Downloads/DS_Project/data.json"


if __name__ == "__main__":
    with open(file_path, 'r') as file:
        data_list = json.load(file)
    true_counter = 0
    for data in tqdm(data_list, desc="Processing JSON data"):
        #u should change here
        system = amir_main.Program_1(data["query"], data["candidate_documents_id"])
        if system.doc_ans == int(data["document_id"]):
            true_counter += 1
        print(f"\n{true_counter}")
    true_percentage = (true_counter / len(data_list)) * 100
    print(true_percentage)