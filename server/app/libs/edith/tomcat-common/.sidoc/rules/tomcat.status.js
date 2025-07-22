;(function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "tomcat.status",
        name: "Tomcat状态信息",
        mixraw: [],
        raw: {
            gcLogState: "",
            heapDumpState: "",
            runningState: ""
        },
        actual: "",
        expected: "",
        category: "状态检查",
        family: "conf"
    }

    if (!input) {
        return {results: [result]}
    }
    raw = input[0]
    result.raw = copy(raw["status"])
    results.push(result)
    return {results: results}
})(input)
