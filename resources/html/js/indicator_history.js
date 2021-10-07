function handle(data) {
    var table = $("#table tbody")
    var role_info = data['role_info']
    var role_history = data['data']

    $("#name").text(role_info['server'] + " " + role_info['name'])

    for (var i = 0; i < role_history.length; i++) {
        one_data = role_history[i]
        one_string = get_string(one_data)
        table.append(one_string)
    }
}

function get_string(data) {
    var won = data['won']
    if (won) {
        var color = 'class= "text-success"'
        var won_str = "胜利"
    } else {
        var color = 'class= "text-danger"'
        var won_str = "失败"
    }
    var one_string = "<tr><td " + color + ">" + data['time']

    cost_time = data['end_time'] - data['start_time']
    one_string += "</td><td " + color + ">" + cost_time + "s"
    one_string += "</td><td " + color + ">" + data['kungfu']
    type = data['pvp_type']
    if (type == 2) {
        type_str = "2v2"
    } else if (type == 3) {
        type_str = "3v3"
    } else {
        type_str = "5v5"
    }
    one_string += "</td><td " + color + ">" + type_str
    one_string += "</td><td " + color + ">" + data['total_mmr']
    one_string += "</td><td " + color + ">" + data['avg_grade']
    one_string += "</td><td " + color + ">" + data['mmr'] + " ↑"
    one_string += "</td><td " + color + ">" + won_str + '</td></tr>'

    return one_string
}
