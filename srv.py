# -*- coding: utf-8 -*-

from flask import jsonify, Flask

import extractor
import img

app = Flask(__name__)

list = [
    {
        "rec_create_date": "12 Jun 2016",
        "rec_dietary_info": "nothing",
        "rec_dob": "01 Apr 1988",
        "rec_first_name": "New",
        "rec_last_name": "Guy",
    },
    {
        "rec_create_date": "1 Apr 2016",
        "rec_dietary_info": "Nut allergy",
        "rec_dob": "01 Feb 1988",
        "rec_first_name": "Old",
        "rec_last_name": "Guy",
    },
]

@app.route('/')
def index():
    # data = extractor.extract()
    data = img.search('./img/140149599.jpg')

    return jsonify(data)

@app.route('/test')
def test():
    return jsonify(list)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
