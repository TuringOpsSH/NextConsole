;(function (input) {
    var results = []
    var result = {
        desc: "检查IPV6是否禁用",
        effect: "可能影响网络连接或者网速",
        solution: "禁用IPV6",
        level: "正常",
        id: "win.ifDisabledIPV6",
        name: "检查IPV6是否禁用",
        mixraw: [],
        raw: "",
        actual: "",
        expected: "IPV6禁用",
        category: "基本配置检查",
        family: "conf"
    }

    try {
        raw = input
        if (raw.includes("is enabled")) {
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
