#!python3

# Main entry point for the Mongo Watson web service
#

import sys

from flask import Flask
from flask import jsonify
from flask import request
from flask import abort

from flask_cors import CORS

from werkzeug.exceptions import BadRequest


# Ensure that the caller is using python 3
if (sys.version_info[0] < 3):
    raise Exception("Must be using Python 3")

app = Flask(__name__)
CORS(app)

class SymbolizedStack:
    def __init__(self, buildInfo):
        self.buildInfo = buildInfo
    
    def tojson(self):
        return jsonify(buildInfo = self.buildInfo)

@app.route('/symbolizestack', methods=['POST'])
def post():
    print('Executing request ', request.method)

    if (not request.is_json):
        raise BadRequest('Invalid request content')

    content = request.get_json()
    print(content)
    stack = content['stack']

    symbolizedStack = SymbolizedStack('0x001212AA')

    return symbolizedStack.tojson()


if __name__ == '__main__':
    app.run(debug=True)
