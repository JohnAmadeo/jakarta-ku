from __future__ import print_function
from flask import Flask, render_template, request, redirect, make_response, Response
from chartcreation import create_chart_list
import os, json

app = Flask(__name__)

@app.route('/')
def serve_index():
    return render_template('index.html')

@app.route('/charts', methods=['POST'])
def serve_charts():
    print("create new chart")
    body = request.get_json()
    comparison = body['comparison']
    region_list = body['region_list']
    category = body['category']

    chart_list = create_chart_list(comparison, region_list, category)
    return Response(response=json.dumps(chart_list),
                    status=200,
                    mimetype='application/json')  

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)    