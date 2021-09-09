function handle(data) {

    $("#nickname").text(data['nickname'])
    $("#friend_nums").text(data['friend_nums'])

    friends = data['friends']
    var table = $("#table tbody")
    for (var i = 0; i < friends.length; i++) {
        one_friend = friends[i]
        one_string = get_string(i + 1, one_friend)
        table.append(one_string)
    }
}


function get_string(num, data) {
    var one_string = '<tr><td>' + num + '</td><td>' + data['user_name'] + '</td><td>' + data['user_id']
    return one_string
}
