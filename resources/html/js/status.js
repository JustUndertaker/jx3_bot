function handle(data) {
    //名字
    $("#nickname").text(data['nickname'])
    //数量
    $("#group_nums").text(data['group_nums'])
    //时间
    $("#time").text(data['time'])

    groups = data['groups']
    var table = $("#table tbody")
    for (var i = 0; i < groups.length; i++) {
        one_group = groups[i]
        one_string = get_string(one_group)
        table.append(one_string)
    }
}

function get_string(data) {
    var one_string = "<tr><td>" + data['group_name'] + '</td><td>' + data['group_id']
    one_string += '</td><td>' + data['sign_nums']
    one_string += '</td><td>' + data['server']
    one_string += '</td><td>' + data['active']
    group_status = data['robot_status']

    if (group_status) {
        one_string += '</td><td><div class="form-check form-switch"><input class="form-check-input" type="checkbox" checked></div></td></tr>'
    } else {
        one_string += '</td><td><div class="form-check form-switch"><input class="form-check-input" type="checkbox"></div></td></tr>'
    }
    return one_string
}
