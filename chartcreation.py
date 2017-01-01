from __future__ import print_function
from flask import Flask, render_template, request, redirect, make_response, Response
from pymongo import MongoClient
from fieldutils import get_field_display_order, get_field_list
import os, json

DATABASE = MongoClient().get_database('jakartaku')

def main():
    create_chart_list('region', ['koja', 'tebet'], 'education')
    return 0

def create_chart_list(comparison, region_list, category):
    global DATABASE
    if category == 'education':
        collection = DATABASE.get_collection('education')
        if comparison == 'field': 
            return create_education_by_field(region_list, collection)
        elif comparison == 'region':
            return create_education_by_region(region_list, collection)
    elif category == 'occupation':
        collection = DATABASE.get_collection('occupation')
        if comparison == 'field':
            return create_occupation_by_field(region_list, collection)
        elif comparison == 'region':
            return create_occupation_by_region(region_list, collection)
    elif category == 'marriage':
        collection = DATABASE.get_collection('marriage')
        if comparison == 'field':
            return create_marriage_by_field(region_list, collection)
        elif comparison == 'region':
            return create_marriage_by_region(region_list, collection)

def create_education_by_field(region_list, collection):
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
        # jsonprint(document)
        for field in document:
            quantity_data.append(
                [
                    field,
                    document[field],
                    {"edu_level": 
                        get_field_display_order('education', field)} 
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

def create_education_by_region(region_list, collection):
    # Get total people for each selected region
    population_dict = dict()
    match_list = [{"Kecamatan": region} for region in region_list]
    occupation_list = get_field_list(collection)
    group_object = {'_id': '$Kecamatan'}
    for occupation in occupation_list:
        group_object[occupation] = {"$sum": '$' + occupation}

    cursor = \
    collection.aggregate([
        {'$match': {'$or': match_list} },
        {'$group': group_object}
    ])

    for document in cursor:
        region = document.pop('_id')
        population_dict[region] = sum(list(document.values()))

    # jsonprint(population_dict)

    # Get chart_list w/ absolute numbers
    quantity_list = []
    percentage_list = []
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
            {'$match': {"$or": match_list} }, 
            {'$project': {"_id" : 1, "Kecamatan" : 1, edu_level : 1} },
            {'$group': group_object },
            {'$project': project_object }
        ])        

        field_data = None
        for result in cursor:
            field_data = result

        quantity_list.append({
            "chart_type": 'bar', "label": edu_level,
            "xtitle": 'Kecamatan', "ytitle": 'Jumlah Orang',
            "data": [[region, field_data[region]] 
                     for region in list(field_data.keys())],
            "edu_level": 
                get_field_display_order('education', edu_level) 
        })

        percentage_data = []
        for region in list(field_data.keys()):
            num_decimals = 2
            percentage = field_data[region] / population_dict[region]
            while round(percentage, num_decimals) == 0:
                num_decimals += 1
            percentage_data.append([region, 
                                    round(percentage, num_decimals)])

        percentage_list.append({
            "chart_type": 'bar', "label": edu_level,
            "xtitle": 'Kecamatan', "ytitle": 'Jumlah Orang',
            "data": percentage_data,
            "edu_level": 
                get_field_display_order('education', edu_level) 
        })

    quantity_list = sorted(quantity_list, 
                           key=lambda chart: chart['edu_level'])
    percentage_list = sorted(percentage_list, 
                             key=lambda chart: chart['edu_level'])

    for index, data in enumerate(quantity_list):
        quantity_list[index].pop('edu_level')
        percentage_list[index].pop('edu_level')  

    chart_list = \
    {
        'chart_list': {
            'quantity_list': quantity_list,
            'percentage_list': percentage_list
        }
    }      

    jsonprint(chart_list)
    return chart_list      

def create_occupation_by_field(region_list, collection):
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

def create_occupation_by_region(region_list, collection):
    chart_list = []

    # Handle $match stage
    # ----------------------
    match_list = [{"Kecamatan": region} for region in region_list]

    occupation_list = get_field_list(collection)
    for occupation in occupation_list:
        group_object = {"_id": "null"}
        project_object = {"_id": 0}

        for region in region_list:
            group_object[region] = \
            {
                "$sum": {
                    "$cond" : {
                        "if": {"$eq": ["$Kecamatan", region]},
                        "then": "$" + occupation, "else": 0
                    }
                }
            }
            project_object[region] = 1

        cursor = \
        collection.aggregate([
            {"$match": {"$or": match_list} }, 
            {
                "$project": {"_id" : 1, "Kecamatan" : 1, occupation : 1}
            },
            {"$group": group_object },
            {"$project": project_object }
        ])    

        field_data = None
        for result in cursor:
            field_data = result

        # jsonprint(field_data)

        if not all_x(list(field_data.values()), 0):
            chart_list.append({
                "chart_type": 'bar',
                "xtitle": 'Kecamatan',
                "ytitle": 'Jumlah Orang',
                "label": occupation,
                "data": [[key, field_data[key]] 
                         for key in list(field_data.keys())],
                "occupation_stage": 
                    get_field_display_order('occupation', occupation) 
            })

    chart_list = sorted(chart_list, 
                        key=lambda chart: chart['occupation_stage'])
    for chart in chart_list:
        chart.pop('occupation_stage')

    chart_list = {'chart_list': chart_list, 
                  'warning': 'Pekerjaan yang dipegang oleh 0 orang ' + 
                             'di semua kecamatan yang terseleksi ' +
                             'tidak akan ditampilkan'}

    jsonprint(chart_list)
    return chart_list      

def all_x(elem_list, check_elem):
    for elem in elem_list:
        if elem != check_elem:
            return False
    return True

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
