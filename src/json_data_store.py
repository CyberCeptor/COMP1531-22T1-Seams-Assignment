import json

from src.data_store import data_store

DATA_STRUCTURE = {
    data_store.get()
}

with open('export.json', 'w') as FILE:
    print(json.dumps(DATA_STRUCTURE))
    json.dump(DATA_STRUCTURE, FILE)