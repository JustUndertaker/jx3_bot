function handle(data) {
    //数量
    $("#token_nums").text(data['token_nums'])

    var tokens = data['data']
    var table = $("#table tbody")
    for (var i = 0; i < tokens.length; i++) {
        one_token = tokens[i]
        one_string = get_string(one_token, i + 1)
        table.append(one_string)
    }
}

function get_string(data, index) {
    var one_string = "<tr><td>" + index + '</td><td>' + data['token']

    var alive = data['alive']
    if (alive) {
        one_string += '</td><td><div class="text-success">有效</td></tr>'
    } else {
        one_string += '</td><td><div class="text-danger">无效</td></tr>'
    }
    return one_string
}
