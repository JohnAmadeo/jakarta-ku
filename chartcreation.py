from __future__ import print_function
from flask import Flask, render_template, request, redirect, make_response, Response
from pymongo import MongoClient
from fieldutils import get_field_display_order, get_field_list
import os, json

DATABASE = MongoClient().get_database('jakartaku')

def main():
    chart_list = create_marriage_chart(['koja', 'tebet'], 'region')

# Props 
#     chartType (string)
#     'bar' or 'doughnut'
#     chartName (string)
#     'Tingkat Pendidikan antar Kecamatan'
#     dataFields (object)
#     {
#       values: [1,2,3],
#       labels: ['a','b','c']
#     }

#     dataOptions (object)
#     {
#       fieldAxis: 'Pekerjaan'
#       measureAxis: 'Jumlah Orang'
#       tooltipStringFormat: //func?
#     }

def create_chart_list(comparison, region_list, category):
    """
    Create a list of charts to display 

    Args
    comparison: compare data in the category by field or by region
    region_list: list of regions whose data will be examined
    category: category of the dataset examined

    Returns
    chart_list: list of charts i.e objects to display         
    """
    if category == 'education':
        return create_education_chart(region_list, comparison)
    elif category == 'occupation':
        return create_occupation_chart(region_list, comparison)
    elif category == 'marriage':
        return create_marriage_chart(region_list, comparison)
    elif category == 'religion':
        return create_religion_chart(region_list, comparison)
    elif category == 'demographics':
        return create_demographics_chart(region_list, comparison)

def create_religion_chart(region_list, comparison):
    """
    Create list of charts to display data from the religion category 

    Args
    region_list: list of regions whose data will be examined
    comparison: compare data in the category by field or by region

    Returns
    chart_list: list of charts i.e objects to display          
    """
    if comparison == 'field':
        qty_data = create_data_by_field_qty(region_list, 'religion')
        qty_chart = {
            'chartType': 'bar',
            'chartName': 'Agama menurut Jumlah Penganut',
            'dataFields': qty_data,
            'dataOptions': {
                'fieldAxis': 'Agama',
                'measureAxis': 'Jumlah Orang',
                'tooltipStringFormat': ['_', ' ', 'Orang']
            }
        }

        dataset_total = sum(qty_data['values'])
        pct_data = create_data_by_field_pct(qty_data, dataset_total)
        pct_chart = {
            'chartType': 'doughnut',
            'chartName': 'Agama menurut Persentase Penganut',
            'dataFields': pct_data,
            'dataOptions': {
                'fieldAxis': 'Agama',
                'measureAxis': 'Persentase Orang',
                'tooltipStringFormat': ['_', '%']
            }
        }

        chart_list = {'chartList': [qty_chart, pct_chart]}
        jsonprint(chart_list)
        return chart_list

    elif comparison == 'region':
        qty_list = create_data_by_region_qty(region_list, 'religion')

        dataset_total_list = get_dataset_total_list(qty_list)
        pct_list = create_data_by_region_pct(qty_list, 
                                             dataset_total_list)

        chart_list = {'chartList': []}
        for index, chart in enumerate(qty_list):
            pct_list[index]['dataOptions'] = {
                'tooltipStringFormat': ['_', '%'],
                'fieldAxis': 'Agama',
                'measureAxis': 'Persentase Orang'
            }
            qty_list[index]['dataOptions'] = {
                'tooltipStringFormat': ['_', ' ', 'Orang'],
                'fieldAxis': 'Agama',
                'measureAxis': 'Jumlah Orang'
            }

            field = pct_list[index]['chartName']
            pct_list[index]['chartName'] = \
                'Persentase Orang Penganut Agama ' + field + \
                ' menurut Kecamatan'
            qty_list[index]['chartName'] = \
                'Jumlah Orang Penganut Agama ' + field + \
                ' menurut Kecamatan'

            chart_list['chartList'].append(pct_list[index])
            chart_list['chartList'].append(qty_list[index])

        jsonprint(chart_list)
        return chart_list

