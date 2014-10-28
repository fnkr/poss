var ctx = $("#chart").get(0).getContext("2d");

if (data.labels.length == 1) {
    data.labels.unshift('');
    for (i = 0; i < data.datasets.length; i++) {
        try {
            data.datasets[i].data.unshift(0);
        } catch(e) {
        }
    }
}
var chart = new Chart(ctx).Line(data);
