;(function (input) {
    var results = []
    var result = {
        desc: "windows内存使用率检查",
        effect: "系统运行缓慢甚至不响应",
        solution: "排查各应用占用内存情况，合理进行扩容",
        level: "正常",
        id: "win.memUsedPercent",
        name: "windows内存使用率检查",
        mixraw: [],
        raw: {},
        actual: "",
        expected: "内存使用率小于 90%",
        category: "系统容量检查",
        family: "conf"
    }
    result.actual = input["usedPercent"].toFixed(2) + "%"
    result.raw.total = input["total"]
    result.raw.available = input["available"]
    result.raw.used = input["used"]
    result.raw.usedPercent = result.actual
    result.raw.free=input["free"]
    try {
        if (input["usedPercent"] > 90) {

            result.level = "高风险"
        } else {
            result.level = "正常"
        }
    } catch (err) {
        $.print(err.message)
        result.level = "低风险"
        result.actual = "原始数据异常"
    }
    results.push(result)
    return {results: results}
})(input)