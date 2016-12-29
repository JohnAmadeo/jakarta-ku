from __future__ import print_function
from flask import Flask, render_template, request, redirect, make_response, Response
from pymongo import MongoClient
from fieldutils import get_field_stage
import os, json

app = Flask(__name__)
# Constants
DATABASE = MongoClient().get_database('jakartaku')

# Naming conventions
# ------------------------------------
# 1. Lists have names that end with '..._l'
#    e.g 'car_l', 'animal_l', 'winner_l'
# 2. 

def main():
    serve_education_charts_by_category(['koja', 'tebet'])

@app.route('/')
def serve_index():
    return render_template('index.html')

@app.route('/charts', methods=['POST'])
def serve_charts():
    body = request.get_json()
    comparison = body['comparison']
    region_list = body['region_list']
    category = body['category']

    if category == 'education':
        if comparison == "category": 
            return serve_education_charts_by_category(region_list)
        elif comparison == "region":
            return serve_education_charts_by_region(region_list)

def serve_education_charts_by_category(region_list):
    global DATABASE
    collection = DATABASE.get_collection('education')

    # Handle $match stage
    # ----------------------
    match_list = [{"Kecamatan": region} for region in region_list]

    # Handle $project stage
    # ----------------------
    # get list of all educational level fields
    edu_level_list = get_field_list(collection)

    project_object = {'_id': 1}
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

    quantity_data = []    
    for document in cursor:
        for field in document:
            quantity_data.append(
                {
                    'field': field,
                    'value': document[field],
                    "edu_level": get_field_stage('education', field) 
                }
            )
        # quantity_data = document

    quantity_chart = {'field': 'quantity', 'chart': 'bar', 
                      'data': sorted(quantity_data, 
                                     key=lambda x: x['edu_level'])}
    for data_unit in quantity_chart['data']:
        data_unit.pop('edu_level')
    # jsonprint(quantity_chart)

    # get total number of people counted in slice of dataset
    total_people = 0
    for data_unit in quantity_chart['data']:
        total_people += data_unit['value']

    # # calculate the number of people in each educational level
    # # field as a percentage of the total number of people
    percentage_data = [] 
    for data_unit in quantity_chart['data']:
        percentage = data_unit['value'] / total_people
        num_decimals = 2
        while round(percentage, num_decimals) == 0:
            num_decimals += 1
        percentage_data.append(
            {
                'field': data_unit['field'],
                'value': round(percentage, num_decimals)
            }
        )

    percentage_chart = {'field': 'percentage', 'chart': 'pie', 
                        'data': percentage_data}

    jsonprint({'chart_list': [quantity_chart, percentage_chart]})

    return Response(response=json.dumps({'chart_list': [quantity_chart,
                                                        percentage_chart]}), 
                   status=200, 
                   mimetype='application/json')

def serve_education_charts_by_region(region_list):
    global DATABASE
    collection = DATABASE.get_collection('education')
    chart_list = []

    # Handle $match stage
    # ----------------------
    match_list = [{"Kecamatan": region} for region in region_list]

    edu_level_list = get_field_list(collection)
    for edu_level in edu_level_list:
        group_object = {"_id": "null"}
        project_object = {"_id": 0}

        for region in region_list:
            group_object[region] = \
            {
                "$sum": {
                    "$cond" : {
                        "if": {"$eq": ["$Kecamatan", region]},
                        "then": "$" + edu_level, "else": 0
                    }
                }
            }
            project_object[region] = 1

        cursor = \
        collection.aggregate([{
            "$match": {"$or": match_list}
        }, 
        {
            "$project": {"_id" : 1, "Kecamatan" : 1, edu_level : 1}
        },
        {
            "$group": group_object
        },
        {
            "$project": project_object
        }])        

        field_data = None
        for result in cursor:
            field_data = result

        chart_list.append({
            "field": edu_level,
            "data": field_data,
            "edu_level": get_field_stage('education', edu_level) 
        })

    chart_list = sorted(chart_list, 
                        key=lambda chart: chart['edu_level'])
    for chart in chart_list:
        chart.pop('edu_level')
        jsonprint(chart)

    return Response(response=json.dumps({'chart_list': chart_list}), 
                   status=200, 
                   mimetype='application/json')       

def get_field_list(collection):
    """
    Get list of all non-spacetime fields in a standard 
    collection document
    """
    # list all space/time/id fields in document
    spacetimeid_list = ['Kecamatan', 'Kabupaten', 'Kelurahan', 
                        'Tahun', "_id"]
    # list all education level fields
    return [field for field in list(collection.find_one().keys()) 
            if field not in spacetimeid_list]

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