;(function (input) {
    var results = []
    var result = {
        desc: "检查操作系统激活情况",
        effect: "功能受限并存在安全风险",
        solution: "激活操作系统",
        level: "正常",
        id: "win.ifOperatingSystemActive",
        name: "检查操作系统激活情况",
        mixraw: [],
        raw: "",
        actual: "",
        expected: "操作系统已激活",
        category: "基本配置检查",
        family: "conf"
    }

    try {
        raw = input
        if (raw.includes("is not actived")) {
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
