; (function (input, params) {
    var results = []
    var result = {
        _sid: "",
        desc: "查看平均执行时间值大于95%的平均执行时间的语句（可近似地认为是平均执行时间超长的语句），默认情况下按照语句平均延迟(执行时间)降序排序",
        effect: "响应时间过长",
        solution: "优化语句",
        level: "正常",
        id: "mysql.view_the_statements_whose_average_execution_time_value_is_greater_than_95pct_of_the_average_execut",
        name: "平均执行时间超长的语句",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "无 SQL 报错并展示查询结果",
        category: "",
        family: "log"
    }

    if (!mysqlVersion(params[3]["Value"].match(/\d+\.(?:\d+\.)*\d+/g)[0], "5.7")) {
        result.actual = "本检查不适用于该版本数据库"
        result.raw = ["本检查不适用于该版本数据库"]
        return {results: [result]}
    }

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
            input[i][j]["query"] = input[i][j]["query"].replace(/`/g, " ")
        }
    }
    result.level = "中风险"
    result.expected = "-"
    result.actual = "请移步下章节查看详细内容"
    result.effect = "响应时间过长"
    result.solution = "优化语句"
    result.mixraw = input

    results.push(result)
    return { results: results }

})(input, params)
