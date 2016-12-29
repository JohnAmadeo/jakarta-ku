#!/usr/bin/python

from pymongo import MongoClient
import json
client = MongoClient()
db = client.get_database('jakartaku')
col = db.get_collection('education')

def main(num):

    if num == 1:
        # Number of citizens who have completed each education level
        # for all the regions selected
        cursor = col.aggregate([{
                "$match": {"$or": [{"Kecamatan": "tebet"},
                                   {"Kecamatan": "kebon jeruk"}]}
            }])

        for result in cursor:
            docprint(result)

    elif num == 2:
        # Number of citizens who have completed SD per region 
        # in ascending order of kecamatan name
        cursor = col.aggregate([{
                    "$group": {
                        "_id": "$Kecamatan",
                        "count": {"$sum": "$SD"}
                    }
                },
                {
                    "$sort": {
                        "_id": 1
                    }
                }])

        for result in cursor:
            print(result)

def docprint(document):
    """Prints Mongo document i.e Python object 
    """
    del document['_id']
    print(json.dumps(document, sort_keys=True, indent=4))

if __name__ == "__main__":
    main(1)

