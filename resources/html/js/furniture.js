function handle(data) {
    //装饰
    $("#name").text(data['name'])
    $("#imagePath").attr("src", data['image_path'])
    $("#tip").text(data['tip'])
    $("#type").text(data['type'])
    $("#quality").text(data['quality'])
    $("#source").text(data['source'])
    $("#architecture").text(data['architecture'])
    $("#levelLimit").text(data['level_limit'])
    $("#qualityLevel").text(data['quality_level'])
    $("#viewScore").text(data['view_score'])
    $("#practicalScore").text(data['practical_score'])
    $("#hardScore").text(data['hard_score'])
    $("#geomanticScore").text(data['geomantic_score'])
    $("#interestingScore").text(data['interesting_score'])
}
