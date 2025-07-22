; (function (input) {
    var results = []
    var result = {
        desc: "列出访问httpd服务前10的客户端IP和访问次数",
        effect: "评估访问量，是否有安全隐患",
        solution: "需要具体分析",
        level: "",
        id: "apache.status.top10ip",
        name: "客户端访问量检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "需要具体分析",
        category: "日志排查",
        family: "status"
    }

    if (!input) {
        result.actual = "暂无访问记录"
        return { results: result }
    }


    if (result.family == "status") {
        result.raw = input[0]["metric"]
    } else {
        result.raw = input
    }

    if (!result.raw) {
        return { results: [result] }
    }

    results.push(result)
    return { results: results }

})(input)
