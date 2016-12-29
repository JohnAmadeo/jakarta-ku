#!/usr/bin/python

from pymongo import MongoClient
import json
client = MongoClient()
db = client.get_database('jakartaku')
col = db.get_collection('education')

def get_education_charts_by_category():
    region_list = ["koja"]
    
    match_list = [{"Kecamatan": region} for region in region_list]

    spacetime_list = ['Kecamatan', 'Kabupaten', 'Kelurahan', 'Tahun']
    project_list = [field for field in list(col.find_one().keys()) 
                    if field not in spacetime_list]
    project_object = {}
    for field in project_list:
        project_object[field] = 1

    group_object = {"_id": "null"}
    for field in project_list:
        if field != "_id":
            group_object[field] = {"$sum" : ("$" + field)}

    cursor = \
    col.aggregate([{
        "$match": {"$or": match_list}
    }, 
    {
        "$project": project_object
    },
    {
        "$group": group_object
    },
    {
        "$project": {"_id": 0}
    }])

    quantity_chart = {'field': 'quantity'}
    for result in cursor:
        quantity_chart['data'] = result

def main(num):
    if num == 1:
        get_edu_by_category()
    elif num == 2:
        # Number of citizens who have completed each education level
        # for all the regions selected
        cursor = \
        col.aggregate([{
            "$match": {"$or": [{"Kecamatan": "tebet"},
                               {"Kecamatan": "kebon jeruk"}]}
        }, 
        {
            "$project": {"_id" : 1, "Kecamatan" : 1, "SD" : 1, 
                         "SMA": 1, "S1": 1, "S3": 1}
        },
        {
            "$group": {"_id": "null", 
                       "SD" : {"$sum": "$SD"}, 
                       "SMA" : {"$sum": "$SMA"}}
        }])

        for result in cursor:
            docprint(result)

    elif num == 3:
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
    main(1)

