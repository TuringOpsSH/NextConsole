;(function (input) {
    var results = []
    var result = {
        desc: "进程列表",
        effect: "",
        solution: "",
        level: "正常",
        id: "win.processList",
        name: "进程列表",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "",
        category: "基本配置检查",
        family: "conf"
    }
    try {
        raw = input
        result.raw.push(raw)
    } catch (err) {
        $.print(err.message)
        result.level = "低风险"
        result.actual = "原始数据异常"
    }
    results.push(result)
    return {results: results}
})(input)