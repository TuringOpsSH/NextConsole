;(function (input) {
    var results = []
    var result = {
        desc: "Autovacuum配置信息",
        effect: "",
        solution: "",
        level: "正常",
        id: "autovacuum_settings",
        name: "Autovacuum配置信息检查",
        mixraw: [],
        raw: {},
        actual: "",
        expected: "",
        category: "",
        family: "conf"
    }

    if (!input) {
        result.actual = "查询结果为空"
        return {results: [result]}
    }
    try {
        raw = $.copy(input)
        result.raw = raw
    } catch (err) {
        $.print(err.message)
        result.level = "低风险"
        result.actual = "原始数据异常"
        result.solution = ""
    }
    results.push(result)
    return {results: results}
})(input)
