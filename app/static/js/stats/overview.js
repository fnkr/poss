var ctx = $("#chart").get(0).getContext("2d");

if (data.labels.length == 1) {
    var chart = new Chart(ctx).Bar(data);
} else {
    var chart = new Chart(ctx).Line(data);
}
