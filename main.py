#!/usr/bin/env python
import os
import urllib2
import webapp2
from google.appengine.api import memcache
from HTMLParser import HTMLParser
from webapp2_extras import json


class PlayStoreParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.version_tag = False
        self.version_info = None
        self.change_tag = False
        self.change_info = []

    def handle_starttag(self, tag, attributes):
        for name, value in attributes:
            # find softwareVersion which corresponds to android:versionName
            if name == "itemprop" and value == "softwareVersion":
                self.version_tag = True
                break
            # find list of changes to be parsed into a list later
            if name == "class" and value == "recent-change":
                self.change_tag = True
                break

    def handle_data(self, data):
        if self.version_tag:
            self.version_info = data.strip()
            self.version_tag = False

        if self.change_tag:
            self.change_info.append(data)
            self.change_tag = False


class CacheHandler(webapp2.RequestHandler):

    def get(self):
        self.cache_result(
            self.get_update_info()
        )

    def get_update_info(self):
        parser = None
        try:
            # read in play store page and pass into custom parser
            response = urllib2.urlopen(
                urllib2.Request(
                    os.environ['play_store_url']))
            parser = PlayStoreParser()
            parser.feed(response.read())
        except urllib2.HTTPError as e:
            print 'HTTPError = ' + str(e.code)
        except urllib2.URLError as e:
            print 'URLError = ' + str(e.reason)
        finally:
            return parser

    def cache_result(self, data):
        cache_data = {}

        cache_data["version_code"] = int(
            data.version_info.split(".")[-1]) if data.version_info else 0

        change_list = ""
        if data.change_info:
            change_list = "What's New:</p><br>"
            for change in data.change_info:
                change_list += "<li>" + change + "</li>"

        cache_data['content'] = change_list

        memcache.add('play_info', cache_data)


class VersionHandler(webapp2.RequestHandler):

    def get(self):
        data = memcache.get('play_info')
        self.response.content_type = 'application/json'
        self.response.write(json.encode(data))


app = webapp2.WSGIApplication(
    [('/', VersionHandler), ("/cache", CacheHandler)])