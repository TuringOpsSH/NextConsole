;(function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "tomcat.logs",
        name: "Tomcat日志信息",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "",
        category: "日志检查",
        family: "conf"
    }

    if (!input) {
        return {results: [result]}
    }

    if (result.family == "status") {
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        return {results: [result]}
    }

    raw0 = raw[0].logs
    result.raw = raw0
    results.push(result)
    return {results: results}
})(input)
