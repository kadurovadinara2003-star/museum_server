import json

with open("data/exhibits.json", "r", encoding="utf-8") as f:
    EXHIBITS = json.load(f)

def get_exhibit_by_id(exhibit_id):

    for exhibit in EXHIBITS:
        if exhibit["id"] == exhibit_id:
            return exhibit

    return None