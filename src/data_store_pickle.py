import pickle

from src.data_store import data_store

DATA_STRUCTURE = data_store.get()

with open('datastore.p', 'wb') as FILE:
    pickle.dump(DATA_STRUCTURE, FILE)
