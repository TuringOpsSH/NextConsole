; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "win.basicLogConfInfo",
        name: "系统日志的配置信息检查",
        mixraw: [],
        raw: {},
        actual: "",
        expected: "系统日志的配置信息检查正常",
        category: "",
        family: "any"
    }

    try {
        raw = $.copy(input)
        result.raw = raw
    } catch (err) {
        $.print(err.message)
        return { results: [result] }
    }

    // if(!raw){
    //     return { results: [result] }
    // }

    // for (i = 0; i < raw.length; i++) {
    //     mixlevel = "正常"
    //     fields = {}
    //     fields = raw[i]
    //
    //     // Check fields, reset mixlevel and result.level here:
    //
    //     // fields["test"] //string
    //
    //
    //     fields["mixlevel"] = mixlevel
    //     result.mixraw.push(fields)
    // }
    results.push(result)
    return { results: results }

})(input)