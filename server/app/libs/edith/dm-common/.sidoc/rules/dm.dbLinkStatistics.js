;(function (input) {
    var results = []
    var result = {
        desc: "DBLINK 统计",
        effect: "当存在告警时，可能表示数据库链接存在异常或者被恶意使用",
        solution: "建议检查数据库链接的配置和使用情况，确保安全性",
        level: "正常",
        id: "dm.dbLinkStatistics",
        name: "DBLINK 统计",
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
