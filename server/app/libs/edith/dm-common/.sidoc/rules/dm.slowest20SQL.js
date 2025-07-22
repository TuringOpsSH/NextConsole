;(function (input) {
    var results = []
    var result = {
        desc: "最慢的20条SQL统计",
        effect: "当存在告警时，可能会导致系统性能下降。",
        solution: "优化慢查询语句，减少查询时间。",
        level: "正常",
        id: "dm.slowest20SQL",
        name: "最慢的20条SQL统计",
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
