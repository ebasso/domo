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
# Requires Python 3.6
#
import json
import time
import domocmd.utilities as utilities
from domocmd.render import Render


class DominoHealthPlatform(object):

    def __init__(self, config, servers):
        self.config = config
        self.servers = servers
        self.server_count = 0
        self.loadStats()
        self.now = time.strftime("%Y-%m-%d %H:%M")
        self.context = {'title': 'Domino Statistics',
                        'now': self.now,
                        'servers': self.servers,
                        'server_count': self.server_count
                        }

    def _parseStatsFromFile(self, server):
        fileName = self.config.tempDir() + server['name']
        inputfile = open(fileName + '.tmp',mode='rb')

        aDict = {}

        for line in inputfile:
            line = line.strip()
            start = line.find(' = ')
            if (start > 0):
                k, v = line.split(' = ', 1)
                aDict[k] = v

        inputfile.close()
        return aDict

    def _getStatInt(self, stats, str):
        try:
            sout = stats[str]
            sout = sout.replace(',', '')
            if (sout.count('.') >= 2):
                sout = sout.replace('.','')
            #if (sout.count('+') == 0):
            #    sout = sout.replace('.', '')
            return int(sout)
        except KeyError:
            return 0

    def _getStatFloat(self, stats, str):
        try:
            sout = stats[str]
            sout = sout.replace(',', '')
            if (sout.count('.') >= 2):
                sout = sout.replace('.','')
            #if (sout.count('+') == 0):
            #    sout = sout.replace('.', '')
            return float(sout)
        except KeyError:
            return 0.0

    def _getStatPercentFloat(self, stats, str):
        try:
            sp = stats[str]
            sp = sp.replace(',', '.')
            B = float(sp)
            sout = '{0:.2f}'.format(B)
            sout = '{message:{fill}{align}{width}}'.format(message=sout, fill=' ', align='>', width=0)
            return float(sout)
        except KeyError:
            return 0

    def loadStats(self):
        #print('loadStats - start')
        count = 0
        for server in self.servers:
            #print 'parse from server: %s' % (server['name'])
            stats = self._parseStatsFromFile(server)
            if (stats):
                count += 1
                domstats = {
                    #'Server.Name': stats['Server.Name']
                }
                domstats = self._status_platform_pagingfile(stats, domstats)

            server['statistics'] = domstats
        self.server_count = count
        #print('loadStats - end')

    def alerts(self):
        for server in self.servers:
            print('')
            print(server['name'])

    
    def _status_platform_pagingfile(self, stats, domstats):

        avg = self._getStatFloat(
            stats, 'Platform.PagingFile.Total.PctUtil.Avg')
        txt = 'Bad'
        if (avg <= 10):
            txt = 'Excelent'
        elif (avg <= 20):
            txt = 'Good'
        elif (avg <= 60):
            txt = 'Warning'
        domstats['Platform.PagingFile.Total.PctUtil.Avg'] = avg
        domstats['Platform.PagingFile.Total.PctUtil.Avg.status'] = txt
        return domstats

    
    def render(self):

        myrender = Render(self.config.templatesPath(), 'domino-health-platform-html.tpl',
                          self.config.wwwRoot() + 'domino-health-platform.html')
        myrender.render(self.context)
        myrender = Render(self.config.templatesPath(), 'json',
                          self.config.wwwRoot() + 'domino-health-platform.json')
        myrender.render(self.context)
