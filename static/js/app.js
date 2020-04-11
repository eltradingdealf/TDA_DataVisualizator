

function loadSessionName(_mydomain) {
    console.log('->loadSessionName-> ' + '[' + new Date().toUTCString() + '] INIT');

    var params = {};

    console.log('->' + _mydomain + '/etda/ajx/sessionName');
    $.get(_mydomain + "/etda/ajx/sessionName", params, function(data) {
        console.log('->loadSessionName-> errormessage= ' + data['serverdata']['errormessage'] + ', session= ' + data['serverdata']['fecha']);
        if('0' == data['serverdata']['errormessage']) {

            fecha = data['serverdata']['fecha'];
            sessionName = data['serverdata']['sessionName'];

            $("#eurofx-cardheader-a").html(fecha);
        }
        else {
            console.log('->loadSessionName-> Error requesting SessionName data:' + data['serverdata']['errormessage']);
        }

        console.log('->loadSessionName-> ' + '[' + new Date().toUTCString() + '] ENDS AJX');
    });

    console.log('->loadSessionName-> ' + '[' + new Date().toUTCString() + '] ENDS');
}//fin loadCardsCurrentDataValues



function getGlobaldata(_mydomain) {
    console.log('->getGlobaldata-> ' + '[' + new Date().toUTCString() + '] INIT');

    var params = {};
    params['sessionName'] = sessionName;
    console.log('params: ' + JSON.stringify(params));

    console.log('->' + _mydomain + '/etda/ajx/eurofx/globaldata');
    $.get(_mydomain + "/etda/ajx/eurofx/globaldata", params, function(data) {
        console.log('->getGlobaldata-> errormessage= ' + data['serverdata']['errormessage']);
        if('0' == data['serverdata']['errormessage']) {

            $("#eurofx-glb-sessionname").html(sessionName);
            $("#eurofx-glb-buyprice").html(data['serverdata']['buy_price']);
            $("#eurofx-glb-sellprice").html(data['serverdata']['sell_price']);
            $("#eurofx-glb-voltotal").html(data['serverdata']['volume_total']);
        }
        else {
            console.log('->getGlobaldata-> Error requesting EuroFX global data:' + data['serverdata']['errormessage']);
        }

        console.log('->getGlobaldata-> ' + '[' + new Date().toUTCString() + '] ENDS AJX');
    });

    console.log('->getGlobaldata-> ' + '[' + new Date().toUTCString() + '] ENDS');
}//fin loadCardsCurrentDataValues