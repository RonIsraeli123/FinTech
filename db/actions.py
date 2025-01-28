from db.connect import collection

def insert_many(documents):
    collection.insert_many(documents)
    print("Documents inserted successfully {}".format(documents))
    
def insert_one(document):
    collection.insert_one(document)
    print("Document inserted successfully {}".format(document))
    
def find_one(query):
    return collection.find(query)
