;(function (input) {
    var results = []
    var result = {
        desc: "单日访问量前十用户",
        name: "客户端访问量统计检查",
        level: "低风险",
        id: "nginx.status.top10ip",
        raw: [],
        expected: "",
        family: "status",
        category: "动态参数检查"
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
    result.raw = input[0]["metric"]
    results.push(result)
    return {results: results}
})(input)
