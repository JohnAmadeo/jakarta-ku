from __future__ import print_function
from flask import Flask, render_template, request, redirect, make_response, Response
from pymongo import MongoClient
from fieldutils import get_field_display_order, get_field_list
import os, json

DATABASE = MongoClient().get_database('jakartaku')

def main():
    chart_list = create_demographics_chart(['koja', 'tebet'], 'region')

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
        (qty_list, label_list) = \
            create_data_by_region_qty(region_list, 'religion')

        dataset_total_list = get_dataset_total_list(qty_list)
        pct_list = create_data_by_region_pct(qty_list, 
                                             dataset_total_list)

        chart_list = {'chartList': [], 'labelList': label_list}
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
        (qty_list, label_list) = \
            create_data_by_region_qty(region_list, 'education')

        dataset_total_list = get_dataset_total_list(qty_list)
        pct_list = create_data_by_region_pct(qty_list, 
                                             dataset_total_list)

        chart_list = {'chartList': [], 'labelList': label_list}
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
        (qty_list, label_list) = \
            create_data_by_region_qty(region_list, 'marriage')
        dataset_total_list = get_dataset_total_list(qty_list)
        pct_list = create_data_by_region_pct(qty_list,
                                             dataset_total_list)

        chart_list = {'chartList': [], 'labelList': label_list}
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
        qty_data = create_data_by_field_qty(region_list, 'occupation')
        qty_data['labels'] = \
            [label for label, value in 
             sorted(zip(qty_data['labels'], qty_data['values']), 
                    key=lambda x: x[1], reverse=True)]
        qty_data['values'] = sorted(qty_data['values'], reverse=True)

        top_ten_chart = {
            'chartType': 'bar',
            'chartName': '10 Pekerjaan dengan Jumlah Orang Paling Banyak',
            'dataFields': {
                'labels': qty_data['labels'][:10],
                'values': qty_data['values'][:10]
            },
            'dataOptions': {
                'fieldAxis': 'Pekerjaan',
                'measureAxis': 'Jumlah Orang',
                'tooltipStringFormat': ['_', ' ', 'Orang']
            }
        }

        num_jobs = len(qty_data['labels'])
        bottom_ten_chart = {
            'chartType': 'bar',
            'chartName': '10 Pekerjaan dengan Jumlah Orang Paling Sedikit',
            'dataFields': {
                'labels': qty_data['labels'][num_jobs - 10:],
                'values': qty_data['values'][num_jobs - 10:]
            },
            'dataOptions': {
                'fieldAxis': 'Pekerjaan',
                'measureAxis': 'Jumlah Orang',
                'tooltipStringFormat': ['_', ' ', 'Orang']
            }
        }

        chart_list = {'chartList': [top_ten_chart, bottom_ten_chart]}

        for start in range(10, num_jobs - 10,10):
            end = (start + 10) if start != 70 else (start + 5) 
            chart_list['chartList'].append({
                'chartType': 'bar',
                'chartName': 'Pekerjaan berdasarkan Jumlah ' + \
                             'Orang: #' + str(start) + \
                             '-#' + str(end),
                'dataFields': {
                    'labels': qty_data['labels'][start:end],
                    'values': qty_data['values'][start:end]                  
                },
                'dataOptions': {
                    'fieldAxis': 'Pekerjaan',
                    'measureAxis': 'Jumlah Orang',
                    'tooltipStringFormat': ['_', ' ', 'Orang']
                }                
            })

        jsonprint(chart_list)
        return chart_list 

    elif comparison == 'region': 
        (qty_list, label_list) = \
            create_data_by_region_qty(region_list, 'occupation')

        for chart in qty_list[:]:
            if all_x(chart['dataFields']['values'], 0):
                qty_list.remove(chart)
            else:
                chart['chartName'] = 'Jumlah Orang dengan ' + \
                                     'pekerjaan ' + \
                                     chart['chartName']
                chart['dataOptions'] = {
                    'tooltipStringFormat': ['_', ' ', 'Orang'],
                    'fieldAxis': 'Kecamatan',
                    'measureAxis': 'Jumlah Orang'
                }

        chart_list = {'chartList': qty_list, 'labelList': label_list}
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
        data = create_data_by_field_qty(region_list, 'demographics')
    
        age_labels = [(data['labels'][index].split(' ')[0] + ' Tahun') 
                      for index in range(0, len(data['labels']),2)]
        age_values = [(data['values'][index]+data['values'][index+1]) 
                      for index in range(0, len(data['values']),2)]
        dataset_total = sum(age_values)
    
        qty_age_chart1 = {
            'chartType': 'bar',
            'chartName': 'Jumlah Orang berdasarkan Umur: 0-49 Tahun',
            'dataFields': {
                'labels': age_labels[:10],
                'values': age_values[:10]
            },
            'dataOptions': {
                'fieldAxis': 'Kategori Demografi',
                'measureAxis': 'Jumlah Orang',
                'tooltipStringFormat': ['_', ' Orang']
            }
        }   

        qty_age_chart2 = {
            'chartType': 'bar',
            'chartName': 'Jumlah Orang berdasarkan Umur: 50-75< Tahun',
            'dataFields': {
                'labels': age_labels[10:],
                'values': age_values[10:]
            },
            'dataOptions': {
                'fieldAxis': 'Kategori Demografi',
                'measureAxis': 'Jumlah Orang',
                'tooltipStringFormat': ['_', ' Orang']
            }
        }              

        pct_age_chart = {
            'chartType': 'doughnut',
            'chartName': 'Persentase Orang berdasarkan Umur',
            'dataFields': {
                'labels': age_labels,
                'values': [100 * (value/dataset_total) 
                            for value in age_values]
            },
            'dataOptions': {
                'tooltipStringFormat': ['_', '%']
            }
        }

        qty_demo_chart1 = {
            'chartType': 'bar',
            'chartName': 'Jumlah Orang berdasarkan Umur dan Kelamin: 0-24 Tahun',
            'dataFields': {
                'labels': data['labels'][:10],
                'values': data['values'][:10]
            },
            'dataOptions': {
                'fieldAxis': 'Kategori Demografi',
                'measureAxis': 'Jumlah Orang',
                'tooltipStringFormat': ['_', ' Orang']
            }
        }   

        qty_demo_chart2 = {
            'chartType': 'bar',
            'chartName': 'Jumlah Orang berdasarkan Umur dan Kelamin: 25-49 Tahun',
            'dataFields': {
                'labels': data['labels'][10:20],
                'values': data['values'][10:20]
            },
            'dataOptions': {
                'fieldAxis': 'Kategori Demografi',
                'measureAxis': 'Jumlah Orang',
                'tooltipStringFormat': ['_', ' Orang']
            }
        }   

        qty_demo_chart3 = {
            'chartType': 'bar',
            'chartName': 'Jumlah Orang berdasarkan Umur dan Kelamin: 50-75< Tahun',
            'dataFields': {
                'labels': data['labels'][20:],
                'values': data['values'][20:]
            },
            'dataOptions': {
                'fieldAxis': 'Kategori Demografi',
                'measureAxis': 'Jumlah Orang',
                'tooltipStringFormat': ['_', ' Orang']
            }
        }       

        gender_values = [
            sum([data['values'][index] 
                for index in range(0, len(data['values']), 2)]),
            sum([data['values'][index] 
                for index in range(1, len(data['values']), 2)])
        ]
        gender_labels = ['Laki-Laki', 'Perempuan']
        pct_gender_chart = {
            'chartType': 'doughnut',
            'chartName': 'Persentase Orang berdasarkan Kelamin',
            'dataFields': {
                'labels': gender_labels,
                'values': [100 * (value / dataset_total)
                           for value in gender_values]
            },
            'dataOptions': {
                'tooltipStringFormat': ['_','%']
            }
        } 

        chart_list = {
            'chartList': [
                qty_age_chart1, qty_age_chart2, pct_age_chart,
                qty_demo_chart1, qty_demo_chart2, qty_demo_chart3,
                pct_demo_chart, pct_gender_chart
            ]
        }

        jsonprint(chart_list)
        return chart_list
    elif comparison == 'region':
        (qty_list, label_list) = \
            create_data_by_region_qty(region_list, 'demographics')
        dataset_total_list = get_dataset_total_list(qty_list)
        pct_list = create_data_by_region_pct(qty_list, 
                                             dataset_total_list)

        chart_list = {'chartList': [], 'labelList': label_list}
        for index, chart in enumerate(qty_list):
            pct_list[index]['dataOptions'] = {
                'tooltipStringFormat': ['_', '%'],
                'fieldAxis': 'Umur dan Kelamin',
                'measureAxis': 'Persentase Orang'
            }
            qty_list[index]['dataOptions'] = {
                'tooltipStringFormat': ['_', ' ', 'Orang'],
                'fieldAxis': 'Umur dan Kelamin',
                'measureAxis': 'Jumlah Orang'
            }

            field = pct_list[index]['chartName']
            pct_list[index]['chartName'] = \
                "Persentase Orang dalam Kategori '" + field + \
                "' menurut Kecamatan"
            qty_list[index]['chartName'] = \
                "Jumlah Orang dalam Kategori '" + field + \
                "' menurut Kecamatan"

            chart_list['chartList'].append(pct_list[index])
            chart_list['chartList'].append(qty_list[index])

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
    label_list = [chart['chartName'] for chart in qty_list]

    return (qty_list, label_list)

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
