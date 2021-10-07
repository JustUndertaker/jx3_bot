function handle(data) {
    var table = $("#table tbody")
    var type = data['type']
    var alldata = data['data']

    if (type == "2d") {
        type_str = "2v2"
    } else if (type == "3d") {
        type_str = "3v3"
    } else {
        type_str = "5v5"
    }

    $("#name").text(type_str)

    for (var i = 0; i < alldata.length; i++) {
        one_data = alldata[i]
        one_string = get_string(one_data)
        table.append(one_string)
    }
}

function get_string(data) {
    var one_string = "<tr><td>" + data['rankNum']
    one_string += '</td><td>' + data['roleName']
    one_string += '</td><td>' + data['zoneName']
    one_string += '</td><td>' + data['serverName']
    one_string += '</td><td>' + data['forceName']
    one_string += '</td><td>' + data['score']
    one_string += '</td><td>' + data['upNum']
    one_string += '</td><td>' + data['winRate'] + "</td></tr>"
    return one_string
}
