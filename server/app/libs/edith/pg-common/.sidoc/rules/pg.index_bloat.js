;(function (input) {
    var results = []
    var result = {
        desc: "Autovacuum Btree指数膨胀",
        effect: "",
        solution: "",
        level: "正常",
        id: "index_bloat",
        name: "Autovacuum Btree指数膨胀检查",
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
        var entries = Object.entries(raw["index_bloat"])
        var res = []
        for (var i = 0; i < entries.length; i++) {
            if (entries[i].length == 2) {
                var obj = {}
                obj=$.copy(entries[i][1])
                res.push(obj)
            }
        }
        res = OrderByNum(res)
        raw["index_bloat"]=res
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
