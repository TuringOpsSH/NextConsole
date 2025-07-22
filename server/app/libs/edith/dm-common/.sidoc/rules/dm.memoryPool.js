;(function (input) {
    var results = []
    var result = {
        desc: "内存池",
        effect: "当内存池存在问题时，可能会导致数据库性能下降或者系统崩溃。",
        solution: "建议定期监控内存池的使用情况，及时调整参数以保证数据库的正常运行。",
        level: "正常",
        id: "dm.memoryPool",
        name: "内存池",
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
