; (function (input, params) {
    var results = []
    var result = {
        _sid: "",
        desc: "当前Innodb内核中的当前活跃（active）事务",
        effect: "该规则可以帮助用户了解当前Innodb内核中的当前活跃（active）事务",
        solution: "无",
        level: "正常",
        id: "mysql.current_active_transactions_in_the_current_innodb_kernel",
        name: "当前活跃事务",
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
