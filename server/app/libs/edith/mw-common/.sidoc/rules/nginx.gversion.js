; (function (input) {
    var results = []
    var result = {
        desc: "Nginx版本",
        effect: "",
        solution: "",
        level: "低风险",
        id: "nginx.gversion",
        name: "产品版本",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "",
        category: "常规检查",
        family: "conf"
    }

    if (!input) {
        result.actual = "未发现配置信息"
        return { results: [result] }
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
