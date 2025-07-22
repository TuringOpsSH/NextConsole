; (function (input, params) {
    var results = []
    var result = {
        _sid: "",
        desc: "查询MySQL支持的所有字符集",
        effect: "",
        solution: "",
        effect: "查询MySQL支持的所有字符集",
        solution: "执行查询语句，查询MySQL支持的所有字符集",
        level: "正常",
        id: "mysql.query_all_character_sets_supported_by_mysql",
        name: "MySQL支持的所有字符集",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "",
        expected: "无 SQL 报错并展示查询结果",
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
