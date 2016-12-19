from pymongo import MongoClient
import json

def main():
    client = MongoClient()
    collection = client.test.test
    cursor = collection.find()

    print("Number of documents:{}".format(cursor.count()))
    for document in cursor[:2]:
        document.pop('_id')
        docprint(document)
    return 0

def docprint(document):
    """Prints Mongo document i.e Python object 
    """
    print(json.dumps(document, sort_keys=True, indent=4))

if __name__ == "__main__":
    main()