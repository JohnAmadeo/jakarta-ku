from __future__ import print_function
from flask import Flask, render_template, request, redirect, make_response, Response
from pymongo import MongoClient
from fieldutils import get_field_display_order, get_field_list
import os, json

DATABASE = MongoClient().get_database('jakartaku')

def main():
    chart_list = create_demographics_chart(['koja', 'tebet'], 'region')

def create_chart_list(comparison, region_list, category):
    global DATABASE
    if category == 'education':
        create_education_chart(region_list, comparison)
    elif category == 'occupation':
        create_occupation_chart(region_list, comparison)
    elif category == 'marriage':
        create_marriage_chart(region_list, comparison)
    elif category == 'religion':
        create_religion_chart(region_list, comparison)
    elif category == 'demographics':
        create_demographics_chart(region_list, comparison)

def create_religion_chart(region_list, comparison):
    if comparison == 'field':
        qty_chart = create_chart_by_field_qty(region_list, 'religion')
        chart_total = get_chart_total(qty_chart, 'field')
        pct_chart = create_chart_by_field_pct(qty_chart, chart_total)

        qty_chart['xtitle'] = 'Agama'
        qty_chart['ytitle'] = 'Jumlah Orang'
        pct_chart['xtitle'] = 'Agama'
        pct_chart['ytitle'] = 'Persentase Orang'
        chart_list = {'chart_list': [qty_chart, pct_chart]}

        jsonprint(chart_list)
        return chart_list

    elif comparison == 'region':
        qty_list = create_chart_by_region_qty(region_list, 'religion')
        chart_total = get_chart_total(qty_list, 'region')
        pct_list = create_chart_by_region_pct(qty_list, chart_total)

        for index, chart in enumerate(qty_list):
            qty_list[index]['xtitle'] = 'Kecamatan'
            qty_list[index]['ytitle'] = 'Jumlah Orang'
            pct_list[index]['xtitle'] = 'Kecamatan'
            pct_list[index]['ytitle'] = 'Persentase Orang'

        chart_list = {'chart_list': qty_list + pct_list}

        jsonprint(chart_list)
        return chart_list

def create_education_chart(region_list, comparison):
    if comparison == 'field':
        qty_chart = create_chart_by_field_qty(region_list, 'education')
        chart_total = get_chart_total(qty_chart, 'field')
        pct_chart = create_chart_by_field_pct(qty_chart, chart_total)

        qty_chart['xtitle'] = 'Tingkat Pendidikan'
        qty_chart['ytitle'] = 'Jumlah Orang'
        pct_chart['xtitle'] = 'Tingkat Pendidikan'
        pct_chart['ytitle'] = 'Persentase Orang'
        chart_list = {'chart_list': [qty_chart, pct_chart]}

        jsonprint(chart_list)
        return chart_list

    elif comparison == 'region':
        qty_list = create_chart_by_region_qty(region_list, 'education')
        chart_total = get_chart_total(qty_list, 'region')
        pct_list = create_chart_by_region_pct(qty_list, chart_total)

        for index, chart in enumerate(qty_list):
            qty_list[index]['xtitle'] = 'Kecamatan'
            qty_list[index]['ytitle'] = 'Jumlah Orang'
            pct_list[index]['xtitle'] = 'Kecamatan'
            pct_list[index]['ytitle'] = 'Persentase Orang'

        chart_list = {'chart_list': qty_list + pct_list}

        jsonprint(chart_list)
        return chart_list       

def create_marriage_chart(region_list, comparison):
    if comparison == 'field':
        qty_chart = create_chart_by_field_qty(region_list, 'marriage')
        chart_total = get_chart_total(qty_chart, 'field')
        pct_chart = create_chart_by_field_pct(qty_chart, chart_total)

        qty_chart['xtitle'] = 'Status Pernikahan'
        qty_chart['ytitle'] = 'Jumlah Orang'
        pct_chart['xtitle'] = 'Tingkat Pendidikan'
        pct_chart['ytitle'] = 'Persentase Orang'
        chart_list = {'chart_list': [qty_chart, pct_chart]}

        jsonprint(chart_list)
        return chart_list

    elif comparison == 'region':
        qty_list = create_chart_by_region_qty(region_list, 'marriage')
        chart_total = get_chart_total(qty_list, 'region')
        pct_list = create_chart_by_region_pct(qty_list, chart_total)

        for index, chart in enumerate(qty_list):
            qty_list[index]['xtitle'] = 'Kecamatan'
            qty_list[index]['ytitle'] = 'Jumlah Orang'
            pct_list[index]['xtitle'] = 'Kecamatan'
            pct_list[index]['ytitle'] = 'Persentase Orang'

        chart_list = {'chart_list': qty_list + pct_list}

        jsonprint(chart_list)
        return chart_list     

