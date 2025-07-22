;(function (input) {
    var results = []
    var result = {
        desc: "windows系统日志的最近10个错误和警告事件",
        effect: "可能影响业务",
        solution: "",
        level: "正常",
        id: "win.recent10ErrorMsg",
        name: "windows系统日志的最近10个错误和警告事件",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "",
        category: "系统运行状态",
        family: "log"
    }
    try {
        raw = input["Events"]
        result.raw = raw
    } catch (err) {
        $.print(err.message)
        result.level = "低风险"
        result.actual = "原始数据异常"
    }
    results.push(result)
    return {results: results}
})(input)