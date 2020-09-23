

function loadSessionName(_mydomain, _market) {
    console.debug('->loadSessionName-> ' + '[' + new Date().toUTCString() + '] INIT');

    var params = {};

    console.debug('->' + _mydomain + '/etda/ajx/sessionName');
    $.get(_mydomain + "/etda/ajx/sessionName", params, function(data) {
        console.info('->loadSessionName-> errormessage= ' + data['serverdata']['errormessage'] + ', session= ' + data['serverdata']['fecha']);
        if('0' == data['serverdata']['errormessage']) {

            fecha = data['serverdata']['fecha'];
            sessionName = data['serverdata']['sessionName'];

            const cabecera = fecha + ' * ' + _market + ' *';
            $("#cardheader_a_h1").text(cabecera);
        }
        else {
            console.info('->loadSessionName-> Error requesting SessionName data:' + data['serverdata']['errormessage']);
        }

        console.debug('->loadSessionName-> ' + '[' + new Date().toUTCString() + '] ENDS AJX');
    });

    console.debug('->loadSessionName-> ' + '[' + new Date().toUTCString() + '] ENDS');
}//fin loadSessionName



function getGlobaldata(_mydomain, _market) {
    console.debug('->getGlobaldata-> ' + '[' + new Date().toUTCString() + '] INIT');

    var params = {};
    params['sessionName'] = sessionName;
    params['market'] = _market;
    console.debug('params: ' + JSON.stringify(params));

    console.debug('->' + _mydomain + '/etda/ajx/globaldata');
    $.get(_mydomain + "/etda/ajx/globaldata", params, function(data) {
        console.debug('->getGlobaldata-> errormessage= ' + data['serverdata']['errormessage']);
        if('0' == data['serverdata']['errormessage']) {

            $("#glb-sessionname").html(sessionName);
            $("#glb-buyprice").html(data['serverdata']['buy_price']);
            $("#glb-sellprice").html(data['serverdata']['sell_price']);
            $("#glb-voltotal").html(data['serverdata']['volume_total']);
            $("#glb-speed").html(data['serverdata']['speed']);
            $("#deltas-speed-i").html(data['serverdata']['speed']);
        }
        else {
            console.info('->getGlobaldata-> Error requesting Global data:' + data['serverdata']['errormessage']);
        }

        console.debug('->getGlobaldata-> ' + '[' + new Date().toUTCString() + '] ENDS AJX');
    });

    console.debug('->getGlobaldata-> ' + '[' + new Date().toUTCString() + '] ENDS');
}//fin getGlobaldata



