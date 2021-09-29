function handle(data) {
    //服务器
    $("#server").text(data['server'])
    //时间
    $("#time").text(data['time'])

    var adventure_list = data['data']
    var table = $("#table tbody")
    for (var i = 0; i < adventure_list.length; i++) {
        adventure = adventure_list[i]
        one_string = get_string(adventure)
        table.append(one_string)
    }
}

function get_string(data) {
    var one_string = "<tr><td class='text-center text-primary'>" + data['serendipity'] + '</td>'
    one_string += "<td class='text-center text-success'>" + data['name'] + "</td>"
    one_string += "<td class='text-center text-danger'>" + data['time'] + "</td></tr>"
    return one_string
}
