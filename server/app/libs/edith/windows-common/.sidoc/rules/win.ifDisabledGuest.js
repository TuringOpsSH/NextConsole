;(function (input) {
    var results = []
    var result = {
        desc: "检查Guest用户是否禁用",
        effect: "对系统安全有影响",
        solution: "禁用Guest用户",
        level: "正常",
        id: "win.ifDisabledGuest",
        name: "检查Guest用户是否禁用",
        mixraw: [],
        raw: "",
        actual: "",
        expected: "禁用Guest用户",
        category: "基本配置检查",
        family: "conf"
    }

    try {
        raw = input
        if (raw.includes("account disbale")) {
            result.level = "正常"
        } else {
            result.level = "中风险"
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
