from __future__ import print_function
from flask import Flask, render_template, request, redirect, make_response, Response
from pymongo import MongoClient
import os, json

app = Flask(__name__)
# Constants
DATABASE = MongoClient().get_database('jakartaku')
ID_LIST = ['Kecamatan', 'Kabupaten', 'Kelurahan', 'Tahun', '_id']

# Naming conventions
# ------------------------------------
# 1. Lists have names that end with '..._l'
#    e.g 'car_l', 'animal_l', 'winner_l'
# 2. 

def main():
    serve_education_charts_by_category(['koja'])

@app.route('/')
def serve_index():
    return render_template('index.html')

@app.route('/charts', methods=['POST'])
def serve_charts():
    body = request.get_json()
    comparison = body['comparison']
    region_list = body['region_list']
    category = body['category']

    if category == 'education' and comparison == "category": 
        return serve_education_charts_by_category(region_list)

def serve_education_charts_by_category(region_list):
    global DATABASE
    collection = DATABASE.get_collection('education')

    # Handle $match stage
    # ----------------------
    match_list = [{"Kecamatan": region} for region in region_list]

    # Handle $project stage
    # ----------------------
    # list all space/time fields in document
    spacetime_list = ['Kecamatan', 'Kabupaten', 'Kelurahan', 'Tahun']
    # list all education level fields
    edu_level_list = [field for field in list(collection.find_one().keys()) 
                    if field not in spacetime_list]
    project_object = {}
    for field in edu_level_list:
        project_object[field] = 1

    # Handle $group stage
    # ----------------------    
    group_object = {"_id": "null"}
    for field in edu_level_list:
        if field != "_id":
            group_object[field] = {"$sum" : ("$" + field)}

    cursor = \
    collection.aggregate([
    # Search only documents whose regions are in the selected
    # regions list
    {
        "$match": {"$or": match_list}
    }, 
    # Show only id and educational level fields
    {
        "$project": project_object
    },
    # Sum the total number of people that fall into each 
    # of the educational level fields across all the selected
    # regions
    {
        "$group": group_object
    },
    # Remove id field
    {
        "$project": {"_id": 0}
    }])

    quantity_data = None    
    for document in cursor:
        quantity_data = document
    quantity_chart = {'field': 'quantity', 'chart': 'bar', 
                      'data': quantity_data}

    # get total number of people counted in slice of dataset
    total_people = 0
    for key in quantity_data.keys():
        total_people += quantity_data[key]

    # calculate the number of people in each educational level
    # field as a percentage of the total number of people
    percentage_data = quantity_data.copy()
    for key in percentage_data.keys():
        percentage = percentage_data[key] / total_people
        num_decimals = 2
        while round(percentage, num_decimals) == 0:
            num_decimals += 1
        percentage_data[key] = round(percentage, num_decimals)
    percentage_chart = {'field': 'percentage', 'chart': 'pie', 
                        'data': percentage_data}

    jsonprint({'chart_list': [quantity_chart, percentage_chart]})

    return Response(response=json.dumps({'chart_list': [quantity_chart,
                                                        percentage_chart]}), 
                   status=200, 
                   mimetype='application/json')

def jsonprint(obj):
    """Prints Mongo document i.e Python object 
    """
    try:
        print(json.dumps(obj, sort_keys=True, indent=4))
    except TypeError:
        obj_copy = obj.copy()
        del obj_copy['_id']
        print(json.dumps(obj_copy, sort_keys=True, indent=4))

if __name__ == '__main__':
    main()
    # port = int(os.environ.get('PORT', 5000))
    # app.run(host='0.0.0.0', port=port)    