;(function (input) {
    var results = []
    var result = {
        desc: "数据库备份日志",
        effect: "检查数据库备份日志是否正常",
        solution: "根据实际情况采取相应的处理措施",
        level: "正常",
        id: "dm.backupLogs",
        name: "数据库备份日志",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "",
        category: "",
        family: ""
    }

    if (!input) {
        result.actual = "查询结果为空"
        return {results: [result]}
    }
    try {
        result.raw = input
    } catch (err) {
        $.print(err.message)
        result.level = "低风险"
        result.actual = "原始数据异常"
        result.solution = ""
    }
    // $.print(err.message)
    results.push(result)
    return {results: results}

})(input)
