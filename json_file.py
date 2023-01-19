import json
import settings

def save_json(test_dict:dict):
    try:
        with open(settings.path_json, "w+") as file:
            json.dump(test_dict, file,  ensure_ascii=False)
    except Exception as Ex:
        print(f"Error save_json. Exeption: {Ex}")

def init_json():
    try:
        with open(settings.path_json,  'r') as file:
            json_file = json.load(file)
    except FileNotFoundError:
        print ("File not found")
        return 1
    except Exception as Ex:
        print("Error init json: " + str(Ex) + "\n")
        return 1
    return json_file
