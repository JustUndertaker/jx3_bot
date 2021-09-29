function handle(data) {
    //名字
    $("#name").text(data['name'])
    //图片
    $("#image").attr("src", data['upload'])
    //说明
    $("#info").text(data['info'])
    var item_list = data['data']
    for (var i = 0; i < item_list.length; i++) {
        one_list = item_list[i]
        for (var j = 0; j < one_list.length; j++) {
            item = one_list[j]
            server = item['zone']
            table_name = "#" + server + " tbody"
            var table = $(table_name)
            one_string = get_string(item)
            table.append(one_string)
        }
    }
}

function get_string(data) {
    var one_string = "<tr><td class='text-center text-warning'>" + data['time'] + '</td>'
    one_string += "<td class='text-center'>" + data['server'] + "</td>"
    one_string += "<td class='text-center text-primary'>￥" + data['price'] + "</td>"
    one_string += "<td class='text-center'>" + data['sales'] + "</td></tr>"
    return one_string
}
