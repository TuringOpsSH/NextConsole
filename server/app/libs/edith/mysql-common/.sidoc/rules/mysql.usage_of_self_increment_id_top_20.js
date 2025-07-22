; (function (input, params) {
    var results = []
    var result = {
        _sid: "",
        desc: "自增ID的使用情况（前20条）",
        effect: "可能需要扩容",
        solution: "根据实际情况扩容",
        level: "正常",
        id: "mysql.usage_of_self_increment_id_top_20",
        name: "自增ID Top20",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "Auto_increment < 1717986917 (INT类型最大值的80%)",
        category: "",
        family: "log"
    }

    result._sid = params[2]["Value"]
    
    if (input == null) {
        result.actual = "查询结果为空"
        return {results: [result]}
    }

    if (typeof input[0] == "string") {
        result.expected = "无 SQL 报错并展示查询结果"
        result.level = "中风险"
        result.actual = input
        result.raw = input
        results.push(result)
        return {results: results}
    }

    result.raw = input
    result.expected = "Auto_increment < 1717986917 (INT类型最大值的80%)"
    for (var i = 0; i < input.length; i++) {
        for (var j = 0; j < input[i].length; j++) {
            if (input[i][j]["Auto_increment"] > 1717986917) {
                input[i][j]["inspectionLevel"] = "中风险"
                result.level = "中风险"
                result.expected = "Auto_increment < 1717986917 (INT类型最大值的80%)"
                result.actual = input[i][j]["Auto_increment"]
                result.effect = "可能需要扩容"
            }
        }
    }

    result.mixraw = input

    results.push(result)
    return { results: results }

})(input, params)
