;(function (input) {
    var results = []
    var result = {
        desc: "前20条长耗时等待事件统计，用于统计前20条长耗时等待事件",
        effect: "存在告警时的影响是数据库性能下降",
        solution: "告警时的处理方案建议是检查长耗时等待事件的相关配置，优化数据库性能",
        level: "正常",
        id: "dm.longtime20Events",
        name: "前20条长耗时等待事件统计",
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
