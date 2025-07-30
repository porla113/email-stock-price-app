import os
import json

def list_to_json(data_list, json_file):
    if os.path.exists(json_file):
    
        # Open the file in write mode ("w") and use json.dump() to write the data
        with open(json_file, "w") as file:
            json.dump(data_list, file, indent=4) # indent for pretty-printing

        print(f"Data successfully written to {json_file}")
    else:
        print(f"Error: {json_file} is not found.")

if __name__ == "__main__":
    test_data = {
        "name": "Alice",
        "age": 30,
        "isStudent": False,
        "courses": ["Math", "Science", "History"]
    }
    list_to_json(test_data, "test_write.json")