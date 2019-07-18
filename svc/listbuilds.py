import json

import common

from flask import Response
from html.parser import HTMLParser
from werkzeug.exceptions import BadRequest


class BuildsParser(HTMLParser):
    def __init__(self):
        super(BuildsParser, self).__init__()

        self.inTableLevel = 0
        self.builds = []

    def generateBuilds(self):
        for build in self.builds:
            if (len(build) == 0):
                continue
            if (not 'debugsymbols' in build[0]):
                continue
            yield json.dumps({
                'name': build[0].split('/')[-1],
                'url': common.DOWNLOADS_URL_BASE + build[0]
            }) + '\n'

    def handle_starttag(self, tag, attrs):
        if (tag == 'table'):
            self.inTableLevel += 1
        if (tag == 'tr'):
            self.inTableLevel += 1
            self.builds.append([])
        if (tag == 'td'):
            self.inTableLevel += 1

    def handle_data(self, data):
        if (self.inTableLevel < 3):
            return
        self.builds[-1].append(data)

    def handle_endtag(self, tag):
        if (tag == 'td'):
            self.inTableLevel -= 1
        if (tag == 'tr'):
            self.inTableLevel -= 1
        if (tag == 'table'):
            self.inTableLevel -= 1


class ListBuildsRequest:
    def __init__(self, request):
        self.buildOS = request.args['buildOS']


def listBuildsRequestImpl(request):
    lbRequest = ListBuildsRequest(request)

    r = common.gHttpService.request('GET', common.LIST_BUILDS_URL_BASE + lbRequest.buildOS)

    parser = BuildsParser()
    parser.feed(r.data.decode('utf-8'))
    r.release_conn()

    return Response(parser.generateBuilds())
