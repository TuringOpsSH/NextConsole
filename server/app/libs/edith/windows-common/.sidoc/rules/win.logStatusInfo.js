;(function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "win.logStatusInfo",
        name: "应用程序日志的状态",
        mixraw: [],
        raw: {},
        actual: "",
        expected: "应用程序日志的状态正常",
        category: "",
        family: "any"
    }

    try {
        raw = copy(input)
        result.raw = raw
    } catch (err) {
        $.print(err.message)
        return {results: [result]}
    }
    results.push(result)
    return {results: results}

})(input)