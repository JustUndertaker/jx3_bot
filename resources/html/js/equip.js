function handle(alldata) {
    //标题
    var page_tittle = alldata['tittle'] + " 角色图鉴"
    $("#page_tittle").text(page_tittle)

    //属性
    var attribute = alldata['attribute']
    for (var i = 0; i < attribute.length; i++) {
        var one_role = attribute[i]
        role_tittle = "#role_tittle_" + i
        role_value = "#role_value_" + i
        $(role_tittle).text(one_role["tittle"])
        $(role_value).text(one_role["value"])
    }


    //装备
    var equip = data['equip']
    for (var i = 0; i < equip.length; i++) {
        var one_equip = equip[i]
        equip_icon = "#equip_icon_" + i
        equip_name = "#equip_name_" + i
        $(equip_icon).attr("src", one_equip['icon'])
        $(equip_name).text(one_equip['name'])
    }

    //奇穴
    var qixue = data['qixue']
    for (var i = 0; i < qixue.length; i++) {
        var one_qixue = qixue[i]
        qixue_icon = "#qixue_icon_" + i
        qixue_name = "#qixue_name_" + i
        $(qixue_icon).attr("src", one_qixue['icon'])
        $(qixue_name).text(one_qixue['name'])
    }

    //页脚
    $("#nickname").text(alldata['nickname'])
}
