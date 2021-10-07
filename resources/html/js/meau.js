function handle(data) {
    //头像
    $("#head_icon").attr("src", data['head_icon'])
    //状态
    $("#robot_status").text(data['robot_status'])
    $("#nickname").text(data['nickname'])
    $("#server").text(data['server'])
    $("#sign_nums").text(data['sign_nums'])
    $("#active").text(data['active'])

    plugins = data['plugins']
    var table = $("#table tbody")
    for (var i = 0; i < plugins.length; i++) {
        one_plugin = plugins[i]
        one_string = get_string(one_plugin)
        table.append(one_string)
    }
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
