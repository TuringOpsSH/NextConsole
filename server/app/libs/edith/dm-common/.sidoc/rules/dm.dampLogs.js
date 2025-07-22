;(function (input) {
    var results = []
    var result = {
        desc: "DMAP 进程日志",
        effect: "当存在告警时，可能会影响系统的正常运行",
        solution: "建议检查并解决告警产生的问题，确保系统的稳定性",
        level: "正常",
        id: "dm.dampLogs",
        name: "DMAP 进程日志",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "",
        category: "",
        family: ""
    }

    if (!input) {
        result.actual = "查询结果为空"
        return {results: [result]}
    }
    try {
        // obj = {}
        // for (let i = 0; i < input.length; i++) {
        //     if (input[i]["ErrorDamps"].length) {
        //        continue
        //     }
        //     obj = $.copy(input[i])
        //     result.raw.push(obj)
        // }
        result.raw = input
    } catch (err) {
        $.print(err.message)
        result.level = "低风险"
        result.actual = "原始数据异常"
        result.solution = ""
    }
    // $.print(err.message)
    results.push(result)
    return {results: results}

})(input)
