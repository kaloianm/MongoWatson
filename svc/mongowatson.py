#!python3

#
# Main entry point for the Mongo Watson web service
#

import sys

# Ensure that the caller is using python 3
if (sys.version_info[0] < 3):
    raise Exception("Must be using Python 3")

import site
site.addsitedir('svc/triage-scripts/mongosymb')

from flask import Flask, request
from flask_cors import CORS

from listbuilds import listBuildsRequestImpl
from symbolizestack import symbolizeStackRequestImpl

app = Flask(__name__)
CORS(app)


# Implemenst the listbuilds API
#
# Request parameters:
#   - buildOS: string, one of the fixed supported operating systems for which to list the available
#              builds
#
# Response: New line-separated list of JSON objects containing 'name' of the build and 'url' from
#           where to download the symbols archive
#
@app.route('/listbuilds', methods=['GET'])
def get():
    return listBuildsRequestImpl(request)


# Implements the symbolizestack API
#
# Request parameters:
#   - stack: string
#   - buildId: string (optional)
#
# Response: SymbolizeStackResponse
#
@app.route('/symbolizestack', methods=['POST'])
def post():
    return symbolizeStackRequestImpl(request)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
