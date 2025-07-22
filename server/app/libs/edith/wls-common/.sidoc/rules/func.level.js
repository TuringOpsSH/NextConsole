;(function (params) {
    var level = "低风险"
    input = params[0];
    for (i = 0; i < input.length; i++) {
        if (input[i].level == "high") {
            level = "高风险"
            break
        } else if (input[i].level == "mid") {
            level = "中风险"
            break
        }
    }
    return level
})(input)