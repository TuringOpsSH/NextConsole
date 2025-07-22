;(function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "tomcat.webConf",
        name: "",
        mixraw: [],
        raw: {
            servlet: [],
            version: "",
            xmlns: "",
            xsi: "",
        },
        actual: "",
        expected: "",
        category: "配置检查",
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
    result.raw.servlet = raw.servlet
    result.raw.version = raw.version
    result.raw.xmlns = raw.xmlns
    result.raw.xsi = raw.xsi

    results.push(result)
    return {results: results}
})(input)
