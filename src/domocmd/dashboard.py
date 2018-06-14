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
import json
import time
from domocmd.render import Render


class Dashboard(object):

    def __init__(self, config):
        self.config = config
        self.now = time.strftime("%Y-%m-%d %H:%M")
        self.context = {'title': 'Dashboard',
                        'now': self.now,
                        'panels': [
                            {'pn': 'panel-primary', 'icon': 'fa-comment', 'num': '121', 'msg': 'Domino Servers', 'href':'/comments.html'},
                            {'pn': 'panel-green', 'icon': 'fa-twitter', 'num': '50.37%', 'msg': 'New Tasks', 'href':'#'},
                            {'pn': 'panel-yellow', 'icon': 'fa-envelope', 'num': '124', 'msg': 'Notifications', 'href':'#'},
                            {'pn': 'panel-red', 'icon': 'fa-tasks', 'num': '13', 'msg': 'Alerts', 'href':'#'}]
                        }
                        #{'pn': 'panel-red', 'icon': 'fa-tasks', 'num': '13', 'msg': 'Alerts', 'href':'#'},
        self.notifications = [
            {'icon': 'fa-comment', 'msg': 'New Comment Created', 'when': '4 minutes ago', 'href':'/comments.html'},
            {'icon': 'fa-twitter', 'msg': '3 New Followers', 'when': '12 minutes ago', 'href':'#'},
            {'icon': 'fa-envelope', 'msg': 'Message Sent', 'when': '27 minutes ago', 'href':'#'},
            {'icon': 'fa-tasks', 'msg': 'New Task', 'when': '43 minutes ago', 'href':'#'},
            {'icon': 'fa-upload', 'msg': 'Server Rebooted', 'when': '11:32 AM', 'href':'#'},
            {'icon': 'fa-bolt', 'msg': 'Server Crashed!', 'when': '11:13 AM', 'href':'#'},
            {'icon': 'fa-warning', 'msg': 'Server Not Responding', 'when': '10:57 AM', 'href':'#'},
            {'icon': 'fa-shopping-cart', 'msg': 'New Order Placed', 'when': '9:49 AM', 'href':'#'},
            {'icon': 'fa-money', 'msg': 'Payment Received', 'when': 'Yesterday', 'href':'#'}]

    def render(self):
        myrender = Render(self.config.templatesPath(), 'dashboard-html.tpl',
                          self.config.wwwRoot() + 'dashboard.html')
        myrender.render(self.context)
        myrender = Render(self.config.templatesPath(), 'json',
                          self.config.wwwRoot() + 'dashboard.json')
        #myrender.render(self.context)
        myrender = Render(self.config.templatesPath(), 'json',
                          self.config.wwwRoot() + 'dashboard-notifications.json')
        #myrender.render(self.notifications)
