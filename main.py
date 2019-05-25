#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, Response, jsonify
import json

from api.m3u8.m3u8_parse import *

app = Flask(__name__)

@app.route('/m3u8', methods=['POST'])
def m3u8():    
    result = { 'status': 0, 'message': 'success' }

    try:
        json_data = request.get_json()
        if not 'url' in json_data:
            raise Exception('url parameter missing')

        channel = channel = json_data['c'] if 'c' in json_data else 1
        url = json_data['url']

        switcher = {
            1: simple,
            2: multiple,
            3: aggregation
        }
        # Get the function from switcher dictionary
        func = switcher.get(channel)
        if not func:
            raise Exception('invalid channel')

        # Execute the function
        return_url = func(url)
        result['playUrl'] = return_url
    except Exception as e:
        result['status'] = 1
        result['message'] = str(e)

    return Response(json.dumps(result), mimetype='application/json')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)