from __future__ import print_function
from flask import Flask, render_template, request, redirect, make_response, Response
from pymongo import MongoClient
from fieldutils import get_field_display_order, get_field_list
import os, json

DATABASE = MongoClient().get_database('jakartaku')

def main():
    create_chart_list('field', ['koja', 'tebet'], 'religion')

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
    elif category == 'religion':
        if comparison == 'field':
            qty_chart = create_chart_by_field_qty(region_list, category)
            chart_population = get_chart_population(qty_chart, 'field')
            pct_chart = create_chart_by_field_pct(qty_chart, chart_population)
            # add_axes([qty_chart, pct_chart])
            chart_list = {'chart_list': [qty_chart, pct_chart]}
            jsonprint(chart_list)
            return chart_list

def create_chart_by_field_qty(region_list, category):
    global DATABASE
    collection = DATABASE.get_collection(category)

    # filter out all documents whose region field is not
    # in the selected region list
    match_list = [{'Kecamatan': region} for region in region_list]

    # get list of all category fields
    field_list = get_field_list(collection)

    project_object = {'_id': 1}
    for field in field_list:
        project_object[field] = 1

    group_object = {'_id': 'null'}
    for field in field_list:
        group_object[field] = {'$sum': ('$' + field)}

    cursor = \
    collection.aggregate([
        {'$match': {'$or': match_list} }, 
        {'$project': project_object },
        {'$group': group_object },
        {'$project': {'_id': 0} }        
    ])

    data = None
    for document in cursor:
        data = [[key, document[key], get_field_display_order(key)]
                for key in list(document.keys())]
        jsonprint(data)
        data = sorted(data, key=lambda x: x[2])
    
    chart = {
        'label': 'quantity'
        'data': [[data_unit[0], data_unit[1]] for data_unit in data]
    }           

    return chart

def get_chart_population(chart, comparison):
    if comparison == 'field':
        return sum([data_unit[1] for data_unit in chart['data']])

def create_chart_by_field_pct(chart, total_people):
    data = [[data_unit[0], round_num(data_unit[1], total_people)] 
            for data_unit in chart['data']]
    chart = {'label': 'percentage', 'data': data}
    return chart

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
                    {"edu_level": get_field_display_order(field)} 
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
    population_dict = get_dataset_population(region_list, collection)    

    # Get regional comparison quantity and percentage-wise
    # Comment more later
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
            "edu_level": get_field_display_order(edu_level) 
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
            "edu_level": get_field_display_order(edu_level) 
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

    # jsonprint(chart_list)
    return chart_list   

def create_occupation_by_region(region_list, collection):
    # Comment later
    quantity_list = []

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
            quantity_list.append({
                "chart_type": 'bar', "label": occupation,
                "xtitle": 'Kecamatan', "ytitle": 'Jumlah Orang',
                "data": [[key, field_data[key]] 
                         for key in list(field_data.keys())],
                "occupation_stage": get_field_display_order(occupation) 
            })


    # quantity_list = sorted(quantity_list, key=lambda chart: chart['occupation_stage'])
    quantity_list = sorted(quantity_list, 
                           key=lambda chart: chart['occupation_stage'])

    # jsonprint(quantity_list)

    for index, data in enumerate(quantity_list):
        quantity_list[index].pop('occupation_stage')

    chart_list = {
        'chart_list':  quantity_list,
        'warning': 'Pekerjaan yang dipegang oleh 0 orang di semua ' + 
                   'kecamatan yang terseleksi tidak akan ditampilkan'
    }

    jsonprint(chart_list)
    return chart_list      

