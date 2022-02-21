//charts_data has been initialazed in index.php

//---------------------------temperature chart----------------------------
var temperature_ctx = document.getElementById("temperature_canvas");
var myChart = new Chart(temperature_ctx, {
type: 'line',
data: {
    labels: chart_temperature_dates,

    datasets: [{
        data: chart_temperature_values,
        borderColor: 'rgba(255,255,255,1)',
        borderWidth: 1
    }]
},
options: {
    title: {
        display: true,
        text: "Temperatura [°C]",
        fontColor: "#ffffff",
        fontFamily: "PoppinsLight",
        fontStyle: "normal",
        fontSize: 18
    },

    scales: {
        yAxes: [{

            ticks: {
                suggestedMin: 0,
                suggestedMax: 30,
                stepSize: 5,
                maxTicksLimit: 11
            },

            gridLines: {
                color: "rgba(255,255,255,0.2)"
            }
        }]
    },

    legend: {
        display: false
    },

    maintainAspectRatio: false
}
});
//------------------------------------------------------------------------

//-----------------------------humidity chart-----------------------------
var humidity_ctx = document.getElementById("humidity_canvas");
var myChart = new Chart(humidity_ctx, {
type: 'line',
data: {
    labels: chart_humidity_dates,

    datasets: [{
        data: chart_humidity_values,
        borderColor: 'rgba(255,255,255,1)',
        borderWidth: 1
    }]
},
options: {
    title: {
        display: true,
        text: "Wilgotność [%]",
        fontColor: "#ffffff",
        fontFamily: "PoppinsLight",
        fontStyle: "normal",
        fontSize: 18
    },

    scales: {
        yAxes: [{

            ticks: {
                suggestedMin: 40,
                suggestedMax: 100,
                stepSize: 20,
                maxTicksLimit: 11
            },

            gridLines: {
                color: "rgba(255,255,255,0.2)"
            }
        }]
    },

    legend: {
        display: false
    },

    maintainAspectRatio: false
}
});
//------------------------------------------------------------------------