; (function (input, params) {
    var results = []
    var result = {
        _sid: "",
        desc: "数据库基本信息",
        effect: "查询数据库基本信息",
        solution: "无",
        level: "正常",
        id: "mysql.basic_information_of_database",
        name: "数据库基本信息",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "无 SQL 报错并展示查询结果",
        category: "数据库",
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
