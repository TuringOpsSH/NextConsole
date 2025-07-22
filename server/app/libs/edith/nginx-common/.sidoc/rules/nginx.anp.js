;(function (input) {
    var results = []
    var result = {
        desc: "Nginx监听端口",
        effect: "",
        solution: "需要具体分析",
        level: "低风险",
        id: "nginx.anp",
        name: "Nginx监听端口",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "80或443",
        category: "全局配置参数检查",
        family: "conf"
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
        desc: "Nginx监听端口",
        effect: "",
        solution: "需要具体分析",
        level: "高风险",
        id: "nginx.anp",
        name: "Nginx监听端口",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "80或443",
        category: "全局配置参数检查",
        family: "conf"
    }
    var arr = input.split(':')
    var port = arr[1] - 0
    if (port != 80 && port != 443) {
        errResult.actual = port
        errResult.raw = port
        results.push(errResult)
    } else {
        result.raw = port
        result.actual = port
        results.push(result)
    }
    return {results: results}
})(input)
