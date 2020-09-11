

function loadSessionName(_mydomain) {
    console.debug('->loadSessionName-> ' + '[' + new Date().toUTCString() + '] INIT');

    var params = {};

    console.debug('->' + _mydomain + '/etda/ajx/sessionName');
    $.get(_mydomain + "/etda/ajx/sessionName", params, function(data) {
        console.info('->loadSessionName-> errormessage= ' + data['serverdata']['errormessage'] + ', session= ' + data['serverdata']['fecha']);
        if('0' == data['serverdata']['errormessage']) {

            fecha = data['serverdata']['fecha'];
            sessionName = data['serverdata']['sessionName'];

            $("#eurofx-cardheader-a").html(fecha);
        }
        else {
            console.info('->loadSessionName-> Error requesting SessionName data:' + data['serverdata']['errormessage']);
        }

        console.debug('->loadSessionName-> ' + '[' + new Date().toUTCString() + '] ENDS AJX');
    });

    console.debug('->loadSessionName-> ' + '[' + new Date().toUTCString() + '] ENDS');
}//fin loadSessionName



function getGlobaldata(_mydomain) {
    console.debug('->getGlobaldata-> ' + '[' + new Date().toUTCString() + '] INIT');

    var params = {};
    params['sessionName'] = sessionName;
    console.debug('params: ' + JSON.stringify(params));

    console.debug('->' + _mydomain + '/etda/ajx/eurofx/globaldata');
    $.get(_mydomain + "/etda/ajx/eurofx/globaldata", params, function(data) {
        console.debug('->getGlobaldata-> errormessage= ' + data['serverdata']['errormessage']);
        if('0' == data['serverdata']['errormessage']) {

            $("#eurofx-glb-sessionname").html(sessionName);
            $("#eurofx-glb-buyprice").html(data['serverdata']['buy_price']);
            $("#eurofx-glb-sellprice").html(data['serverdata']['sell_price']);
            $("#eurofx-glb-voltotal").html(data['serverdata']['volume_total']);
        }
        else {
            console.info('->getGlobaldata-> Error requesting EuroFX global data:' + data['serverdata']['errormessage']);
        }

        console.debug('->getGlobaldata-> ' + '[' + new Date().toUTCString() + '] ENDS AJX');
    });

    console.debug('->getGlobaldata-> ' + '[' + new Date().toUTCString() + '] ENDS');
}//fin getGlobaldata



function getDeltas(_mydomain) {
    console.debug('->getDeltas-> ' + '[' + new Date().toUTCString() + '] INIT');

    const params = {};
    params['sessionName'] = sessionName;
    params['lastCandle'] = global_deltas_lastCandle;
    console.debug('params: ' + JSON.stringify(params));

    console.debug('->' + _mydomain + '/etda/ajx/eurofx/deltas');
    $.get(_mydomain + "/etda/ajx/eurofx/deltas", params, function(data) {
        console.debug('->getDeltas-> errormessage= ' + data['serverdata']['errormessage']);
        if('0' == data['serverdata']['errormessage']) {

            const theRecords = data['serverdata']['result'];
            console.info('getDeltas result length: ' + theRecords.length); //JSON.stringify(data.result));

            const lastRecord = theRecords.slice(-1).pop();
            console.debug('lastRecord: ' + JSON.stringify(lastRecord));
            global_deltas_lastCandle = lastRecord['candle_id']

            $("#eurofx-deltas-candle_id").html(lastRecord['candle_id']);
            $("#eurofx-deltas-delta").html(lastRecord['delta']);
            $("#eurofx-deltas-vol_avg").html(lastRecord['vol_avg']);
            $("#eurofx-deltas-delta_strong").html(lastRecord['delta_strong']);
            $("#eurofx-deltas-delta_p1").html(lastRecord['delta_period']);
            $("#eurofx-deltas-vol-filtered").html(lastRecord['vol_filtered']);

            if(0 != global_deltas_list.length) {
                global_deltas_list.pop();
            }
            global_deltas_list.push(...theRecords);

            const lastRecordGlobal = global_deltas_list.slice(-1).pop();
            console.debug('lastRecordGlobal: ' + JSON.stringify(lastRecordGlobal));

            //Update the chart
            updateChart_deltas();
        }
        else {
            console.info('->getDeltas-> Error requesting EuroFX deltas data:' + data['serverdata']['errormessage']);
        }

        console.debug('->getDeltas-> ' + '[' + new Date().toUTCString() + '] ENDS AJX');
    });

    console.debug('->getDeltas-> ' + '[' + new Date().toUTCString() + '] ENDS');
}//fin getDeltas


/**
* js: shift() elimina el primer elemento del array y lo retorna
* js: slice() devuelve una copia de una parte del array dentro de un nuevo array empezando por inicio hasta fin (fin no incluido). El array original no se modificará.
* js: pop() elimina el último elemento de un array y lo devuelve
* js: push() añade uno o más elementos al final de un array y devuelve la nueva longitud del array
*/

