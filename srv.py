# -*- coding: utf-8 -*-

from flask import jsonify, Flask

import extractor
import img
import mongo
import info

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"state":True})

# @app.route('/search')
# def search():
#     # data = extractor.extract()
#     data = img.search('./img/140149599.jpg')

#     return jsonify(data)

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
