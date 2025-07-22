;(function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "basicInfo",
        name: "edith基本参数信息",
        mixraw: [],
        raw: {
            format: "",
            output: "",
            path: ""
        },
        actual: "",
        expected: "",
        category: "",
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
    result.raw.format = raw.flags["format"]
    result.raw.output = raw.flags.output
    result.raw.path = raw.flags.path
    results.push(result)
    return {results: results}
})(input)
