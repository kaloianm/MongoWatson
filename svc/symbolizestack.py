#!/usr/bin/env python

import common, json, re, symbolize

from flask import jsonify
from werkzeug.exceptions import BadRequest

sourcePathRegex = r'/data/mci/(?P<buildId>\w+)/src/(?P<sourcePath>[\w\W]+):(?P<lineNum>\d+):(?P<colNum>\d+):\s+(?P<funcName>\S{1}[\S\s]+)'


def gitUrl(buildInfo, stackLine):
    match = re.match(sourcePathRegex, stackLine)
    if (match):
        return {
            'functionName':
                match['funcName'],
            'sourceFileUrl':
                'https://github.com/mongodb/mongo/tree/{}/{}#L{}'.format(buildInfo['githash'],
                                                                     match['sourcePath'],
                                                                     match['lineNum'])
        }
    else:
        return {'functionName': None}


class SymbolizeStackRequest:
    def __init__(self, request):
        self.stack = request['stack']


class SymbolizeStackResponse:
    def __init__(self, buildInfo, stackFrames):
        self.buildInfo = buildInfo
        self.stackFrames = stackFrames

    def tojson(self):
        return jsonify(buildInfo=self.buildInfo, stackFrames=self.stackFrames)


def symbolizeStackRequestImpl(request):
    if isinstance(request, str):
        ssRequest = SymbolizeStackRequest({ 'stack' : request })
    elif request.is_json:
        ssRequest = SymbolizeStackRequest(request.get_json())
    else:
        raise BadRequest('Invalid request content')

    build_info, symbolized_stacktrace = symbolize.symbolize_backtrace_from_logs(ssRequest.stack, json_format=True)

    # FIXME: this is going to fail now.
    # The symbolized_stacktrace will contain entries like the following:
      # {
      #   "path": "/Users/rf/.mongosymb.cache/c5c4d740b31991fe10d9e8b5550c9afd2d195028.debug",
      #   "buildId": "C5C4D740B31991FE10D9E8B5550C9AFD2D195028",
      #   "offset": "1CD6195",
      #   "addr": 30237076,
      #   "symbol": null,
      #   "symbinfo": [
      #     {
      #       "fn": "std::function<void ()>::operator()() const",
      #       "file": "/opt/mongodbtoolchain/v2/include/c++/5.4.0/functional",
      #       "column": 0,
      #       "line": 2267
      #     },
      #     {
      #       "fn": "operator()",
      #       "file": "/data/mci/7946403a5351d044e6cf13da2806ff98/src/src/mongo/transport/service_executor_synchronous.cpp",
      #       "column": 0,
      #       "line": 138
      #     },
      #     {
      #       "fn": "std::_Function_handler<void (), mongo::transport::ServiceExecutorSynchronous::schedule(std::function<void ()>, mongo::transport::ServiceExecutor::ScheduleFlags, mongo::transport::ServiceExecutorTaskName)::'lambda'()>::_M_invoke(std::_Any_data const&)",
      #       "file": "/opt/mongodbtoolchain/v2/include/c++/5.4.0/functional",
      #       "column": 0,
      #       "line": 1871
      #     }
      #   ]
      # },

    ssResponse = SymbolizeStackResponse(
        buildInfo, list(map(lambda stackFrame: gitUrl(buildInfo, stackFrame.strip()), stackFrames)))

    return ssResponse.tojson()

if __name__ == '__main__':
    # Enable testing from the command line
    import sys
    with open(sys.argv[1], 'r') as f:
        logs = f.readlines()
    symbolizeStackRequestImpl('\n'.join(logs))
