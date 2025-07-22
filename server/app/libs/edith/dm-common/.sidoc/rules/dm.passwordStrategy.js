;(function (input) {
    var results = []
    var result = {
        desc: "密码策略",
        effect: "",
        solution: "",
        level: "正常",
        id: "dm.passwordStrategy",
        name: "密码策略",
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
