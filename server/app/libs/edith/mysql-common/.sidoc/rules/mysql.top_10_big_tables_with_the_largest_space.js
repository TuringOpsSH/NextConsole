; (function (input, params) {
    var results = []
    var result = {
        _sid: "",
        desc: "占用空间最大的前10张大表",
        effect: "影响查询效率",
        solution: "优化表结构，减少表内数据量",
        level: "正常",
        id: "mysql.top_10_big_tables_with_the_largest_space",
        name: "占用空间Top10的表",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "表内行数量小于40000000",
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

    for (var i = 0; i < input.length; i++) {
        for (var j = 0; j < input[i].length; j++) {
            if (input[i][j]["table_rows"] > 40000000) {
                input[i][j]["inspectionLevel"] = "中风险"
                result.level = "中风险"
                result.actual = "table_rows: " + input[i][j]["table_rows"]
                result.expected = "表内行数量小于40000000"
                result.effect = "影响查询效率"
            }
        }
    }

    result.mixraw = input

    results.push(result)
    return { results: results }

})(input, params)
