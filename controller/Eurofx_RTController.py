#!/usr/bin/env python
""" Controller
    -*-MAIN PAGE-*-    ->Controller for main page requests


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
from common import Constantes
from service.RT_Service import RT_Service



class Eurofx_RTController:


    def __init__(self):
        self.log = logging.getLogger('TDA_DataVisualizator')
    #


    def getTheTime(self):
        self.log.debug('Eurofx_RTController - getTheTime INIT')

        rt_service = RT_Service()
        result = rt_service.getThetime()

        self.log.debug('Eurofx_RTController - getTheTime ENDS')
        return result
    #


    def getSessionName(self):
        self.log.debug('Eurofx_RTController - getSessionName INIT')

        rt_service = RT_Service()
        result = rt_service.getTheSessionName()

        self.log.debug('Eurofx_RTController - getSessionName ENDS')
        return result
    #
#