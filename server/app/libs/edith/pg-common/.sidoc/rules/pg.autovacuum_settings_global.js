;(function (input) {
    var results = []
    var result = {
        desc: "Autovacuum全局配置信息",
        effect: "",
        solution: "",
        level: "正常",
        id: "autovacuum_settings_global",
        name: "Autovacuum全局配置信息检查",
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
        raw = $.copy(input["global_settings"])
        var entries = Object.entries(raw)
        var res = []
        for (var i = 0; i < entries.length; i++) {
            if (entries[i].length == 2) {
                var obj = {}
                obj=$.copy(entries[i][1])
                res.push(obj)
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
