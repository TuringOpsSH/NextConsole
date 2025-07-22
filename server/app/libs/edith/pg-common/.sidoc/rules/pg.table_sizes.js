;(function (input) {
    var results = []
    var result = {
        desc: "数据库表的大小",
        effect: "",
        solution: "",
        level: "正常",
        id: "table_sizes",
        name: "数据库表大小检查",
        mixraw: [],
        raw: {},
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
        var entries = Object.entries(raw["tables_data"])
        var res = []
        for (var i = 0; i < entries.length; i++) {
            if (entries[i].length == 2) {
                var obj = {}
                obj = $.copy(entries[i][1])
                res.push(obj)
            }
        }
        res = OrderByNum(res)
        raw["tables_data"] = res
        result.raw = raw
    } catch (err) {
        $.print(err.message)
        result.level = "低风险"
        result.actual = "原始数据异常"
        result.solution = ""
    }
    results.push(result)
    return {results: results}
})(input)
