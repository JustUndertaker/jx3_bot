function handle(data) {
    //头像
    $("#head_icon").attr("src", data['head_icon'])
    //状态
    $("#robot_status").text(data['robot_status'])
    $("#nickname").text(data['nickname'])
    $("#server").text(data['server'])
    $("#sign_nums").text(data['sign_nums'])
    $("#active").text(data['active'])

    //开关
    var col = $("#col")
    welcome = get_alert(data['welcome_status'], "进群通知")
    someoneleft = get_alert(data['someone_left_status'], "离群通知")
    goodnight = get_alert(data['goodnight_status'], "晚安通知")
    col.append(welcome)
    col.append(someoneleft)
    col.append(goodnight)

    plugins = data['plugins']
    var table = $("#table tbody")
    for (var i = 0; i < plugins.length; i++) {
        one_plugin = plugins[i]
        one_string = get_string(one_plugin)
        table.append(one_string)
    }
}

function get_alert(status, name) {
    if (status) {
        var one_string = '<div class="alert alert-success"><h6>' + name + '：开</h6></div>'
    } else {
        var one_string = '<div class="alert alert-secondary"><h6>' + name + '：关</h6></div>'
    }
    return one_string
}


function get_string(data) {
    plugin_status = data['status']
    if (plugin_status) {
        var one_string = '<tr><td>' + data['name'] + '</td><td>' + data['command'] + '</td><td>' + data['des'] + '</td><td><div class="form-check form-switch"><input class="form-check-input" type="checkbox" checked></div></td></tr>'
    } else {
        var one_string = '<tr><td>' + data['name'] + '</td><td>' + data['command'] + '</td><td>' + data['des'] + '</td><td><div class="form-check form-switch"><input class="form-check-input" type="checkbox"></div></td></tr>'
    }
    return one_string
}
