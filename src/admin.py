
from src.data_store import data_store

def count_global_owners():
    store = data_store.get()
    # return store['users'].count(['perm_id'] == 1)
    count = list(filter(lambda id: ['perm_id'] == 1, store['users']))
    return count
