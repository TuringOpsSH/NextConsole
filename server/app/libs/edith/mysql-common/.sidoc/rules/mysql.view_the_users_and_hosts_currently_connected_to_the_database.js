; (function (input, params) {
    var results = []
    var result = {
        _sid: "",
        desc: "查看当前连接到数据库的用户和Host",
        effect: "可以查看当前连接到数据库的用户和Host",
        solution: "执行该命令即可查看当前连接到数据库的用户和Host",
        level: "正常",
        id: "mysql.view_the_users_and_hosts_currently_connected_to_the_database",
        name: "当前连接的用户",
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
