from __future__ import print_function
from flask import Flask, render_template, request, redirect, make_response, Response
import os

app = Flask(__name__)

@app.route('/')
def serve_index():
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)    