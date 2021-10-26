function handle(data) {
    var table = $("#table tbody")
    for (var i = 0; i < data.length; i++) {
        one_data = data[i]
        one_string = get_string(i + 1, one_data)
        table.append(one_string)
    }
}

function get_string(count, data) {
    var one_string = "<tr><td>" + count + '</td><td>' + data['role']
    one_string += '</td><td>' + data['sect']
    one_string += '</td><td>' + data['zone']
    one_string += '</td><td>' + data['server']
    one_string += '</td><td>' + data['value'] + "</td></tr>"
    return one_string
}
