;(function (input) {
    var results = []
    var result = {
        desc: "过滤日志中的错误信息（具体需要根据生产中httpd的error日志中常见的报错关键字来过滤）",
        effect: "系统有报错出现",
        solution: "需要具体分析",
        level: "",
        id: "apache.errlog",
        name: "异常日志检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "无错误日志",
        category: "日志排查",
        family: "log"
    }

    if (!input) {
        result.actual = "暂无异常日志"
        result.level = "低风险"
        return {results: [result]}
    }

    if (!input[0]["metric"]) {
        result.actual = "暂无异常日志"
        result.level = "低风险"
        return {results: [result]}
    }

    result.raw = input[0]["metric"]
    result.actual = "发现异常日志"
    result.level = "高风险"
    results.push(result)
    return {results: results}

})(input)
