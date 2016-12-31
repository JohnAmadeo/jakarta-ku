from __future__ import print_function
from flask import Flask, render_template, request, redirect, make_response, Response
from pymongo import MongoClient
from fieldutils import get_field_stage, get_field_list
import os, json

DATABASE = MongoClient().get_database('jakartaku')

def main():
    return 0

def create_chart_list(comparison, region_list, category):
    if category == 'education' and comparison == "field": 
            return serve_education_charts_by_field(region_list)
    elif category == 'education' and comparison == "region":
            return serve_education_charts_by_region(region_list)
    elif category == 'occupation' and comparison == "field":
            return serve_occupation_charts_by_field(region_list)

def create_education_charts_by_field(region_list):
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
    for edu_level in edu_level_list:
        project_object[edu_level] = 1

    # Handle $group stage
    # ----------------------    
    group_object = {"_id": "null"}
    for edu_level in edu_level_list:
        group_object[edu_level] = {"$sum" : ("$" + edu_level)}

    cursor = \
    collection.aggregate([
        # Search only documents whose regions are in the selected
        # regions list
        {"$match": {"$or": match_list} }, 
        # Show only id and educational level fields
        {"$project": project_object },
        # Sum the total number of people that fall into each 
        # of the educational level fields across all the selected
        # regions
        {"$group": group_object },
        # Remove id field
        {"$project": {"_id": 0} }
    ])

    quantity_data = []    
    for document in cursor:
        jsonprint(document)
        for field in document:
            quantity_data.append(
                [
                    field,
                    document[field],
                    {"edu_level": get_field_stage('education', field)} 
                ]
            )

    quantity_chart = {'label': 'quantity', 'chart_type': 'bar',
                      'xtitle': 'Jumlah Orang',  
                      'ytitle': 'Tingkat Pendidikan',
                      'data': sorted(quantity_data, 
                                     key=lambda x: x[2]['edu_level'])}
    for data_unit in quantity_chart['data']:
        data_unit.pop()
    # jsonprint(quantity_chart)

    # get total number of people counted in slice of dataset
    total_people = 0
    for data_unit in quantity_chart['data']:
        total_people += data_unit[1]

    # # calculate the number of people in each educational level
    # # field as a percentage of the total number of people
    percentage_data = [] 
    for data_unit in quantity_chart['data']:
        percentage = data_unit[1] / total_people
        num_decimals = 2
        while round(percentage, num_decimals) == 0:
            num_decimals += 1
        percentage_data.append([data_unit[0], 
                                round(percentage, num_decimals)])

    percentage_chart = {'label': 'percentage', 'chart_type': 'pie',
                        'xtitle': 'Tingkat Pendidikan', 
                        'ytitle': 'Persentase Orang', 
                        'data': percentage_data}

    chart_list = {'chart_list': [quantity_chart, percentage_chart]}
    jsonprint(chart_list)

    return chart_list

def create_education_charts_by_region(region_list):
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
        collection.aggregate([
            {"$match": {"$or": match_list} }, 
            {
                "$project": {"_id" : 1, "Kecamatan" : 1, edu_level : 1}
            },
            {"$group": group_object },
            {"$project": project_object }
        ])        

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
        # jsonprint(chart)

    chart_list = {'chart_list': chart_list}

    return chart_list      

def create_occupation_charts_by_field(region_list):
    global DATABASE
    collection = DATABASE.get_collection('occupation')

    # $match
    match_list = [{"Kecamatan": region} for region in region_list]

    # $project
    occupation_list = get_field_list(collection)
    project_object = {'_id': 1}
    for occupation in occupation_list:
        project_object[occupation] = 1

    # $group
    group_object = {'_id': 'null'}
    for occupation in occupation_list:
        group_object[occupation] = {'$sum' : ('$' + occupation)}

    cursor = \
    collection.aggregate([
        {'$match': {'$or': match_list} },
        {'$project': project_object},
        {'$group': group_object},
        {'$project': {'_id': 0} }
    ])

    data = None
    for document in cursor:
        data = document

    chart_data = [[occupation, data[occupation]] 
                  for occupation in list(data.keys())
                  if occupation != "Lainnya" and data[occupation] != 0]

    top10_data = sorted(chart_data, key=lambda x:x[1], reverse=True)[:10]
    bottom10_data = sorted(chart_data, key=lambda x:x[1])[:10]

    top10_chart = {'label': 'a', 'chart_type': 'bar',
                   'xtitle': 'Jumlah Orang', 'ytitle': 'Pekerjaan',
                   'data': top10_data}

    bottom10_chart = {'label': 'a', 'chart_type': 'bar',
                      'xtitle': 'Jumlah Orang', 'ytitle': 'Pekerjaan',
                      'data': bottom10_data}

    chart_list = {'chart_list': [top10_chart, bottom10_chart]}

    jsonprint(chart_list)
    return chart_list   

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