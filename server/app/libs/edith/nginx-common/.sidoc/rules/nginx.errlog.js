;(function (input) {
    var results = []
    var result = {
        desc: "日志中是否有错误信息",
        name: "Error日志检查",
        level: "低风险",
        id: "nginx.errlog",
        raw: [],
        expected: "无错误日志信息",
        actual: "",
        family: "logs",
    }
    if (!input) {
        result.actual = "未发现相关记录"
        return {results: [result]}
    }

    if (result.family == "status") {
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        result.actual = "未发现相关记录"
        return {results: [result]}
    }
    var errResult = {
        desc: "日志中是否有错误信息",
        name: "Error日志检查",
        level: "高风险",
        id: "nginx.errlog",
        raw: [],
        expected: "无错误日志信息",
        actual:""
    }
    var errLog = input
    if (errLog != "") {
        errResult.raw = errLog
        errResult.actual = "日志有错误信息，详细内容略"
        results.push(errResult)
    } else {
        result.raw = errLog
        result.actual = "日志无错误信息"
        results.push(result)
    }
    return {results: results}
})(input)
