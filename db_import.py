import pymongo
import sys, os, json
import pandas as pd

DB = pymongo.MongoClient(os.environ['MONGODB_URI'], 
                         connectTimeoutMS=30000,
                         socketTimeoutMS=None,
                         socketKeepAlive=True)['jakartaku']

def main():
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
    collection.remove()
    collection.insert(data_json)

if __name__ == "__main__":
    main()