function updateChart_deltas() {

    let currentIndex = -1;
    if(global_deltas_list.length > global_deltas_list_last_length) {
        currentIndex = ((global_deltas_list.length - global_deltas_list_last_length) * -1) - 1;
    }
    global_deltas_list_last_length = global_deltas_list.length;

    while(CHART_DELTAS_X_AXIS_LENGTH <= chart_deltas.data.datasets[0].data.length) {
        console.info('shift');
        chart_deltas.data.labels.shift();
        chart_deltas.data.datasets[0].data.shift();
        chart_deltas.data.datasets[1].data.shift();
        chart_deltas.data.datasets[2].data.shift();
        chart_deltas.data.datasets[3].data.shift();
        chart_deltas.data.datasets[4].data.shift();
    }

    console.info('chart_deltas.data.datasets[0].data.length: ' + chart_deltas.data.datasets[0].data.length);
    console.info('currentIndex: ' + currentIndex);

    const newRecords = global_deltas_list.slice(currentIndex);

    chart_deltas.data.labels.pop();
    chart_deltas.data.datasets[0].data.pop();
    chart_deltas.data.datasets[1].data.pop();
    chart_deltas.data.datasets[2].data.pop();
    chart_deltas.data.datasets[3].data.pop();
    chart_deltas.data.datasets[4].data.pop();

    newRecords.forEach(record => {
        chart_deltas.data.labels.push(record['candle_id']);
        chart_deltas.data.datasets[0].data.push(parseFloat(record['delta']));
        chart_deltas.data.datasets[1].data.push(parseFloat(record['delta_period']));
        chart_deltas.data.datasets[2].data.push(parseInt(record['vol_filtered']));
        chart_deltas.data.datasets[3].data.push(0);
        chart_deltas.data.datasets[4].data.push(50);
    });

    console.info('delta_period: ' + JSON.stringify(chart_deltas.data.datasets[1].data));
    console.info('vol_filtered: ' + JSON.stringify(chart_deltas.data.datasets[2].data));
    chart_deltas.update();
    console.debug('chart_deltas updated');
}



//********----CHARTS----************

function defineChart_deltas() {

    var ctx = document.getElementById("chart_deltas");
    chart_deltas = new Chart(ctx, {
        type: 'line',
        data : {
            labels: [],
            datasets: [{
                label: "Delta",
                data:[],
                fill: false,
                borderColor: ['#3333ff'],
                backgroundColor: ['#3333ff'],
                borderWidth: 1,
                pointRadius: 0,
                yAxisID: 'y-axis-1'
            },
            {
                label: "Delta Pe = 1",
                data:[],
                fill: false,
                borderColor: ['#00ff00'],
                backgroundColor: ['#00ff00'],
                borderWidth: 1,
                pointRadius: 0,
                yAxisID: 'y-axis-1'
            },
            {
                label: "Vol >= 10",
                data:[],
                borderColor: ['#ff1a1a'],
                backgroundColor: ['#ff1a1a'],
                borderWidth: 1,
                barPercentage: 0.4,
                yAxisID: 'y-axis-2',
            },
            {
                label: "zero line",
                data:[],
                fill: false,
                borderColor: ['#ffffff'],
                backgroundColor: ['#ffffff'],
                borderWidth: 1,
                pointRadius: 0,
                yAxisID: 'y-axis-1'
            },
            {
                label: "50 line",
                data:[],
                fill: false,
                borderColor: ['#99ffb3'],
                backgroundColor: ['#99ffb3'],
                borderWidth: 1,
                pointRadius: 0,
                borderDash: [10, 10],
                yAxisID: 'y-axis-1'
            }]
        },
        options:{
            responsive: true,
            aspectRatio: 2,
			hoverMode: 'index',
			stacked: false,
			title: {
				display: true,
				text: 'Deltas and volume average'
			},
            scales: {
                yAxes: [{
                        ticks: {
                            beginAtZero:false,
                            min:-100,
                            max:100
                        },
                        type: 'linear', // only linear but allow scale type registration. This allows extensions to exist solely for log scale for instance
                        display: true,
                        position: 'left',
                        stepSize: 5,
                        id: 'y-axis-1',
                    },
                    {
                        ticks: {
                            beginAtZero:false,
                            min:0,
                            max:100
                        },
                        type: 'linear', // only linear but allow scale type registration. This allows extensions to exist solely for log scale for instance
                        display: true,
                        position: 'right',
                        id: 'y-axis-2',
                        gridLines: {
                            drawOnChartArea: false, // only want the grid lines for one axis to show up
                        }
                    }]
            }
        }
    });

    //chart_deltas.canvas.parentNode.style.height = '200px';
    //chart_deltas.canvas.parentNode.style.width = '400px';

}//fin defineChart_deltas



function initChartDataset_deltas() {

    for(x = 0; x <= CHART_DELTAS_X_AXIS_LENGTH; x++) {
        chart_deltas.data.labels.push(0);
        chart_deltas.data.datasets[0].data.push(0);
        chart_deltas.data.datasets[1].data.push(0);
        chart_deltas.data.datasets[2].data.push(0);
        chart_deltas.data.datasets[3].data.push(0);
        chart_deltas.data.datasets[4].data.push(0);
    }
}