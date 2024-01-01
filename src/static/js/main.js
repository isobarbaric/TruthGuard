
function drawChart(pred) {
    const context = document.getElementById('chart');

    const data = {
        labels: [
            'pro-science',
            'conspiracy/pseudoscience'
        ],
        datasets: [{
            data: [
                pred['pro-science'],
                pred['conspiracy/pseudoscience']
            ],
            backgroundColor: [
                'rgb(0, 153, 76)',
                'rgb(204, 0, 0)'
            ],
            hoverOffset: 4
        }]
    };

    const config = {
        type: 'doughnut',
        data: data,
        options: {
            maintainAspectRatio: false,
            rotation: 45,
            circumference: 360,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            let label = context.label || '';
                            if (label) {
                                label += ': ';
                            }
                            label += context.parsed + '%';
                            return label;
                        }
                    }
                }                        
            }
        }
    };

    new Chart(context, config);
}
