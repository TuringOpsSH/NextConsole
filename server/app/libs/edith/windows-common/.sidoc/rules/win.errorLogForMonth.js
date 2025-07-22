;(function (input) {
    var results = []
    var result = {
        desc: "查看系统事件日志中最近一个月内 Error 和 Warning 的记录数",
        effect: "",
        solution: "",
        level: "正常",
        id: "win.errorLogForMonth",
        name: "系统事件日志中最近一个月内 Error 和 Warning 的记录数",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "",
        category: "",
        family: "any"
    }

    try {
        result.raw = input
    } catch (err) {
        $.print(err.message)
        return {results: [result]}
    }
    results.push(result)
    return {results: results}

})(input)