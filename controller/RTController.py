#!/usr/bin/env python
""" Controller
    -*-MAIN PAGE-*-    ->Controller for main page requests


    @author Alfredo Sanz
    @date Sept 2020
"""
# APIs imports
import logging
import json
from datetime import date, timedelta, datetime
import time

# local imports
from common import Util
from common import Constantes
from service.RT_Service import RT_Service



class RTController:


    def __init__(self):
        self.log = logging.getLogger('TDA_DataVisualizator')
    #


    def getTheTime(self):
        self.log.debug('RTController - getTheTime INIT')

        rt_service = RT_Service()
        result = rt_service.getThetime()

        self.log.debug('RTController - getTheTime ENDS')
        return result
    #


    def getSessionName(self):
        self.log.debug('RTController - getSessionName INIT')

        rt_service = RT_Service()
        result = rt_service.getTheSessionName()

        self.log.debug('RTController - getSessionName ENDS')
        return result
    #


    def getGlobalData(self, _request):
        self.log.debug('RTController - getGlobalData INIT')
        errormessage = '0'

        sessionName = _request.args.get('sessionName')
        self.log.debug('sessionName->' + sessionName)
        market = _request.args.get('market')
        self.log.debug('market->' + market)

        rt_service = RT_Service()
        errormessage, result = rt_service.getGlobalData(market, sessionName)

        self.log.debug('RTController - getGlobalData ENDS')
        return result
    # fin getGlobalData


    def getDeltas(self, _request):
        self.log.debug('RTController - getDeltas INIT')
        errormessage = '0'

        market = _request.args.get('market')
        self.log.debug('market->' + market)
        lastCandle = _request.args.get('lastCandle')
        self.log.debug('lastCandle->' + lastCandle)

        rt_service = RT_Service()
        errormessage, result = rt_service.getDeltaValues(market, lastCandle)

        self.log.debug('RTController - getDeltas ENDS')
        return result
    # fin getDeltas
#