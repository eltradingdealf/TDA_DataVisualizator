#!/usr/bin/env python
""" Controller
    -*-MAIN PAGE-*-    ->Service for Realtime controllers


    @author Alfredo Sanz
    @date April 2020
"""
# APIs imports
import logging
import json
from datetime import date, timedelta, datetime
import time

# local imports
from common import Util
from dao.RT_Dao import RT_Dao


class RT_Service:

    def __init__(self):
        self.log = logging.getLogger('TDA_DataVisualizator')
    #


    def getThetime(self):
        self.log.debug('RT_Service - getThetime INIT')

        result = Util.getCurrentTime_months()

        self.log.debug('RT_Service - getThetime ENDS')
        return result
    #


    def getTheSessionName(self):
        self.log.debug('RT_Service - getTheSessionName INIT')

        thetime = Util.getCurrentTime_months()

        self.log.debug('RT_Service - getTheSessionName ENDS')
        return thetime['intDate']
    #


    def getGlobalData(self, _market, _sessionName):
        self.log.debug('RT_Service - getGlobalData INIT')

        errormessage = '0'

        dao = RT_Dao()
        errormessage, result = dao.getGlobaldata(_sessionName, _market)

        self.log.debug('RT_Service - getGlobalData ENDS')
        return errormessage, result
    #fin getGlobalData
#