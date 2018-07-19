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


class DominoHealthGeneral(object):

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
                    #'Server.Name': stats['Server.Name'],
                    'Server.ElapsedTime': stats['Server.ElapsedTime']
                    #'Stats.Time.Current': stats['Stats.Time.Current'],
                    #'Stats.Time.Start': stats['Stats.Time.Start']
                }
                domstats = self._status_server_performance(stats, domstats)
                domstats = self._status_buffer_pool(stats, domstats)
                domstats = self._status_database_namelookupcache(stats, domstats)
                domstats = self._status_updall(stats, domstats)
                #domstats = self._statistics_mail(stats, domstats)

            server['statistics'] = domstats
        self.server_count = count
        #print('loadStats - end')

    def alerts(self):
        for server in self.servers:
            print('')
            print(server['name'])

    def _status_server_performance(self, stats, domstats):

        sai = self._getStatFloat(stats, 'Server.AvailabilityIndex')
        stpm = self._getStatFloat(stats, 'Server.Trans.PerMinute')
        ct = self._getStatInt(stats, 'Server.ConcurrentTasks')
        ctw = self._getStatInt(stats, 'Server.ConcurrentTasks.Waiting')

        # Server.AvailabilityIndex
        sai_txt = 'Bad'
        if (sai >= 90):
            sai_txt = 'Excelent'
        elif (sai >= 30):
            sai_txt = 'Good'
        elif (sai >= 10):
            sai_txt = 'Warning'

        stpm_txt = 'Good'
        if (stpm > 10000):
            stpm_txt = 'Attention'

        ct_txt = 'Bad'
        if (ct <= 10):
            ct_txt = 'Good'

        ctw_txt = 'Bad'
        if (ctw == 0):
            ctw_txt = 'Excelent'

        domstats['Server.AvailabilityIndex'] = sai
        domstats['Server.AvailabilityIndex.status'] = sai_txt
        domstats['Server.ConcurrentTasks'] = ct
        domstats['Server.ConcurrentTasks.status'] = ct_txt
        domstats['Server.ConcurrentTasks.Waiting'] = ctw
        domstats['Server.ConcurrentTasks.Waiting.status'] = ctw_txt
        domstats['Server.Trans.PerMinute'] = stpm
        domstats['Server.Trans.PerMinute.status'] = stpm_txt
        return domstats

    def _status_buffer_pool(self, stats, domstats):

        pib = self._getStatFloat(stats, 'Database.Database.BufferPool.PerCentReadsInBuffer')
        #maxmegabytes = self._getStatFloat(stats, 'Database.Database.BufferPool.Maximum.Megabytes')
        highwatermak = self._getStatFloat(stats, 'Database.DbCache.HighWaterMark')
        currententries = self._getStatFloat(stats, 'Database.DbCache.CurrentEntries')
        maxentries = self._getStatFloat(stats, 'Database.DbCache.MaxEntries')
        ocr = self._getStatFloat(stats, 'Database.DbCache.OvercrowdingRejections')

        # http://www-01.ibm.com/support/docview.wss?uid=swg21286171
        # Solution: NSF_Buffer_Pool_Size_MB - default: 512MB
        pib_txt = 'Bad'
        pib_help = '# Increase NSF_Buffer_Pool_Size_MB - default: 512MB - See http://www-01.ibm.com/support/docview.wss?uid=swg21286171'
        if (pib >= 97):
            pib_txt = 'Excelent'
            pib_help = ''
        elif (pib >= 90):
            pib_txt = 'Good'
            pib_help = ''
        elif (pib >= 70):
            pib_txt = 'Warning'
            pib_help = '# Increase NSF_Buffer_Pool_Size_MB - default: 512MB - See http://www-01.ibm.com/support/docview.wss?uid=swg21286171'

        # http://www-01.ibm.com/support/docview.wss?uid=swg21279893
        dbcache = 'HighWaterMark (' + str(highwatermak) +') < MaxEntries (' + str(maxentries) + ')'
        dbcache_txt = 'Good'
        dbcache_help = ''
        if (highwatermak > maxentries):
            dbcache_txt = 'Bad'
            dbcache_help = '# Increase the DbCache setting: in NOTES.INI, set NSF_DBCACHE_MAXENTRIES to a value slightly greater than the total number of Notes databases on the server. See http://www-01.ibm.com/support/docview.wss?uid=swg21279893'

        ocr_txt = 'Bad'
        ocr_help = '# If the Database.DbCache.OvercrowdingRejections is high, then you should consider tuning this parameter'
        if (ocr == 0):
            ocr_txt = 'Good'
            ocr_help = ''

        domstats['Database.Database.BufferPool.PerCentReadsInBuffer'] = pib
        domstats['Database.Database.BufferPool.PerCentReadsInBuffer.status'] = pib_txt
        if (pib_help != ''):
            domstats['Database.Database.BufferPool.PerCentReadsInBuffer.status_help'] = pib_help
        #domstats['Database.Database.BufferPool.Maximum.Megabytes'] = maxmegabytes
        #domstats['Database.DbCache.HighWaterMark'] = highwatermak
        #domstats['Database.DbCache.CurrentEntries'] = currententries
        #domstats['Database.DbCache.MaxEntries'] = maxentries
        domstats['Database.DbCache'] = dbcache
        domstats['Database.DbCache.status'] = dbcache_txt
        if (dbcache_help != ''):
            domstats['Database.DbCache.status_help'] = dbcache_help
        domstats['Database.DbCache.OvercrowdingRejections'] = ocr
        domstats['Database.DbCache.OvercrowdingRejections.status'] = ocr_txt
        if (ocr_help != ''):
            domstats['Database.DbCache.OvercrowdingRejections.status_help'] = ocr_help
        return domstats

    def _status_database_namelookupcache(self, stats, domstats):

        dnlcp_used = self._getStatFloat(stats, 'Database.NAMELookupCachePool.Used')
        dnlcp_peak = self._getStatFloat(stats, 'Database.NAMELookupCachePool.Peak')
        dnlcm = self._getStatFloat(stats, 'Database.NAMELookupCacheMisses')
        dnlch = self._getStatFloat(stats, 'Database.NAMELookupCacheHits')
        dnlcms = self._getStatFloat(stats, 'Database.NAMELookupCacheMaxSize')

        # Database.NAMELookupCachePool.Used is close to the Database.NAMELookupCachePool.Peak value
        hitrate1 = dnlcp_used / dnlcp_peak * 100
        hitrate1_txt = 'Good'
        hitrate1_help = ''
        if (hitrate1 >= 98):
            hitrate1_txt = 'Bad'
            hitrate1_help = 'Database.NAMELookupCachePool.Used (' + str(dnlcp_used) +') is close to the Database.NAMELookupCachePool.Peak (' + str(dnlcp_peak) +') - Increase NLCache_Size - http://www-01.ibm.com/support/docview.wss?uid=swg21470902'
        elif (hitrate1 >= 90):
            hitrate1_txt = 'Warning'
            hitrate1_help = 'Database.NAMELookupCachePool.Used (' + str(dnlcp_used) +') is close to the Database.NAMELookupCachePool.Peak (' + str(dnlcp_peak) +') - Increase NLCache_Size - http://www-01.ibm.com/support/docview.wss?uid=swg21470902'
            

        # Database.NAMELookupCacheMisses remains above Database.NAMELookupCacheHits for hours
        #hitrate2 = dnlcm / dnlch * 100
        hitrate2 = 'NAMELookupCacheMisses (' + str(dnlcm) +') < NAMELookupCacheHits (' + str(dnlch) + ')'
        hitrate2_txt = 'Good'
        hitrate2_help = ''
        if (dnlcm > dnlch):
            hitrate2 = 'NAMELookupCacheMisses (' + str(dnlcm) +') > NAMELookupCacheHits (' + str(dnlch) + ')'
            hitrate2_txt = 'Bad'
            hitrate2_help = '# Database.NAMELookupCacheMisses remains above Database.NAMELookupCacheHits for hours - Increase NLCache_Size - http://www-01.ibm.com/support/docview.wss?uid=swg21470902'
            

        # Database.NAMELookupCacheMaxSize with Database.NAMELookupCachePool.Peak and Database.NAMELookupCachePool.Used
        # Neither value should have reached Database.NAMELookupCacheMaxSize. If the numbers are close, increase the cache size
        perc = dnlcp_used / dnlcms * 100
        perc_txt = 'Good'
        perc_help = ''
        if (perc >= 98):
            perc_txt = 'Bad'
            perc_help = 'Database.NAMELookupCachePool.Peak (' + str(dnlcp_peak) +') and Database.NAMELookupCachePool.Used (' + str(dnlcp_used) +') should not reach Database.NAMELookupCacheMaxSize (' + str(dnlcms) +').'
        elif (perc >= 90):
            perc_txt = 'Warning'
            perc_help = 'Database.NAMELookupCachePool.Peak (' + str(dnlcp_peak) +') and Database.NAMELookupCachePool.Used (' + str(dnlcp_used) +') should not reach Database.NAMELookupCacheMaxSize (' + str(dnlcms) +').'

        #domstats['Database.NAMELookupCachePool.Used'] =  dnlcp_used
        #domstats['Database.NAMELookupCachePool.Peak'] =  dnlcp_peak
        #domstats['Database.NAMELookupCacheMisses'] =  dnlcm
        #domstats['Database.NAMELookupCacheHits'] =  dnlch
        #domstats['Database.NAMELookupCacheMaxSize'] =  dnlcms
        #domstats['Database.NAMELookupCache.status'] =  dnlcm

        domstats['Database.NAMELookupCache.1'] =  utilities.formatPercentFloat(hitrate1)
        domstats['Database.NAMELookupCache.1.status'] =  hitrate1_txt
        if (hitrate1_help != ''):
            domstats['Database.NAMELookupCache.1.status_help'] =  hitrate1_help
        #domstats['Database.NAMELookupCache.2'] =  utilities.formatPercentFloat(hitrate2)
        domstats['Database.NAMELookupCache.2'] =  hitrate2
        domstats['Database.NAMELookupCache.2.status'] =  hitrate2_txt
        if (hitrate2_help != ''):
            domstats['Database.NAMELookupCache.2.status_help'] =  hitrate2_help
        domstats['Database.NAMELookupCache.3'] =  utilities.formatPercentFloat(perc)
        domstats['Database.NAMELookupCache.3.status'] =  perc_txt
        if (perc_help != ''):
            domstats['Database.NAMELookupCache.3.status_help'] =  perc_help

        ###
        #  Todo: Database.NAMELookupCache.CriticalContainerResets
        #        count of how many CRITICAL views-worth ($ServerAccess or $Users) have been discarded
        #        Database.NAMELookupCache.ContainerResets=
        ####
        domstats['Database.NAMELookupCache.CriticalContainerResets'] =  self._getStatFloat(stats, 'Database.NAMELookupCache.CriticalContainerResets')
        domstats['Database.NAMELookupCache.ContainerResets'] =  self._getStatFloat(stats, 'Database.NAMELookupCache.ContainerResets')
        return domstats

    def _status_updall(self, stats, domstats):
        # Tuning
        # Update_Fulltext_Thread=1
        # FTUPDATE_IDLE_TIME=4
        # ftg_use_sys_memory=1
        pl = self._getStatInt(stats, 'Update.PendingList')
        pl_txt = 'Bad'
        if (pl == 0):
            pl_txt = 'Excelent'
        elif (pl <= 100):
            pl_txt = 'Good'
        elif (pl <= 500):
            pl_txt = 'Warning'

        dl = self._getStatInt(stats, 'Update.DeferredList')
        dl_txt = 'Bad'
        if (dl == 0):
            dl_txt = 'Excelent'
        elif (dl <= 100):
            dl_txt = 'Good'
        elif (dl <= 500):
            dl_txt = 'Warning'

        domstats['Update.PendingList'] = pl
        domstats['Update.PendingList.status'] = pl_txt
        domstats['Update.DeferredList'] = dl
        domstats['Update.DeferredList.status'] = dl_txt
        return domstats

    def _statistics_mail(self, stats, domstats):
        domstats['Mail.Delivered'] = self._getStatInt(stats, 'Mail.Delivered')
        domstats['Mail.DeliveredSize.Under_1KB'] = self._getStatInt(
            stats, 'Mail.DeliveredSize.Under_1KB')
        domstats['Mail.DeliveredSize.1KB_to_10KB'] = self._getStatInt(
            stats, 'Mail.DeliveredSize.1KB_to_10KB')
        domstats['Mail.DeliveredSize.10KB_to_100KB'] = self._getStatInt(
            stats, 'Mail.DeliveredSize.10KB_to_100KB')
        domstats['Mail.DeliveredSize.100KB_to_1MB'] = self._getStatInt(
            stats, 'Mail.DeliveredSize.100KB_to_1MB')
        domstats['Mail.DeliveredSize.1MB_to_10MB'] = self._getStatInt(
            stats, 'Mail.DeliveredSize.1MB_to_10MB')
        domstats['Mail.DeliveredSize.10MB_to_100MB'] = self._getStatInt(
            stats, 'Mail.DeliveredSize.10MB_to_100MB')
        domstats['Mail.DeliveredSize.Over_100MB'] = self._getStatInt(
            stats, 'Mail.DeliveredSize.Over_100MB')
        domstats['Mail.TotalRouted'] = self._getStatInt(
            stats, 'Mail.TotalRouted')
        domstats['Mail.TotalRouted.NRPC'] = self._getStatInt(
            stats, 'Mail.TotalRouted.NRPC')
        domstats['Mail.TotalRouted.SMTP'] = self._getStatInt(
            stats, 'Mail.TotalRouted.SMTP')
        domstats['Mail.Transferred'] = self._getStatInt(
            stats, 'Mail.Transferred')
        domstats['Mail.Transferred.NRPC'] = self._getStatInt(
            stats, 'Mail.Transferred.NRPC')
        domstats['Mail.Transferred.SMTP'] = self._getStatInt(
            stats, 'Mail.Transferred.SMTP')
        domstats['Mail.TransferredSize.Under_1KB'] = self._getStatInt(
            stats, 'Mail.TransferredSize.Under_1KB')
        domstats['Mail.TransferredSize.1KB_to_10KB'] = self._getStatInt(
            stats, 'Mail.TransferredSize.1KB_to_10KB')
        domstats['Mail.TransferredSize.10KB_to_100KB'] = self._getStatInt(
            stats, 'Mail.TransferredSize.10KB_to_100KB')
        domstats['Mail.TransferredSize.100KB_to_1MB'] = self._getStatInt(
            stats, 'Mail.TransferredSize.100KB_to_1MB')
        domstats['Mail.TransferredSize.1MB_to_10MB'] = self._getStatInt(
            stats, 'Mail.TransferredSize.1MB_to_10MB')
        domstats['Mail.TransferredSize.10MB_to_100MB'] = self._getStatInt(
            stats, 'Mail.TransferredSize.10MB_to_100MB')
        domstats['Mail.TransferredSize.Over_100MB'] = self._getStatInt(
            stats, 'Mail.TransferredSize.Over_100MB')

        return domstats

    def render(self):

        myrender = Render(self.config.templatesPath(), 'domino-health-general-html.tpl',
                          self.config.wwwRoot() + 'domino-health-general.html')
        myrender.render(self.context)
        myrender = Render(self.config.templatesPath(), 'json',
                          self.config.wwwRoot() + 'domino-health-general.json')
        myrender.render(self.context)
