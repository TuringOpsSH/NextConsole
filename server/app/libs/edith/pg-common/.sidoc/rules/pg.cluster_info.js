;(function (input) {
    var results = []
    var result = {
        desc: "集群信息",
        effect: "",
        solution: "",
        level: "正常",
        id: "cluster_info",
        name: "集群信息检查",
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
        // arr = []
        // for (var key in raw["database_sizes"]) {
        //     arr.push(key + ': ' + raw["database_sizes"][key])
        // }
        var entries =Object.entries(raw["database_sizes"])
        var res = []
        for (var i = 0; i < entries.length; i++) {
            if (entries[i].length == 2) {
                var obj = {
                    name: entries[i][0],
                    size: (entries[i][1]/1024/1024).toFixed(2)
                }
                res.push(obj)
            }
        }
        raw["database_sizes"]=res
        var entries = Object.entries(raw["general_info"])
        var res = []
        for (var i = 0; i < entries.length; i++) {
            if (entries[i].length == 2) {
                var obj = {}
                obj=$.copy(entries[i][1])
                res.push(obj)
            }
        }
        raw["general_info"]=res
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