def create_marriage_by_field(region_list, collection):
    # Handle $match stage
    match_list = [{"Kecamatan": region} for region in region_list]

    # Handle $project stage
    # get list of all relationship status fields
    status_list = get_field_list(collection)
    project_object = {'_id': 1}
    for status in status_list:
        project_object[status] = 1

    # Handle $group stage
    # sum up total number of people in each relationship status field 
    group_object = {"_id": "null"}
    for status in status_list:
        group_object[status] = {"$sum" : ("$" + status) }

    cursor = \
    collection.aggregate([
        {"$match": {"$or": match_list} }, 
        {"$project": project_object },
        {"$group": group_object },
        {"$project": {"_id": 0} }
    ])

    data = None
    for document in cursor:
        data = [[key, document[key], get_field_display_order(key)] 
                for key in list(document.keys())]
        data = sorted(data, key=lambda x: x[2])

    quantity_chart = {
        'label': 'quantity', 'chart_type': 'bar',
        'xtitle': 'Jumlah Orang', 'ytitle': 'Status Pernikahan',
        'data': [[data_unit[0], data_unit[1]] for data_unit in data]
    }

    total_people = sum([data_unit[1] for data_unit in data])

    # # calculate the number of people in each educational level
    # # field as a percentage of the total number of people
    data = [[data_unit[0], round_num(data_unit[1], total_people)] 
            for data_unit in quantity_chart['data']]

    percentage_chart = {
        'label': 'percentage', 'chart_type': 'pie',
        'xtitle': 'Tingkat Pendidikan', 'ytitle': 'Persentase Orang',
        'data': data
    } 

    chart_list = {'chart_list': [quantity_chart, percentage_chart]}
    jsonprint(chart_list)

    return chart_list    

def create_marriage_by_region(region_list, collection):
    # Comment later
    quantity_list = []
    percentage_list = []
    total_people = get_dataset_population(region_list, collection)

    # Handle $match stage
    # ----------------------
    match_list = [{"Kecamatan": region} for region in region_list]

    status_list = get_field_list(collection)
    for status in status_list:
        group_object = {'_id': 'null'}
        project_object = {'_id': 0}

        for region in region_list:
            group_object[region] = \
            {
                '$sum': {
                    '$cond' : {
                        'if': {'$eq': ['$Kecamatan', region]},
                        'then': '$' + status, 'else': 0
                    }
                }
            }
            project_object[region] = 1

        cursor = \
        collection.aggregate([
            {'$match': {'$or': match_list} }, 
            {'$project': {'_id' : 1, 'Kecamatan' : 1, status : 1} },
            {'$group': group_object },
            {'$project': project_object }
        ])    

        field_data = None
        for result in cursor:
            field_data = result

        quantity_list.append({
            "chart_type": 'bar', "label": status,
            "xtitle": 'Kecamatan', "ytitle": 'Jumlah Orang',
            "data": [[key, field_data[key]] 
                     for key in list(field_data.keys())],
            "status_stage": get_field_display_order(status) 
        })

        percentage_list.append({
            "chart_type": 'bar', "label": status,
            "xtitle": 'Kecamatan', "ytitle": 'Jumlah Orang',
            "data": [[key, round_num(field_data[key], total_people[key])] 
                     for key in list(field_data.keys())],
            "status_stage": get_field_display_order(status) 
        })

    quantity_list = sorted(quantity_list, 
                           key=lambda chart: chart['status_stage'])
    percentage_list = sorted(percentage_list, 
                           key=lambda chart: chart['status_stage'])

    for index, data in enumerate(quantity_list):
        quantity_list[index].pop('status_stage')
        percentage_list[index].pop('status_stage')

    chart_list = {
        'chart_list': {
            'quantity_list': quantity_list,
            'percentage_list': percentage_list
        }
    }

    jsonprint(chart_list)
    return chart_list  

def get_dataset_population(region_list, collection):
    # Get total people for each selected region
    population_dict = dict()
    match_list = [{"Kecamatan": region} for region in region_list]
    field_list = get_field_list(collection)
    group_object = {'_id': '$Kecamatan'}
    for field in field_list:
        group_object[field] = {"$sum": '$' + field}

    cursor = \
    collection.aggregate([
        {'$match': {'$or': match_list} },
        {'$group': group_object}
    ])

    for document in cursor:
        region = document.pop('_id')
        population_dict[region] = sum(list(document.values()))  

    # jsonprint(population_dict)
    return population_dict

def round_num(num, total):
    percentage = num / total
    decimals = 2
    while round(percentage, decimals) == 0:
        decimals += 1
    return round(percentage, decimals)

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
