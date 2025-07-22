; (function (input, params) {
    var results = []
    var result = {
        _sid: "",
        desc: "跟踪长时间操作的进度",
        effect: "响应时间过长",
        solution: "优化长时间操作的语句",
        level: "正常",
        id: "mysql.track_the_progress_of_long_term_operations",
        name: "长时间操作",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "长时间操作进度为空",
        category: "",
        family: "log"
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
    result.level = "中风险"
    result.expected = "长时间操作进度为空"
    result.actual = "请移步下章节查看详细内容"
    result.effect = "响应时间过长"
    result.solution = "优化长时间操作的语句"
    result.mixraw = input


    results.push(result)
    return { results: results }

})(input, params)
