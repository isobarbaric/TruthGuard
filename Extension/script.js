
chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
    let url = tabs[0].url;

    console.log(url);

    const url_display = document.getElementById('article-url');
    url_display.textContent = url;

    const request = getPrediction(url);

    request.then(data => {
        drawChart(data['confidence_level']);
        typePrediction(data['prediction']);
    });
});

async function getPrediction(article_url) {
    const base_url = 'https://cors.eu.org/https://covid19-classifier-app.herokuapp.com/API/';
    const response = await fetch(base_url + article_url, {
        method: 'GET',
        headers: {
            'content-type': 'application/json'
        }
    });
    let json_data = await response.json();
    return json_data;
}

// whenever a new website is reached, use this stuff

async function typePrediction(content) {
    const delay = millis => new Promise((resolve, reject) => {
        setTimeout(_ => resolve(), millis)
    });

    window.addEventListener("load", typing(content, 0));

    async function typing(content, ptr) {
        if (ptr == content.length) {
            return ''
        }
        document.getElementById('prediction').innerHTML += content.charAt(ptr);
        await delay(120);
        typing(content, ptr+1);
    }
}

function drawChart(confidence_percentages) {
    // Chart.defaults.color = "#000";

    const context = document.getElementById('donut');

    const data = {
        labels: [
            'pro-science',
            'conspiracy/pseudoscience'
        ],
        datasets: [{
            // label: 'My First Dataset',
            data: [
                confidence_percentages['pro-science'] * 100,
                confidence_percentages['conspiracy/pseudoscience'] * 100
            ],
            backgroundColor: [
                'rgb(0, 153, 76)',
                'rgb(204, 0, 0)'
            ],
            hoverOffset: 3
        }]
    };

    const config = {
        type: 'pie',
        data: data,
        options: {
            maintainAspectRatio: false,
            // rotation: 270,
            // circumference: 180,
            rotation: 0,
            circumference: 360,
            legend: {
                position: 'bottom'
            },
            plugins: {
                // datalabels: {
                //     formatter: (value, ctx) => {
                //         let sum = ctx.dataset._meta[0].total;
                //         let percentage = (value * 100 / sum).toFixed(2) + "%";
                //         return percentage;
                //     },
                //     color: '#fff'
                // }
                datalabels: {
                    formatter: (value, ctx) => {
                    let datasets = ctx.chart.data.datasets;
                    if (datasets.indexOf(ctx.dataset) === datasets.length - 1) {
                        let sum = datasets[0].data.reduce((a, b) => a + b, 0);
                        let percentage = Math.round((value / sum) * 100) + '%';
                        return percentage;
                    } else {
                        return percentage;
                    }
                    },
                    color: '#fff',
                }
            }
        }
    };

    const canvas_req = new Chart(context, config);
}