"""
Filename: data_store_pickle.py

Author: Aleesha Bunrith(z5371516)
Created: 15/03/2022 - 21/03/2022

Description: pickles the data from data_store into the datastore.p file
"""

import pickle

from src.data_store import data_store

def pickle_data():
    DATA_STRUCTURE = data_store.get()

    with open('datastore.p', 'wb') as FILE:
        pickle.dump(DATA_STRUCTURE, FILE)

def set_prev_data(pickled_data):
    data_store.set(pickled_data)
    