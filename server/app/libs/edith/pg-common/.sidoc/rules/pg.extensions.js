;(function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "extensions",
        name: "extensions",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "",
        category: "",
        family: "conf"
    }

    if (!input) {
        result.actual = "查询结果为空"
        return {results: [result]}
    }
    try {
        raw = $.copy(input)
        var entries = Object.entries(raw)
        var res = []
        for (var i = 0; i < entries.length; i++) {
            if (entries[i].length == 2) {
                var obj = {}
                obj = $.copy(entries[i][1])
                var obj2 = {}
                var entries2 = Object.entries(obj)
                obj2 = entries2[0][1]
                obj2["database"]=entries[i][0]
                res.push(obj2)
            }
        }
        result.raw = res
    } catch (err) {
        $.print(err.message)
        result.level = "低风险"
        result.actual = "原始数据异常"
        result.solution = ""
    }
    results.push(result)
    return {results: results}
})(input)
