function handle(data) {
    var table = $("#table tbody")
    var role_info = data['roleInfo']
    var alldata = data['data']
    name_str = role_info['serverName'] + " " + role_info['roleName']
    $("#name").text(name_str)

    for (var i = 0; i < alldata.length; i++) {
        one_data = alldata[i]
        one_string = get_string(one_data)
        table.append(one_string)
    }
}

function get_string(data) {

    var one_string = "<tr><td>" + data['mapName']
    one_string += '</td><td>' + data['mapType']

    var bossProgress = data['bossProgress']
    boss_str = ""
    for (var i = 0; i < bossProgress.length; i++) {
        one_boss = bossProgress[i]
        finished = one_boss['finished']
        if (finished) {
            boss_str += "○"
        } else {
            boss_str += "●"
        }
    }
    one_string += '</td><td>' + boss_str
    bossCount = data['bossCount']
    bossFinished = data['bossFinished']
    if (bossCount - bossFinished == 0) {
        one_string += '</td><td class="text-success">√</td></tr>'
    } else {
        one_string += '</td><td class="text-danger">×</td></tr>'
    }
    return one_string
}
