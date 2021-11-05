#!/usr/bin/env python
""" Main for web project

    @author Alfredo Sanz
    @date Dec 2019
    @update Sept 2020
"""
import logging

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_restful import Api

#propios
from controller.RTController import RTController

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
app.config['TEMPLATES_AUTO_RELOAD'] = True
logging.basicConfig(filename='Python_VISUALIZATOR.log', level=logging.DEBUG)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# *******************************************************
# API RESTFULL WITH FLASK-RESTFUL LIB
# *******************************************************
api = Api(app)

# Example
# api.add_resource(apiController, '/etda/api/v1/data')


# *******************************************************
# RESTFUL API AVALAIBLE
# *******************************************************
api_routes = [
    {
        'route': u'/etda/ajx/sessionName',
        'methods': u'GET'
    },
    {
        'route': u'/etda/ajx/globaldata',
        'methods': u'GET'
    },
    {
        'route': u'/etda/ajx/deltas',
        'methods': u'GET'
    }
]


@app.route('/etda/api/v1/explore-api', methods=['GET'])
def get_api():
    return jsonify({'api-routes': api_routes})


# *******************************************************
##WEB REQUEST WITH FLASK
# *******************************************************

@app.route("/")
def hello():
    app.logger.info("---default INIT")
    return "Alfredo Tools."


# fin hello


@app.route("/etda/web/")
def helloWeb():
    app.logger.info("---helloWeb INIT")

    errormessage = '0'
    tem_values = {}
    resultData = {}

    try:
        app.logger.debug(request.url_root)

        # Call to Controller
        try:
            # controller = Mainpage_Controller()
            # errormessage, resultData = controller.datosBasicosPortada(request, u'PORTADA')

            resultData['fecha'] = "10-10-2021"

        except Exception as err:
            app.logger.error(str(err))
            app.logger.exception("@Error")
        #

        tem_values = {'errormessage': errormessage,
                      'domain': request.url_root[:-1],  # quita la barra final
                      'fecha': resultData['fecha']
                      }

    except Exception as err:
        app.logger.error(str(err))
        app.logger.exception("@Error")
        errormessage = '*Error Redirecting index: ' + str(err)
    #

    # logging.info('tem_values=' + repr(tem_values))
    app.logger.info("---helloWeb ENDS")
    return render_template('index.html', datas=tem_values)
# fin helloWeb



@app.route("/etda/web/eurofx")
def gotoEurofx():
    app.logger.info("---gotoEurofx INIT")

    errormessage = '0'
    tem_values = {}
    resultData = {}

    try:
        app.logger.debug(request.url_root)

        # Call to Controller
        try:
            controller = RTController()
            thetime = controller.getTheTime()

            resultData['fecha'] = thetime['strFecha']
            resultData['sessionName'] = controller.getSessionName()
            resultData['CHART_X_AXIS_LENGTH'] = 40
            resultData['CHART_DELTAS_SETUP_AXIS_Y2_MIN'] = 35
            resultData['CHART_DELTAS_SETUP_AXIS_Y2_MAX'] = 200
            resultData['CHART_SPEED_SETUP_AXIS_Y1_MIN'] = 30
            resultData['CHART_SPEED_SETUP_AXIS_Y1_MAX'] = 150
            resultData['CHART_SPEED_SETUP_AXIS_Y2_MIN'] = 0
            resultData['CHART_SPEED_SETUP_AXIS_Y2_MAX'] = 6
            resultData['CHART_STRONG_SETUP_AXIS_Y1_MIN'] = -200
            resultData['CHART_STRONG_SETUP_AXIS_Y1_MAX'] = 200

        except Exception as err:
            app.logger.error(str(err))
            app.logger.exception("@Error")
        #

        tem_values = {'errormessage': errormessage,
                      'domain': request.url_root[:-1]  # quita la barra final
                      }
        tem_values.update(resultData)

    except Exception as err:
        app.logger.error(str(err))
        app.logger.exception("@Error")
        errormessage = '*Error Redirecting index: ' + str(err)
    #

    # logging.info('tem_values=' + repr(tem_values))
    app.logger.info("---gotoEurofx ENDS")
    return render_template('market-eurofx.html', datas=tem_values)
