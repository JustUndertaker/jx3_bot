function handle(data) {
    //数量
    $("#robot_nums").text(data['robot_nums'])
    //时间
    $("#time").text(data['time'])

    var robots = data['data']
    var table = $("#table tbody")
    for (var i = 0; i < robots.length; i++) {
        one_robot = robots[i]
        one_string = get_string(one_robot)
        table.append(one_string)
    }
}

function get_string(data) {
    var one_string = "<tr><td>" + data['bot_id'] + '</td><td>' + data['owner_id']
    one_string += '</td><td>' + data['last_sign']
    one_string += '</td><td>' + data['last_left']
    permission = data['permission']
    if (permission) {
        one_string += '</td><td class="text-success">已授权'
    } else {
        one_string += '</td><td class="text-danger">未授权'
    }
    online = data['online']

    if (online) {
        one_string += '</td><td><div class="text-success">在线</td></tr>'
    } else {
        one_string += '</td><td><div class="text-danger">离线</td></tr>'
    }
    return one_string
}
