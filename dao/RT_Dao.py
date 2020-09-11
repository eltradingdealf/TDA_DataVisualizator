#!/usr/bin/env python
""" Clase para operar contra BD en relacion
    a datos de futuros con precios en formato decimal.

    @author Alfredo Sanz
    @date April 2020
"""

# APIs imports
import logging
import pymysql

# local imports
import ConfigRoot
from common import query_sql
from common import Constantes


class RT_Dao():
    """
    * Constructor
    """
    def __init__(self):
        self.log = logging.getLogger('TDA_DataVisualizator')
    # construct

    """
    * Obtiene los datos globales para un market determinado.
    *
    * @return errormessage, result <dict>{int, int}
    """

    def getGlobaldata(self, _sessionName, _market):
        """ return result {'buy_price, 'sell_price'} """

        self.log.debug("***RT_Dao  getGlobaldata:" + _market + " INIT")
        self.log.debug('=====mysql, mysql_Query Current_prices-> date:' + str(_sessionName))

        errormessage = '0'
        result = {'sell_price': '0.0', 'buy_price': '0.0', 'vprofile': '', 'volume_total':'0'}
        connection = None

        try:
            self.log.debug('=====mysql, getGlobaldata trap before conn')
            connection = pymysql.connect(host="127.0.0.1",
                                         port=3306,
                                         user=ConfigRoot.db_mariadb_user,
                                         passwd=ConfigRoot.db_mariadb_pass,
                                         db="trading_db",
                                         charset='utf8',
                                         cursorclass=pymysql.cursors.DictCursor)

            self.log.debug('=====mysql, getGlobaldata trap after conn')

            with connection.cursor() as cursor:
                sql = query_sql.SQL_SELECT_GLOBAL_DATA

                cursor.execute(sql, (_sessionName, _market))
                rs = cursor.fetchall()
                for row in rs:
                    result['buy_price'] = str(row['buy_price'])
                    result['sell_price'] = str(row['sell_price'])
                    result['vprofile'] = str(row['vprofile'])
                    result['volume_total'] = str(row['volume_total'])
                #
            #
            self.log.debug('=====mysql, getGlobaldata trap after harvest')


        except Exception as ex:
            self.log.error("Error getGlobaldata from MariaDB  " + _market, ex)
            errormessage = "Error getGlobaldata from MariaDB  " + _market + " : " + repr(ex)
        finally:
            if connection:
                connection.close()
            #
        #

        self.log.debug("***RT_Dao  getGlobaldata:" + _market + " ENDS")
        return errormessage, result
    #fin getGlobaldata



    def getDeltaValues(self, _market, _lastCandle):
        """ return result [{'candle_id, 'delta', 'vol_avg', 'delta_strong'},{...}] """

        self.log.debug("***RT_Dao  getDeltaValues:" + _lastCandle + " INIT")

        errormessage = '0'
        result = []
        connection = None

        try:
            self.log.debug('=====mysql, getDeltaValues trap before conn')
            connection = pymysql.connect(host="127.0.0.1",
                                         port=3306,
                                         user=ConfigRoot.db_mariadb_user,
                                         passwd=ConfigRoot.db_mariadb_pass,
                                         db="trading_db",
                                         charset='utf8',
                                         cursorclass=pymysql.cursors.DictCursor)

            self.log.debug('=====mysql, getDeltaValues trap after conn')

            with connection.cursor() as cursor:
                sql = ''
                if _market == Constantes.MARKET_EUROFX:
                    sql = query_sql.SQL_SELECT_DELTAS_EUROFX
                else:
                    #TODO
                    sql = ''
                #

                cursor.execute(sql, (_lastCandle))
                rs = cursor.fetchall()
                for row in rs:
                    record = {
                        'candle_id': row['candle_id'],
                        'delta': row['delta'],
                        'vol_avg': row['vol_avg'],
                        'delta_strong': row['delta_strong'],
                        'delta_period': row['data03'],
                        'vol_filtered': row['data04']
                    }

                    result.append(record)
                #
            #
            self.log.debug('=====mysql, getDeltaValues trap after harvest')


        except Exception as ex:
            self.log.error("Error getDeltaValues from MariaDB ", ex)
            errormessage = "Error getDeltaValues from MariaDB " + repr(ex)
        finally:
            if connection:
                connection.close()
            #
        #

        self.log.debug("***RT_Dao  getDeltaValues")
        return errormessage, result
    #fin getDeltaValues
# class