def create_education_chart(region_list, comparison):
    """
    Create list of charts to display data from the education category 

    Args
    region_list: list of regions whose data will be examined
    comparison: compare data in the category by field or by region

    Returns
    chart_list: list of charts i.e objects to display          
    """
    if comparison == 'field':
        qty_data = create_data_by_field_qty(region_list, 'education')
        qty_chart = {
            'chartType': 'bar',
            'chartName': 'Status Pendidikan menurut Jumlah Orang',
            'dataFields': qty_data,
            'dataOptions': {
                'fieldAxis': 'Status Pendidikan',
                'measureAxis': 'Jumlah Orang',
                'tooltipStringFormat': ['_', ' ', 'Orang']
            }
        }

        dataset_total = sum(qty_data['values'])
        pct_data = create_data_by_field_pct(qty_data, dataset_total)
        pct_chart = {
            'chartType': 'doughnut',
            'chartName': 'Status Pendidikan menurut Persentase Orang',
            'dataFields': pct_data,
            'dataOptions': {
                'fieldAxis': 'Status Pendidikan',
                'measureAxis': 'Persentase Orang',
                'tooltipStringFormat': ['_', '%']
            }            
        }

        chart_list = {'chartList': [qty_chart, pct_chart]}
        jsonprint(chart_list)
        return chart_list

    elif comparison == 'region':
        qty_list = create_data_by_region_qty(region_list, 'education')

        dataset_total_list = get_dataset_total_list(qty_list)
        pct_list = create_data_by_region_pct(qty_list, 
                                             dataset_total_list)

        chart_list = {'chartList': []}
        for index, chart in enumerate(qty_list):
            pct_list[index]['dataOptions'] = {
                'tooltipStringFormat': ['_', '%'],
                'fieldAxis': 'Status Pendidikan',
                'measureAxis': 'Persentase Orang'
            }
            qty_list[index]['dataOptions'] = {
                'tooltipStringFormat': ['_', ' ', 'Orang'],
                'fieldAxis': 'Status Pendidikan',
                'measureAxis': 'Jumlah Orang'
            }

            field = pct_list[index]['chartName']
            pct_list[index]['chartName'] = \
                "Persentase Orang dengan Status Pendidikan '" + field + \
                "' menurut Kecamatan"
            qty_list[index]['chartName'] = \
                "Jumlah Orang dengan Status Pendidikan '" + \
                field + "' menurut Kecamatan"

            chart_list['chartList'].append(pct_list[index])
            chart_list['chartList'].append(qty_list[index])

        jsonprint(chart_list)
        return chart_list       

def create_marriage_chart(region_list, comparison):
    """
    Create list of charts to display data from the marriage category 

    Args
    region_list: list of regions whose data will be examined
    comparison: compare data in the category by field or by region

    Returns
    chart_list: list of charts i.e objects to display          
    """
    if comparison == 'field':
        qty_data = create_data_by_field_qty(region_list, 'marriage')
        qty_chart = {
            'chartType': 'bar',
            'chartName': 'Status Pernikahan menurut Jumlah Orang',
            'dataFields': qty_data,
            'dataOptions': {
                'fieldAxis': 'Status Pernikahan',
                'measureAxis': 'Jumlah Orang',
                'tooltipStringFormat': ['_', ' ', 'Orang']
            }
        }

        dataset_total = sum(qty_data['values'])
        pct_data = create_data_by_field_pct(qty_data, dataset_total)
        pct_chart = {
            'chartType': 'doughnut',
            'chartName': 'Status Pernikahan menurut Persentase Orang',
            'dataFields': pct_data,
            'dataOptions': {
                'fieldAxis': 'Status Pernikahan',
                'measureAxis': 'Persentase Orang',
                'tooltipStringFormat': ['_', '%']
            }
        }

        chart_list = {'chartList': [qty_chart, pct_chart]}
        jsonprint(chart_list)
        return chart_list

    elif comparison == 'region':
        qty_list = create_data_by_region_qty(region_list, 'marriage')
        dataset_total_list = get_dataset_total_list(qty_list)
        pct_list = create_data_by_region_pct(qty_list,
                                             dataset_total_list)

        chart_list = {'chartList': []}
        for index, chart in enumerate(qty_list):
            pct_list[index]['dataOptions'] = {
                'tooltipStringFormat': ['_', '%'],
                'fieldAxis': 'Status Pernikahan',
                'measureAxis': 'Persentase Orang'
            }        
            qty_list[index]['dataOptions'] = {
                'tooltipStringFormat': ['_', ' ', 'Orang'],
                'fieldAxis': 'Status Pernikahan',
                'measureAxis': 'Jumlah Orang'
            }

            field = pct_list[index]['chartName']
            if field == 'Kawin':
                pct_list[index]['chartName'] = \
                    'Persentase Warga yang sudah ' + field + \
                    ' menurut Kecamatan'
                qty_list[index]['chartName'] = \
                    'Jumlah Warga yang sudah ' + field + \
                    ' menurut Kecamatan'
            else:
                pct_list[index]['chartName'] = \
                    'Persentase Warga yang ' + field + \
                    ' menurut Kecamatan'
                qty_list[index]['chartName'] = \
                    'Jumlah Warga yang ' + field + \
                    ' menurut Kecamatan'                

            chart_list['chartList'].append(pct_list[index])
            chart_list['chartList'].append(qty_list[index])

        jsonprint(chart_list)
        return chart_list     

