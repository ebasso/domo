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


class DominoHealthCluster(object):

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
            return int(sout)
        except KeyError:
            return 0

    def _getStatFloat(self, stats, str):
        try:
            sout = stats[str]
            sout = sout.replace(',', '')
            return float(sout)
        except KeyError:
            return 0.0

    def _getStatPercentFloat(self, stats, str):
        try:
            B = float(stats[str])
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
                    'Server.Name': stats['Server.Name'],
                    'Server.ElapsedTime': stats['Server.ElapsedTime'],
                    'Stats.Time.Current': stats['Stats.Time.Current'],
                    'Stats.Time.Start': stats['Stats.Time.Start'],
                }
                domstats = self._status_replica_cluster(stats, domstats)
            server['statistics'] = domstats
        self.server_count = count
        #print('loadStats - end')

    def alerts(self):
        for server in self.servers:
            print('')
            print(server['name'])

    def _status_replica_cluster(self, stats, domstats):
        secs = self._getStatInt(stats, 'Replica.Cluster.SecondsOnQueue')
        secs_avg = self._getStatInt(
            stats, 'Replica.Cluster.SecondsOnQueue.Avg')
        wqd = self._getStatInt(stats, 'Replica.Cluster.WorkQueueDepth')
        wqd_avg = self._getStatInt(stats, 'Replica.Cluster.WorkQueueDepth.Avg')

        # Replica.Cluster.SecondsOnQueue
        secs_txt = 'Bad'
        if (secs <= 10):
            secs_txt = 'Excelent'
        elif (secs <= 15):
            secs_txt = 'Good'

        # Replica.Cluster.SecondsOnQueue
        secs_avg_txt = 'Bad'
        if (secs_avg <= 10):
            secs_avg_txt = 'Excelent'
        elif (secs_avg <= 15):
            secs_avg_txt = 'Good'

        # Replica.Cluster.WorkQueueDepth
        wqd_txt = 'Bad'
        if (wqd <= 10):
            wqd_txt = 'Excelent'
        elif (wqd <= 15):
            wqd_txt = 'Good'

        # Replica.Cluster.WorkQueueDepth.Avg
        wqd_avg_txt = 'Bad'
        if (wqd_avg <= 10):
            wqd_avg_txt = 'Excelent'
        elif (wqd_avg <= 15):
            wqd_avg_txt = 'Good'

        # Only Clusters
        domstats['Replica.Cluster.SecondsOnQueue'] = secs
        domstats['Replica.Cluster.SecondsOnQueue.status'] = secs_txt
        domstats['Replica.Cluster.SecondsOnQueue.Avg'] = secs_avg
        domstats['Replica.Cluster.SecondsOnQueue.Avg.status'] = secs_avg_txt
        domstats['Replica.Cluster.SecondsOnQueue.Max'] = self._getStatInt(stats, 'Replica.Cluster.SecondsOnQueue.Max')
        domstats['Replica.Cluster.WorkQueueDepth'] = wqd
        domstats['Replica.Cluster.WorkQueueDepth.status'] = wqd_txt
        domstats['Replica.Cluster.WorkQueueDepth.Avg'] = wqd_avg
        domstats['Replica.Cluster.WorkQueueDepth.Avg.status'] = wqd_avg_txt
        domstats['Replica.Cluster.WorkQueueDepth.Max'] = self._getStatInt(stats, 'Replica.Cluster.WorkQueueDepth.Max')
        return domstats

    def render(self):

        myrender = Render(self.config.templatesPath(), 'domino-health-cluster-html.tpl',
                          self.config.wwwRoot() + 'domino-health-cluster.html')
        myrender.render(self.context)
        myrender = Render(self.config.templatesPath(), 'json',
                          self.config.wwwRoot() + 'domino-health-cluster.json')
        myrender.render(self.context)