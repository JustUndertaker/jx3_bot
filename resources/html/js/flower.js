function handle(data) {
    //服务器
    $("#server").text(data['server'])
    $("#time").text(data['time'])
    var flower_data = data['data']

    for (var key in flower_data) {
        var one_data = flower_data[key]
        for (var i = 0; i < one_data.length; i++) {
            one_flower = one_data[i]
            id_color = "#" + one_flower['name'] + "-color"
            $(id_color).text(one_flower['color'])
            id_loc = "#" + one_flower['name'] + "-" + key
            line = ""
            var one_line = one_flower['line']
            for (var j = 0; j < one_line.length; j++) {
                line += one_line[j] + ","
            }
            line = line.slice(0, line.length - 1)
            $(id_loc).text(line)
        }
    }

}

