; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "win.base",
        name: "windows系统基本配置检查",
        mixraw: [],
        raw: {},
        actual: "",
        expected: "",
        category: "基本配置检查",
        family: "conf"
    }

    try {
        raw = $.copy(input)
        result.raw = raw
    } catch (err) {
        $.print(err.message)
        result.level = "低风险"
        result.actual = "原始数据异常"
    }

    // $.print(result)
    results.push(result)
    return { results: results }

})(input)
