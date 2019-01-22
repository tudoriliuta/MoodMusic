import json
from time import time
from random import random
from flask import Flask, render_template, make_response

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html', data='test')

@app.route('/live-data')
def live_data(data_dict):
    # Gets a dictionary and echoes its values as JSON
    print "Works! " + data_dict['happiness']
    data = [time() * 1000, data_dict['happiness']]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
