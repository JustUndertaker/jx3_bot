function handle(data) {
    //装饰
    $("#name").text(data['name'])
    $("#imagePath").attr("src", data['imagePath'])
    $("#tip").text(data['tip'])
    $("#type").text(data['type'])
    $("#quality").text(data['quality'])
    $("#source").text(data['source'])
    $("#architecture").text(data['architecture'])
    $("#levelLimit").text(data['levelLimit'])
    $("#qualityLevel").text(data['qualityLevel'])
    $("#viewScore").text(data['viewScore'])
    $("#practicalScore").text(data['practicalScore'])
    $("#hardScore").text(data['hardScore'])
    $("#geomanticScore").text(data['geomanticScore'])
    $("#interestingScore").text(data['interestingScore'])
}
