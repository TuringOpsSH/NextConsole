; (function (input, params) {
    var results = []
    var result = {
        _sid: "",
        desc: "主库状态监测",
        effect: "当查询结果为空时，需要检查数据库连接是否正常，或者是否存在其他异常情况。",
        solution: "当查询结果为空时，需要检查数据库连接是否正常，或者是否存在其他异常情况。如果查询结果为字符串类型，则需要检查SQL语句是否正确，或者是否存在其他异常情况。",
        level: "正常",
        id: "mysql.main_warehouse_status_monitoring",
        name: "主库状态",
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
