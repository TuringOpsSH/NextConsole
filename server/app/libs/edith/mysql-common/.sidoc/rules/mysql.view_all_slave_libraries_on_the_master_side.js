; (function (input, params) {
    var results = []
    var result = {
        _sid: "",
        desc: "主库端查看所有从库",
        effect: "查询主库端所有从库的信息",
        solution: "执行查询语句，查看所有从库的信息",
        level: "正常",
        id: "mysql.view_all_slave_libraries_on_the_master_side",
        name: "从库信息",
        mixraw: [],
        raw: [],
        actual: "",
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
