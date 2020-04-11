#!/usr/bin/env python
""" Common File
    Variables Constantes con las querys Mariadb Sql.

    @author Alfredo Sanz
    @date April 2020
"""
# APIs imports

SQL_SELECT_GLOBAL_DATA =     """   SELECT sessiondate, market, buy_price, sell_price, vprofile, volume_total
                                    FROM trading_db.visu_global
                                    WHERE  sessiondate=%s
                                        AND market=%s 
                                    """