; (function (input, params) {
    var results = []
    var result = {
        _sid: "",
        desc: "查看数据库的运行状态",
        effect: "可以查看数据库的运行状态",
        solution: "执行该命令即可查看数据库的运行状态",
        level: "正常",
        id: "mysql.view_the_running_status_of_the_database",
        name: "数据库状态",
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
