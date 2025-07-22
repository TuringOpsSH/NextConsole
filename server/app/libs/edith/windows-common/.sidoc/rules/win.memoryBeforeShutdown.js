;(function (input) {
    var results = []
    var result = {
        desc: "检查启用关机前清除虚拟内存页面",
        effect: "可能影响业务",
        solution: `找到“清除虚拟内存页面时自动关闭”这个设置，并将其启用`,
        level: "正常",
        id: "win.memoryBeforeShutdown",
        name: "检查启用关机前清除虚拟内存页面",
        mixraw: [],
        raw: "",
        actual: "",
        expected: "启用'关机前清除虚拟内存页面'",
        category: "基本配置检查",
        family: "conf"
    }

    try {
        raw = input
        if (raw.includes("is disabled")) {
            result.level = "中风险"
        } else {
            result.level = "正常"
        }
        result.raw = raw
        result.actual = raw
    } catch (err) {
        $.print(err.message)
        result.level = "低风险"
        result.actual = "原始数据异常"
    }
    results.push(result)
    return {results: results}

})(input)
