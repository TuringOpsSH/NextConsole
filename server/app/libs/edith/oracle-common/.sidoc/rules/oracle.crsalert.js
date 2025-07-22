; (function (input) {
    var results = []
    var result = {
        desc: "检查关键字CRS-, ORA-, error, FAIL, failed",
        effect: "根据日志信息具体分析",
        solution: "根据日志信息具体分析",
        level: "正常",
        id: "oracle.crsalert",
        name: "CRS Alert 日志检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "近15天无异常CRS Alert 日志",
        category: "系统运行状态",
        family: "log"
    }

    try {
        raw = input.split("\n")
        result.raw = $.copy(raw)
    } catch (err) {
        $.print(err.message)
        return { results: [result] }
    }

    for (i = 0; i < raw.length; i++) {
        mixlevel = "中风险"
        fields = {}
        fields["line"] = raw[i]
        if (fields["line"] != "") {
            result.level = "中风险"
            result.actual = "存在CRS-, ORA-, error, FAIL, failed相关告警日志"
        }
        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }
})(input)
