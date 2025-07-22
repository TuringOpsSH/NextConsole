;(function (input, params) {
    var results = []
    var result = {
        _sid: "",
        desc: "性能参数统计",
        effect: "数据库可能重启过",
        solution: "检查数据库是否非正常重启过",
        level: "正常",
        id: "mysql.performance_parameter_statistics",
        name: "性能参数",
        mixraw: [],
        raw: [],
        actual: "运行时间大于15天",
        expected: "运行时间大于15天",
        category: "",
        family: "log"    }

    result._sid = params[2]["Value"]
    
    if (input == null) {
        result.actual = "查询结果为空"
        return {results: [result]}
    }

    if (typeof input[0] == "string") {
        result.expected = "无 SQL 报错并展示查询结果"
        result.level = "中风险"
        result.actual = input
        result.raw = input
        results.push(result)
        return {results: results}
    }
    result.raw = input

    for (var i = 0; i < input.length; i++) {
        for (var j = 0; j < input[i].length; j++) {
            if (input[i][j]["Variable_name"] == "Uptime") {
                if (input[i][j]["Value"] < 1296000) {
                    result.actual = (input[i][j]["Value"] / (24*60*60)).toFixed(2)
                    result.actual += " Days"
                    result.level = "高风险"
                    result.expected = result.expected + "运行时间大于15天"
                    result.effect = "数据库可能重启过"
                    result.solution = "检查数据库是否非正常重启过"
                }
            }
        }
    }
    result.mixraw = input

    results.push(result)
    return {results: results}

})(input, params)
