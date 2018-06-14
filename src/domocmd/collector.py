#!/usr/bin/python
# vim: et sw=4 ts=4:
# -*- coding: utf-8 -*-
#
# Domo - free/libre analytics platform
#
# by ebasso@ebasso.net
# @link https://ebasso.net
# @license https://www.gnu.org/licenses/gpl-3.0.html GPL v3 or later
# @version $Id$
#
# For more info see: https://ebasso.net/wiki
#
# Requires Python 2.6 or 2.7
#
import sys
import getopt
import requests
#from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json

# Disable Warnings from Untrusted TLs keys
#requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Collector(object):
    """
    Open config.json and download Domino stats
    """

    def __init__(self, config, servers):
        self.config = config
        self.servers = servers

    def _doGet(self,url):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
            r = requests.get(url=url, headers=headers, verify=False)
            if (r.status_code != 200):
                print('requests.get -> %s = %s\n' % (r.url, r))
                return None
            return r.content
        except requests.exceptions.RequestException as e:
            print(url, e)
            return None

    def _getStats(self,server):
        url = server['host'] + '/stats.txt'
        content = self._doGet(url)
        if (content):
            fileName = self.config.tempDir() + server['name'] + '.tmp'
            with open(fileName, mode='wb+') as outputfile:
                outputfile.write(content)
                outputfile.close()

    def collect(self):
        for server in self.servers:
            print ('download from server: %s' % server['name'])
            content = self._getStats(server)
