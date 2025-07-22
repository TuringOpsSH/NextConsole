;(function (input) {
    var results = []
    var result = {
        desc: "nginx 编译列表",
        effect: "",
        solution: "",
        level: "正常",
        id: "nginx.confargs",
        name: "编译列表",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "",
        category: "常规检查",
        family: "conf"
    }

    if (!input) {
        result.actual = "未发现配置信息"
        return {results: [result]}
    }

    if (result.family == "status") {
        result.raw = input[0]["metric"]
    } else {
        result.raw = input
    }

    if (!result.raw) {
        return {results: [result]}
    }
    result.actual = input
    results.push(result)
    return {results: results}
})(input)
