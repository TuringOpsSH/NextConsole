; (function (input, params) {
    var results = []
    var result = {
        _sid: "",
        desc: "查询SQL的整体消耗百分比",
        effect: "",
        solution: "",
        level: "正常",
        id: "mysql.overall_consumption_percentage_of_query_sql",
        name: "SQL整体消耗百分比",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "",
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


    results.push(result)
    return { results: results }

})(input, params)
