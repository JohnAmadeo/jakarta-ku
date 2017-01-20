import pymongo
import sys, os, json
import pandas as pd

DB = pymongo.MongoClient(os.environ['MONGODB_URI'], 
                         connectTimeoutMS=30000,
                         socketTimeoutMS=None,
                         socketKeepAlive=True)['heroku_1r8z46f3']

def main():
    global DB
    folder = 'static/csv/'
    import_content(folder + 'religion2013_clean.csv','religion')
    import_content(folder + 'occupation2013_clean.csv','occupation')
    import_content(folder + 'demographics2014_clean.csv','demographics')
    import_content(folder + 'education2014_clean.csv','education')
    import_content(folder + 'marriage2015_clean.csv','marriage')

def import_content(filepath, collection_name):
    global DB
    collection = DB[collection_name]
    data = pd.read_csv(filepath)
    data_json = json.loads(data.to_json(orient='records'))
    print(json.dumps(data_json))
    # collection.remove()
    # collection.insert(data_json)

def jsonprint(obj):
    """Prints Mongo document i.e Python object 
    """
    try:
        print(json.dumps(obj, sort_keys=True, indent=4))
    except TypeError:
        obj_copy = obj.copy()
        del obj_copy['_id']
        print(json.dumps(obj_copy, sort_keys=True, indent=4))

if __name__ == "__main__":
    main()