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


class DominoHealthHttp(object):

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
            if (sout.count('+') == 0):
                sout = sout.replace('.', '')
            return int(sout)
        except KeyError:
            return 0

    def _getStatFloat(self, stats, str):
        try:
            sout = stats[str]
            sout = sout.replace(',', '')
            if (sout.count('+') == 0):
                sout = sout.replace('.', '')
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
                    'Server.Name': stats['Server.Name'],
                    'Server.ElapsedTime': stats['Server.ElapsedTime'],
                    'Stats.Time.Current': stats['Stats.Time.Current'],
                    'Stats.Time.Start': stats['Stats.Time.Start'],
                }
                domstats = self._status_domino_cache_design(stats, domstats)
                domstats = self._status_domino_cache_usercache(stats, domstats)
                domstats = self._status_net_groupcache(stats, domstats)
            server['statistics'] = domstats
        self.server_count = count
        #print('loadStats - end')

    def alerts(self):
        for server in self.servers:
            print('')
            print(server['name'])

    def _status_domino_cache_design(self, stats, domstats):

        hitrate = self._getStatPercentFloat(stats, 'Domino.Cache.Design.HitRate')
        hitrate_status = 'Disabled'
        if (hitrate >= 97):
            hitrate_status = 'Excelent'
        elif (hitrate >= 90):
            hitrate_status = 'Good'
        elif (hitrate > 0):
            hitrate_status = 'Bad'

        displacerate = self._getStatPercentFloat(stats,  'Domino.Cache.Design.DisplaceRate')
        displacerate_status = 'Bad'
        if (displacerate == 0):
            displacerate_status = 'Good'

        domstats['Domino.Cache.Design.HitRate'] = hitrate
        domstats['Domino.Cache.Design.HitRate.status'] = hitrate_status
        domstats['Domino.Cache.Design.DisplaceRate'] = displacerate
        domstats['Domino.Cache.Design.DisplaceRate.status'] = displacerate_status
        domstats['Domino.Cache.Design.MaxSize'] = self._getStatInt(stats, 'Domino.Cache.Design.MaxSize')
        return domstats

    def _status_net_groupcache(self, stats, domstats):

        ngcsize = self._getStatInt(stats, 'NET.GroupCache.Size')
        ngcused = self._getStatInt(stats, 'NET.GroupCache.Used')

        ngcstatus = 'Used (' + str(ngcused) +') < Size (' + str(ngcsize) + ')'
        ngcstatus_txt = 'Good'
        ngcstatus_help = ''
        if (ngcused >= ngcsize):
            ngcstatus_txt = 'Bad'
            ngcstatus_help = '# NET.GroupCache.Used (' + str(ngcused) +') is NET.GroupCache.Size (' + str(dnlcp_peak) +') - Increase Group_cache_size'

        domstats['NET.GroupCache'] = ngcstatus
        domstats['NET.GroupCache.status'] = ngcstatus_txt
        domstats['NET.GroupCache.status_help'] = ngcstatus_help
        return domstats

    def _status_domino_cache_usercache(self, stats, domstats):
    
        hitrate = self._getStatPercentFloat(stats, 'Domino.Cache.User Cache.HitRate')
        hitrate_status = 'Disabled'
        if (hitrate >= 97):
            hitrate_status = 'Excelent'
        elif (hitrate >= 90):
            hitrate_status = 'Good'
        elif (hitrate > 0):
            hitrate_status = 'Bad'

        displacerate = self._getStatPercentFloat(stats,  'Domino.Cache.User Cache.DisplaceRate')
        displacerate_status = 'Bad'
        if (displacerate == 0):
            displacerate_status = 'Good'

        #print('|- Domino.Cache.User Cache.HitRate: ', hitrate, ', maxsize=', maxsize, txt)
            # _status_domino_cache_usercache(server)
        domstats['Domino.Cache.User Cache.HitRate'] = hitrate
        domstats['Domino.Cache.User Cache.HitRate.status'] = hitrate_status
        domstats['Domino.Cache.User Cache.DisplaceRate'] = displacerate
        domstats['Domino.Cache.User Cache.DisplaceRate.status'] = displacerate_status
        domstats['Domino.Cache.User Cache.MaxSize'] = self._getStatInt(
            stats, 'Domino.Cache.User Cache.MaxSize')
        return domstats

    def render(self):

        myrender = Render(self.config.templatesPath(), 'domino-health-http-html.tpl',
                          self.config.wwwRoot() + 'domino-health-http.html')
        myrender.render(self.context)
        myrender = Render(self.config.templatesPath(), 'json',
                          self.config.wwwRoot() + 'domino-health-http.json')
        myrender.render(self.context)
        