def create_occupation_chart(region_list, comparison):
    if comparison == 'field':
        qty_chart = create_chart_by_field_qty(region_list, 'occupation')
        
        top10_data = sorted(qty_chart['data'], 
                            key=lambda x:x[1], reverse=True)[:10]
        top10_chart = qty_chart.copy()
        top10_chart['data'] = top10_data

        bottom10_data = [data_unit for data_unit in qty_chart['data'] 
                         if data_unit[1] != 0]
        bottom10_data = sorted(bottom10_data,
                               key=lambda x:x[1])[:10]
        bottom10_chart = qty_chart.copy()
        bottom10_chart['data'] = bottom10_data
        bottom10_chart['warning'] = 'Pekerjaan yang dipegang oleh 0 orang di semua kecamatan yang terseleksi tidak akan ditampilkan'

        chart_list = {'chart_list': [top10_chart, bottom10_chart]}

        jsonprint(chart_list)
        return chart_list 
    elif comparison == 'region': 
        qty_list = create_chart_by_region_qty(region_list, 'occupation')
        chart_total = get_chart_total(qty_list, 'region')
        for chart in qty_list[:]:
            occupation_count_list = [data_unit[1] 
                                     for data_unit in chart['data']]
            if all_x(occupation_count_list, 0):
                qty_list.remove(chart) 

        for index, chart in enumerate(qty_list):
            qty_list[index]['xtitle'] = 'Kecamatan'
            qty_list[index]['ytitle'] = 'Jumlah Orang'

        chart_list = {'chart_list': qty_list}

        jsonprint(chart_list)
        return chart_list  

def create_demographics_chart(region_list, comparison):
    if comparison == 'field':
        qty_chart = create_chart_by_field_qty(region_list, 'demographics')
        qty_chart['data'] = qty_chart['data'][2:]
        chart_total = get_chart_total(qty_chart, 'field')
        pct_chart = create_chart_by_field_pct(qty_chart, chart_total)

        qty_chart['xtitle'] = 'Demografi'
        qty_chart['ytitle'] = 'Jumlah Orang'
        pct_chart['xtitle'] = 'Agama'
        pct_chart['ytitle'] = 'Persentase Orang'
        chart_list = {'chart_list': [qty_chart, pct_chart]}

        jsonprint(chart_list)
        return chart_list
    elif comparison == 'region':
        qty_list = create_chart_by_region_qty(region_list, 'demographics')
        
        area_chart = qty_list[0]
        density_chart = qty_list[1]
        area_chart['xtitle'] = 'Kecamatan'
        area_chart['ytitle'] = 'Km^2'
        density_chart['xtitle'] = 'Kecamatan'
        density_chart['ytitle'] = 'Orang/Km^2'


        qty_list = qty_list[2:]
        chart_total = get_chart_total(qty_list, 'region')
        pct_list = create_chart_by_region_pct(qty_list, chart_total)

        for index, chart in enumerate(qty_list):
            qty_list[index]['xtitle'] = 'Kecamatan'
            qty_list[index]['ytitle'] = 'Jumlah Orang'
            pct_list[index]['xtitle'] = 'Kecamatan'
            pct_list[index]['ytitle'] = 'Persentase Orang'

        chart_list = {
            'chart_list': [area_chart, density_chart] + qty_list + pct_list
        }

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
        data = sorted(data, key=lambda x: x[2])
    
    chart = {
        'label': 'quantity',
        'data': [[data_unit[0], data_unit[1]] for data_unit in data],
        'chart_type': 'bar'
    }           

    return chart

def create_chart_by_field_pct(chart, chart_total):
    data = [[data_unit[0], round_num(data_unit[1], chart_total)] 
            for data_unit in chart['data']]
    chart = {
        'label': 'percentage', 
        'data': data,
        'chart_type': 'pie'
    }
    return chart

def create_chart_by_region_qty(region_list, category):
    global DATABASE
    collection = DATABASE.get_collection(category)
    qty_list = []

    match_list = [{'Kecamatan': region} for region in region_list]

    field_list = get_field_list(collection)
    for field in field_list:
        group_object = {'_id': 'null'}
        project_object = {'_id': 0}

        for region in region_list:
            group_object[region] = \
            {
                '$sum': {
                    '$cond' : {
                        'if': {'$eq': ['$Kecamatan', region]},
                        'then': '$' + field, 'else': 0
                    }
                }
            }
            project_object[region] = 1

        cursor = \
        collection.aggregate([
            {'$match': {'$or': match_list} }, 
            {'$project': {'_id' : 1, 'Kecamatan' : 1, field : 1} },
            {'$group': group_object },
            {'$project': project_object }
        ])  

        data = None
        for result in cursor:
            data = result

        qty_list.append({
            'label': field,
            'data': [[key, data[key]] for key in list(data.keys())],
            'display_order': get_field_display_order(field),
            'chart_type': 'bar' 
        })

    qty_list = sorted(qty_list, 
                           key=lambda chart: chart['display_order'])
    for chart in qty_list:
        chart.pop('display_order')

    return qty_list

def create_chart_by_region_pct(chart_list, chart_total):
    pct_list = []
    for chart in chart_list:
        pct_list.append({
            'label': chart['label'],
            'data': [[data_unit[0], 
                      round_num(data_unit[1], chart_total[data_unit[0]])]
                     for data_unit in chart['data']],
            'chart_type': 'bar'    
        })

    return pct_list


def get_chart_total(chart_obj, comparison):
    """
    If 'region' comparison, list of charts is passed in
    If 'field' comparison, chart is passed in
    """
    if comparison == 'field':
        chart = chart_obj
        return sum([data_unit[1] for data_unit in chart['data']])
    elif comparison == 'region':
        population_dict = {}
        for chart in chart_obj:
            for data_unit in chart['data']:
                if data_unit[0] in population_dict.keys():
                    population_dict[data_unit[0]] += data_unit[1]
                else:
                    population_dict[data_unit[0]] = data_unit[1]

        return population_dict

def round_num(num, total):
    if num == 0: return 0

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