def create_occupation_chart(region_list, comparison):
    """
    Create list of charts to display data from the occupation category 

    Args
    region_list: list of regions whose data will be examined
    comparison: compare data in the category by field or by region

    Returns
    chart_list: list of charts i.e objects to display          
    """
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
    """
    Create list of charts to display data from the demographics category 

    Args
    region_list: list of regions whose data will be examined
    comparison: compare data in the category by field or by region

    Returns
    chart_list: list of charts i.e objects to display          
    """
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

def create_data_by_field_qty(region_list, category):
    """
    Args
    region_list: list of regions whose data will be examined
    category: category of the dataset

    Returns
    chart: a chart displaying 
    """
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
    
    data_fields = {
        'labels': [data_unit[0] for data_unit in data],
        'values': [data_unit[1] for data_unit in data],
    }

    return data_fields

def create_data_by_field_pct(data, dataset_total):
    data_fields = {
        'labels': data['labels'],
        'values': [100 * round_num(value, dataset_total) 
                   for value in data['values']]
    }

    return data_fields

def create_data_by_region_qty(region_list, category):
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
        for document in cursor:
            data = [[key, document[key]]
                    for key in sorted(list(document.keys()))]

        qty_list.append({
            'chartType': 'bar',
            'chartName': field,
            'dataFields': {
                'values': [data_unit[1] for data_unit in data],
                'labels': [capitalize(data_unit[0]) 
                           for data_unit in data]
            }  
        })

    qty_list = sorted(qty_list, 
               key=lambda x: get_field_display_order(x['chartName']))

    return qty_list

def create_data_by_region_pct(chart_list, dataset_total_list):
    pct_list = []
    for chart in chart_list:
        value_list = chart['dataFields']['values']
        region_list = chart['dataFields']['labels']
        pct_value_list = []
        for index, value in enumerate(value_list):
            total = dataset_total_list[region_list[index]]
            pct_value_list.append(100 * round_num(value, total))

        pct_list.append({
            'chartType': 'bar',
            'chartName': chart['chartName'],
            'dataFields': {
                'values': pct_value_list,
                'labels': chart['dataFields']['labels']
            }  
        })

    return pct_list

def get_dataset_total_list(chart_list):
    """
    Get a list of the total number of people in the dataset
    for each region
    """
    dataset_total_list = dict()
    for chart in chart_list:
        region_list = chart['dataFields']['labels']
        value_list = chart['dataFields']['values']

        for index, region in enumerate(region_list):
            try:
                dataset_total_list[region] += value_list[index]
            except KeyError:
                dataset_total_list[region] = value_list[index]

    return(dataset_total_list)

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

def capitalize(name):
    return ''.join([(word[0].upper() + word[1:] + ' ') 
                    for word in name.split(' ')])[:-1]

if __name__ == "__main__":
    main()
