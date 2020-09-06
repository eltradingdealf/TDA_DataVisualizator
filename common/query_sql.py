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

SQL_SELECT_DELTAS_EUROFX =      """ SELECT sessiondate, candle_id, delta, vol_avg, delta_strong
                                    FROM trading_db.visu_datacalc_feuro
                                    WHERE candle_id >= %s                                        
                                """