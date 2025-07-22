;(function (input) {
    var results = []
    var result = {
        desc: "检查非域服务器关闭共享",
        effect: "可能存在安全风险、数据泄露",
        solution: "关闭非域服务器共享",
        level: "正常",
        id: "win.ifNonDomainServerClosedShare",
        name: "检查非域服务器关闭共享",
        mixraw: [],
        raw: "",
        actual: "",
        expected: "关闭非域服务器共享",
        category: "基本配置检查",
        family: "conf"
    }

    try {
        raw = input
        if (raw.includes("Don't close")) {
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