function getDeltas(_mydomain, _market) {
    console.info('->getDeltas-> ' + '[' + new Date().toUTCString() + '] INIT');

    const params = {};
    params['sessionName'] = sessionName;
    params['market'] = _market;
    params['lastCandle'] = global_deltas_lastCandle;
    console.debug('params: ' + JSON.stringify(params));

    console.debug('->' + _mydomain + '/etda/ajx/deltas');
    $.get(_mydomain + "/etda/ajx/deltas", params, function(data) {
        console.debug('->getDeltas-> errormessage= ' + data['serverdata']['errormessage']);
        if('0' == data['serverdata']['errormessage']) {

            const theRecords = data['serverdata']['result'];
            console.info('getDeltas result length: ' + theRecords.length); //JSON.stringify(data.result));

            const lastRecord = theRecords.slice(-1).pop();
            console.debug('lastRecord: ' + JSON.stringify(lastRecord));
            global_deltas_lastCandle = lastRecord['candle_id']

            $("#deltas-candle_id").html(lastRecord['candle_id']);
            $("#deltas-delta").html(lastRecord['delta']);
            $("#deltas-delta_p1").html(lastRecord['delta_period']);
            $("#deltas-vol_avg").html(lastRecord['vol_avg']);
            $("#deltas-speed-p0").html(lastRecord['speed']);
            $("#deltas-vol-filtered").html(lastRecord['vol_filtered']);
            $("#deltas-delta_strong").html(lastRecord['delta_strong']);
            $("#deltas-delta_WE-AVG_strong").html(lastRecord['delta_weight_avg_strong']);

            if(0 != global_deltas_list.length) {
                global_deltas_list.pop();
                global_speed_list.pop();
            }
            global_deltas_list.push(...theRecords);
            global_speed_list.push(...theRecords);

            //Update the chart;
            updateChart_deltas();
            updateChart_speed();
        }
        else {
            console.info('->getDeltas-> Error requesting Deltas data:' + data['serverdata']['errormessage']);
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
    console.debug('updateChart_deltas init ');
    let currentIndex = -1;
    if(global_deltas_list.length > global_deltas_list_last_length) {
        currentIndex = ((global_deltas_list.length - global_deltas_list_last_length) * -1) - 1;
    }
    global_deltas_list_last_length = global_deltas_list.length;

    while(CHART_DELTAS_X_AXIS_LENGTH <= chart_deltas.data.datasets[0].data.length) {
        console.debug(' updateChart_deltas shift');
        chart_deltas.data.labels.shift();
        chart_deltas.data.datasets[0].data.shift();
        chart_deltas.data.datasets[1].data.shift();
        chart_deltas.data.datasets[2].data.shift();
        chart_deltas.data.datasets[3].data.shift();
        chart_deltas.data.datasets[4].data.shift();
    }

    console.debug('chart_deltas.data.datasets[0].data.length: ' + chart_deltas.data.datasets[0].data.length);
    console.debug('updateChart_deltas currentIndex: ' + currentIndex);

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

    chart_deltas.update();
    console.debug('updateChart_deltas ends: ');
}



function updateChart_speed() {
    console.debug('updateChart_speed init');

    let currentIndex = -1;
    if(global_speed_list.length > global_speed_list_last_length) {
        currentIndex = ((global_speed_list.length - global_speed_list_last_length) * -1) - 1;
    }
    global_speed_list_last_length = global_speed_list.length;

    while(CHART_DELTAS_X_AXIS_LENGTH <= chart_speed.data.datasets[0].data.length) {
        console.debug('updateChart_speed shift');
        chart_speed.data.labels.shift();
        chart_speed.data.datasets[0].data.shift();
        chart_speed.data.datasets[1].data.shift();
    }

    console.debug('chart_speed.data.datasets[0].data.length: ' + chart_speed.data.datasets[0].data.length);
    console.debug('updateChart_speed currentIndex: ' + currentIndex);

    const newRecords = global_speed_list.slice(currentIndex);

    chart_speed.data.labels.pop();
    chart_speed.data.datasets[0].data.pop();
    chart_speed.data.datasets[1].data.pop();

    newRecords.forEach(record => {
        chart_speed.data.labels.push(record['candle_id']);
        chart_speed.data.datasets[0].data.push(parseFloat(record['speed']));
        chart_speed.data.datasets[1].data.push(parseFloat(record['vol_avg']));
    });

    chart_speed.update();
    console.debug('updateChart_speed ends');
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
                label: "Delta Pe = 3",
                data:[],
                fill: false,
                borderColor: ['#00ff00'],
                backgroundColor: ['#00ff00'],
                borderWidth: 1,
                pointRadius: 0,
                yAxisID: 'y-axis-1'
            },
            {
                label: "Vol >= x",
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
            events: ['click'],
            //aspectRatio: 2,
            maintainAspectRatio: false,
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
                            min: CHART_DELTAS_SETUP_AXIS_Y2_MIN,
                            max: CHART_DELTAS_SETUP_AXIS_Y2_MAX
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
}//fin defineChart_deltas



function initChartDataset_deltas() {

    for(x = 0; x <= CHART_DELTAS_X_AXIS_LENGTH; x++) {
        chart_deltas.data.labels.push(0);
        chart_deltas.data.datasets[0].data.push(0);
        chart_deltas.data.datasets[1].data.push(0);
        chart_deltas.data.datasets[2].data.push(0);
        chart_deltas.data.datasets[3].data.push(0);
        chart_deltas.data.datasets[4].data.push(50);
    }
}



function defineChart_speed() {

    var ctx = document.getElementById("chart_speed");
    chart_speed = new Chart(ctx, {
        type: 'line',
        data : {
            labels: [],
            datasets: [{
                label: "Speed p=0",
                data:[],
                fill: false,
                borderColor: ['#00ff00'],
                backgroundColor: ['#00ff00'],
                borderWidth: 1,
                pointRadius: 0,
                yAxisID: 'y-axis-1'
            },
            {
                label: "Vol avg",
                data:[],
                fill: false,
                borderColor: ['#ff1a1a'],
                backgroundColor: ['#ff1a1a'],
                borderWidth: 1,
                pointRadius: 0,
                yAxisID: 'y-axis-2',
            }]
        },
        options:{
            responsive: true,
            events: ['click'],
            //aspectRatio: 2,
            maintainAspectRatio: false,
			hoverMode: 'index',
			stacked: false,
			title: {
				display: true,
				text: 'Pace of tape'
			},
            scales: {
                yAxes: [{
                        ticks: {
                            beginAtZero:true,
                            min: CHART_SPEED_SETUP_AXIS_Y1_MIN,
                            max: CHART_SPEED_SETUP_AXIS_Y1_MAX
                        },
                        type: 'linear', // only linear but allow scale type registration. This allows extensions to exist solely for log scale for instance
                        display: true,
                        position: 'left',
                        id: 'y-axis-1',
                    },
                    {
                        ticks: {
                            beginAtZero:true,
                            min: CHART_SPEED_SETUP_AXIS_Y2_MIN,
                            max: CHART_SPEED_SETUP_AXIS_Y2_MAX
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
}//fin defineChart_speed



function initChartDataset_speed() {

    for(x = 0; x <= CHART_DELTAS_X_AXIS_LENGTH; x++) {
        chart_speed.data.labels.push(0);
        chart_speed.data.datasets[0].data.push(0);
        chart_speed.data.datasets[1].data.push(0);
    }
}