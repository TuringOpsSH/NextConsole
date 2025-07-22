; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "win.safeLogConfInfo",
        name: "安全日志配置信息",
        mixraw: [],
        raw: {},
        actual: "",
        expected: "安全日志配置信息正常",
        category: "",
        family: "any"
    }

    try {
        raw = $.copy(input)
        result.raw = raw
    } catch (err) {
        $.print(err.message)
        return { results: [result] }
    }
    results.push(result)
    return { results: results }

})(input)