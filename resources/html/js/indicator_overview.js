function handle(data) {
    var table = $("#table tbody")
    var role_info = data['role_info']
    var role_performance = data['data']
    var d_2 = role_performance['2d']
    var d_3 = role_performance['3d']
    var d_5 = role_performance['5d']

    $("#name").text(role_info['server'] + " " + role_info['name'])

    if (d_2 != null) {
        type = "2v2"
        one_string = get_string(type, d_2)
        table.append(one_string)
    }
    if (d_3 != null) {
        type = "3v3"
        one_string = get_string(type, d_3)
        table.append(one_string)
    }
    if (d_5 != null) {
        type = "5v5"
        one_string = get_string(type, d_5)
        table.append(one_string)
    }
}

function get_string(type, data) {
    var one_string = "<tr><td>" + type
    one_string += '</td><td>' + data['grade']
    one_string += '</td><td>' + data['total_count']
    one_string += '</td><td>' + data['mmr']
    one_string += '</td><td>' + data['win_count']
    lose = data['total_count'] - data['win_count']
    one_string += '</td><td>' + lose
    one_string += '</td><td>' + data['win_rate'] + "%"
    one_string += '</td><td>' + data['mvp_count']
    one_string += '</td><td>' + data['ranking'] + "</td></tr>"
    return one_string
}