# fin gotoEurofx



@app.route("/etda/web/sp500")
def gotoSp500():
    app.logger.info("---gotoSp500 INIT")

    errormessage = '0'
    tem_values = {}
    resultData = {}

    try:
        app.logger.debug(request.url_root)

        # Call to Controller
        try:
            controller = RTController()
            thetime = controller.getTheTime()

            resultData['fecha'] = thetime['strFecha']
            resultData['sessionName'] = controller.getSessionName()

        except Exception as err:
            app.logger.error(str(err))
            app.logger.exception("@Error")
        #

        tem_values = {'errormessage': errormessage,
                      'domain': request.url_root[:-1]  # quita la barra final
                      }
        tem_values.update(resultData)

    except Exception as err:
        app.logger.error(str(err))
        app.logger.exception("@Error")
        errormessage = '*Error Redirecting index: ' + str(err)
    #

    # logging.info('tem_values=' + repr(tem_values))
    app.logger.info("---gotoSp500 ENDS")
    return render_template('market-sp500.html', datas=tem_values)
# fin gotoSp500



@app.route("/etda/web/nasdaq")
def gotoNasdaq():
    app.logger.info("---gotoNasdaq INIT")

    errormessage = '0'
    tem_values = {}
    resultData = {}

    try:
        app.logger.debug(request.url_root)

        # Call to Controller
        try:
            controller = RTController()
            thetime = controller.getTheTime()

            resultData['fecha'] = thetime['strFecha']
            resultData['sessionName'] = controller.getSessionName()

        except Exception as err:
            app.logger.error(str(err))
            app.logger.exception("@Error")
        #

        tem_values = {'errormessage': errormessage,
                      'domain': request.url_root[:-1]  # quita la barra final
                      }
        tem_values.update(resultData)

    except Exception as err:
        app.logger.error(str(err))
        app.logger.exception("@Error")
        errormessage = '*Error Redirecting index: ' + str(err)
    #

    # logging.info('tem_values=' + repr(tem_values))
    app.logger.info("---gotoNasdaq ENDS")
    return render_template('market-nasdaq.html', datas=tem_values)
# fin gotoNasdaq



@app.route("/etda/web/stoxx50")
def gotoSTOXX50():
    app.logger.info("---gotoSTOXX50 INIT")

    errormessage = '0'
    tem_values = {}
    resultData = {}

    try:
        app.logger.debug(request.url_root)

        # Call to Controller
        try:
            controller = RTController()
            thetime = controller.getTheTime()

            resultData['fecha'] = thetime['strFecha']
            resultData['sessionName'] = controller.getSessionName()
            resultData['CHART_X_AXIS_LENGTH'] = 40
            resultData['CHART_DELTAS_SETUP_AXIS_Y2_MIN'] = 35
            resultData['CHART_DELTAS_SETUP_AXIS_Y2_MAX'] = 200
            resultData['CHART_SPEED_SETUP_AXIS_Y1_MIN'] = 30
            resultData['CHART_SPEED_SETUP_AXIS_Y1_MAX'] = 150
            resultData['CHART_SPEED_SETUP_AXIS_Y2_MIN'] = 0
            resultData['CHART_SPEED_SETUP_AXIS_Y2_MAX'] = 6
            resultData['CHART_STRONG_SETUP_AXIS_Y1_MIN'] = -200
            resultData['CHART_STRONG_SETUP_AXIS_Y1_MAX'] = 200

        except Exception as err:
            app.logger.error(str(err))
            app.logger.exception("@Error")
        #

        tem_values = {'errormessage': errormessage,
                      'domain': request.url_root[:-1]  # quita la barra final
                      }
        tem_values.update(resultData)

    except Exception as err:
        app.logger.error(str(err))
        app.logger.exception("@Error")
        errormessage = '*Error Redirecting index: ' + str(err)
    #

    # logging.info('tem_values=' + repr(tem_values))
    app.logger.info("---gotoSTOXX50 ENDS")
    return render_template('market-stoxx50.html', datas=tem_values)
