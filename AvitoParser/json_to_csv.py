import csv
import json



def json_to_dict(filename: str) -> dict:
    """reads json file"""
    with open(filename, "r", encoding="utf-8") as file:
        data = json.loads(file.read())
    return data


def refactor_data(data: dict) -> dict:
    """brings each object to a single number of features"""
    data_csv = dict()
    for ind, obj in enumerate(data):
        for key in data_csv.keys():
            data_csv[key].append(obj.get(key))
        for key in (obj.keys() - data_csv.keys()):
            data_csv[key] = ([None] * ind) + [obj[key]]
    return data_csv

def dict_to_csv(data: dict, filename: str):
    """saves csv file with given data"""
    with open(filename, "w", encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=";")
        # headers of csv
        headers = list(data.keys())
        writer.writerow(headers)
        # iterating through every index
        for ind in range(len(data[list(data.keys())[0]])):
            row = []
            for key in data.keys():
                row.append(data[key][ind])
            writer.writerow(row)

if __name__ == "__main__":
    data = json_to_dict("dataset.json")
    data = refactor_data(data)
    dict_to_csv(data, "dataset.csv")