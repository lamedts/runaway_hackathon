# -*- coding: utf-8 -*-

from flask import jsonify, Flask, send_from_directory, url_for, request 
import json

import extractor
import img
import mongo
import info
import plot

app = Flask(__name__, static_url_path='/img')

@app.route('/')
def index():
    return jsonify({"state":True})

@app.route('/search/<id>')
def search(id):
    data = info.search(id)
    return jsonify(data)

@app.route('/plot',  methods=['POST']) 
def chart():
    if not request.json:
        # abort(400)
        pass
    # print(request.json)
    request_obj = request.json
    print(request_obj)
    # print(request_obj.list)
    return plot.get_chart(request_obj)
    # return  json.dumps(request.json)

@app.route('/train')
def train():
    data = mongo.getTrain()
    return jsonify(data)

@app.route('/test')
def test():
    data = mongo.getTest()
    return jsonify(data)

@app.route('/infomatch')
def infomatch():
    data = mongo.getInfoMatch()
    return jsonify(data)

@app.route('/imgmatch')
def imgmatch():
    data = mongo.getImgMatch()
    return jsonify(data)

@app.route('/bulkupload')
def bulkupload():
    data = mongo.getImgMatch()
    return jsonify(data)

# @app.route('/test')
# def test():
#     return jsonify(list)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