# fin gotoCL


@app.route("/etda/web/dax")
def gotoDAX():
    app.logger.info("---gotoDAX INIT")

    errormessage = '0'
    tem_values = {}
    resultData = {}

    try:
        app.logger.debug(request.url_root)

        # Call to Controller
        try:
            controller = RTController()
            thetime = controller.getTheTime()

            resultData['fecha'] = thetime['strFecha']
            resultData['sessionName'] = controller.getSessionName()

        except Exception as err:
            app.logger.error(str(err))
            app.logger.exception("@Error")
        #

        tem_values = {'errormessage': errormessage,
                      'domain': request.url_root[:-1]  # quita la barra final
                      }
        tem_values.update(resultData)

    except Exception as err:
        app.logger.error(str(err))
        app.logger.exception("@Error")
        errormessage = '*Error Redirecting index: ' + str(err)
    #

    # logging.info('tem_values=' + repr(tem_values))
    app.logger.info("---gotoDAX ENDS")
    return render_template('market-dax.html', datas=tem_values)
# fin gotoDAX


@app.route("/etda/web/bund")
def gotoBUND():
    app.logger.info("---gotoBUND INIT")

    errormessage = '0'
    tem_values = {}
    resultData = {}

    try:
        app.logger.debug(request.url_root)

        # Call to Controller
        try:
            controller = RTController()
            thetime = controller.getTheTime()

            resultData['fecha'] = thetime['strFecha']
            resultData['sessionName'] = controller.getSessionName()

        except Exception as err:
            app.logger.error(str(err))
            app.logger.exception("@Error")
        #

        tem_values = {'errormessage': errormessage,
                      'domain': request.url_root[:-1]  # quita la barra final
                      }
        tem_values.update(resultData)

    except Exception as err:
        app.logger.error(str(err))
        app.logger.exception("@Error")
        errormessage = '*Error Redirecting index: ' + str(err)
    #

    # logging.info('tem_values=' + repr(tem_values))
    app.logger.info("---gotoBUND ENDS")
    return render_template('market-bund.html', datas=tem_values)
# fin gotoBUND


@app.route('/etda/ajx/sessionName', methods=['GET'])
def getSessionName():
    app.logger.debug("---ajx GET getSessionName INIT")

    tem_values = {'errormessage': '0'}

    try:
        controller = RTController()

        thetime = controller.getTheTime()
        tem_values['fecha'] = thetime['strFecha']
        tem_values['sessionName'] = controller.getSessionName()

    except Exception as Argument:
        app.logger.error(repr(Argument))
        app.logger.exception("@Error")
        tem_values['errormessage'] = '*Error Ajx GET getSessionName: ' + repr(Argument)

    app.logger.debug("---ajx GET getSessionName ENDS")
    return jsonify({'serverdata': tem_values})
# fin getSessionName



@app.route('/etda/ajx/globaldata', methods=['GET'])
def getGlobaldata():
    app.logger.debug("---ajx GET getGlobaldata INIT")

    tem_values = {'errormessage': '0'}

    try:
        controller = RTController()

        result = controller.getGlobalData(request)
        tem_values.update(result)

    except Exception as Argument:
        app.logger.error(repr(Argument))
        app.logger.exception("@Error")
        tem_values['errormessage'] = '*Error Ajx GET getSessionName: ' + repr(Argument)

    app.logger.debug("---ajx GET getGlobaldata ENDS")
    return jsonify({'serverdata': tem_values})
# fin getGlobaldata



@app.route('/etda/ajx/deltas', methods=['GET'])
def getDeltas():
    app.logger.debug("---ajx GET getDeltas INIT")

    tem_values = {'errormessage': '0'}

    try:
        controller = RTController()

        result = controller.getDeltas(request)
        tem_values['result'] = result

    except Exception as Argument:
        app.logger.error(repr(Argument))
        app.logger.exception("@Error")
        tem_values['errormessage'] = '*Error Ajx GET getDeltas: ' + repr(Argument)

    app.logger.debug("---ajx GET getDeltas ENDS")
    return jsonify({'serverdata': tem_values})
# fin getDeltas





