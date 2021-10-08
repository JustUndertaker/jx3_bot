function handle(data) {
    var table = $("#table tbody")
    var history = data['history']
    var role_performance = data['role_performance']
    var d_2 = role_performance['2d']
    var d_3 = role_performance['3d']
    var d_5 = role_performance['5d']
    var card_body = $("#card-body")
    $("#name").text(data['name'])

    if (d_2 != null) {
        type = "2v2"
        one_string = get_card(type, d_2)
        card_body.append(one_string)
    }
    if (d_3 != null) {
        type = "3v3"
        one_string = get_card(type, d_3)
        card_body.append(one_string)
    }
    if (d_5 != null) {
        type = "5v5"
        one_string = get_card(type, d_5)
        card_body.append(one_string)
    }
    for (var i = 0; i < history.length; i++) {
        one_data = history[i]
        one_string = get_string(one_data)
        table.append(one_string)
    }

}

function get_card(type, data) {
    var one_string = '<div class="card bg-light p-3 mb-4"><div class="row text-center text-secondary fs-4 p-1" ><div class="col"><span class="badge bg-primary">'
    one_string += type + '</span ></div ><div class="col" >'
    one_string += data['total_count'] + '</div ><div class="col">'
    one_string += data['mvp_count'] + '</div><div class="col">'
    one_string += data['win_count'] + '</div ><div class="col">'
    one_string += data['win_rate'] + '%</div><div class="col">'
    one_string += data['mmr'] + '</div><div class="col">'
    one_string += data['ranking'] + '</div></div><div class="row text-center text-body fs-4 p-1"><div class="col">'
    one_string += data['grade'] + '段</div><div class="col">总场次</div><div class="col">最佳</div><div class="col">胜场</div><div class="col">胜率</div><div class="col">评分</div><div class="col">周排名</div></div></div>'

    return one_string
}

function get_string(data) {
    var one_string = '<tr class="text-center align-middle"><td>' + data['kungfu']
    one_string += '</td><td><p>' + data['pvp_type'] + '</p><p>' + data['avg_grade'] + '段局</p>'
    one_string += '</td><td>' + data['source']
    var source_add = data['source_add']
    if (source_add[0] == "+") {
        one_string += '（<a class="text-success" style="text-decoration:none;">' + source_add + '</a>）'
    } else {
        one_string += '（<a class="text-danger" style="text-decoration:none;">' + source_add + '</a>）'
    }
    one_string += '</td><td>' + data['pvp_time']
    one_string += '</td><td>' + data['end_time']
    result = data['result']
    if (result) {
        one_string += '</td><td class="text-success">胜利</td></tr>'
    } else {
        one_string += '</td><td class="text-danger">失败</td></tr>'
    }

    return one_string
}
