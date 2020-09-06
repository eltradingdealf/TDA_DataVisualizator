#!/usr/bin/env python
""" Main for web project

    @author Alfredo Sanz
    @date Dec 2019
"""
import logging

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_restful import Api

#propios
from controller.Eurofx_RTController import Eurofx_RTController

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
        'route': u'/etda/ajx/eurofx/globaldata',
        'methods': u'GET'
    },
    {
        'route': u'/etda/ajx/eurofx/deltas',
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

            resultData['fecha'] = "10-10-2019"

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
            controller = Eurofx_RTController()
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
    app.logger.info("---gotoEurofx ENDS")
    return render_template('market-eurofx.html', datas=tem_values)
# fin gotoEurofx



@app.route('/etda/ajx/sessionName', methods=['GET'])
def getSessionName():
    app.logger.debug("---ajx GET getSessionName INIT")

    tem_values = {'errormessage': '0'}

    try:
        controller = Eurofx_RTController()

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



@app.route('/etda/ajx/eurofx/globaldata', methods=['GET'])
def getEurofxGlobaldata():
    app.logger.debug("---ajx GET getEurofxGlobaldata INIT")

    tem_values = {'errormessage': '0'}

    try:
        controller = Eurofx_RTController()

        result = controller.getGlobalData(request)
        tem_values.update(result)

    except Exception as Argument:
        app.logger.error(repr(Argument))
        app.logger.exception("@Error")
        tem_values['errormessage'] = '*Error Ajx GET getSessionName: ' + repr(Argument)

    app.logger.debug("---ajx GET getEurofxGlobaldata ENDS")
    return jsonify({'serverdata': tem_values})
# fin getEurofxGlobaldata



@app.route('/etda/ajx/eurofx/deltas', methods=['GET'])
def getEurofxDeltas():
    app.logger.debug("---ajx GET getEurofxDeltas INIT")

    tem_values = {'errormessage': '0'}

    try:
        controller = Eurofx_RTController()

        result = controller.getDeltas(request)
        tem_values['result'] = result

    except Exception as Argument:
        app.logger.error(repr(Argument))
        app.logger.exception("@Error")
        tem_values['errormessage'] = '*Error Ajx GET getEurofxDeltas: ' + repr(Argument)

    app.logger.debug("---ajx GET getEurofxDeltas ENDS")
    return jsonify({'serverdata': tem_values})
# fin getEurofxDeltas



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
            # controller = Mainpage_Controller()
            # errormessage, resultData = controller.datosBasicosPortada(request, u'PORTADA')

            resultData['fecha'] = "20-01-2020"

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
            # controller = Mainpage_Controller()
            # errormessage, resultData = controller.datosBasicosPortada(request, u'PORTADA')

            resultData['fecha'] = "20-01-2020"

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
    app.logger.info("---gotoNasdaq ENDS")
    return render_template('market-nasdaq.html', datas=tem_values)
# fin gotoNasdaq



@app.route("/etda/web/cl")
def gotoCL():
    app.logger.info("---gotoCL INIT")

    errormessage = '0'
    tem_values = {}
    resultData = {}

    try:
        app.logger.debug(request.url_root)

        # Call to Controller
        try:
            # controller = Mainpage_Controller()
            # errormessage, resultData = controller.datosBasicosPortada(request, u'PORTADA')

            resultData['fecha'] = "20-01-2020"

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
    app.logger.info("---gotoCL ENDS")
    return render_template('market-cl.html', datas=tem_values)
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
            # controller = Mainpage_Controller()
            # errormessage, resultData = controller.datosBasicosPortada(request, u'PORTADA')

            resultData['fecha'] = "20-01-2020"

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
    app.logger.info("---gotoDAX ENDS")
    return render_template('market-dax.html', datas=tem_values)
# fin gotoDAX


