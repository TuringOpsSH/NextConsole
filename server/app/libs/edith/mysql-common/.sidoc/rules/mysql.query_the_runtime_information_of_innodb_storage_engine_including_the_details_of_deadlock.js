;(function (input, params) {
    var results = []
    var result = {
        _sid: "",
        desc: "查询InnoDB存储引擎的运行时信息，包括死锁的详细信息",
        effect: "查询InnoDB存储引擎的运行时信息，包括死锁的详细信息",
        solution: "无",
        level: "正常",
        id: "mysql.query_the_runtime_information_of_innodb_storage_engine_including_the_details_of_deadlock",
        name: "InnoDB详细信息",
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
    result.mixraw = input

    results.push(result)
    return {results: results}

})(input, params)
