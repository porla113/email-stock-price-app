import json

def json_to_list(json_file):
    try:
        with open(json_file, "r") as file:
            data_dict = json.load(file)
        return data_dict
    except FileNotFoundError:
        print(f"Error: {json_file} not found.")
    except json.JSONDecodeError:
        print("Error: Cloud not decode JSON.")

if __name__ == "__main__":
    test_list = json_to_list("stocks.json")
    print(test_list)