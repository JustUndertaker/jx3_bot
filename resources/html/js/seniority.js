function handle(data) {
    var table = $("#table tbody")
    for (var i = 0; i < data.length; i++) {
        one_data = data[i]
        one_string = get_string(one_data)
        table.append(one_string)
    }
}

function get_string(data) {
    var one_string = "<tr><td>" + data['name'] + '</td><td>' + data['role']
    one_string += '</td><td>' + data['zone'] + "-" + data['server']
    one_string += '</td><td>' + data['sect']
    one_string += '</td><td>' + data['value'] + "</td></tr>"
    return one_string
}
