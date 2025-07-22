; (function (input, params) {
    var results = []
    var result = {
        _sid: "",
        desc: "锁详情",
        effect: "根据查询结果进行相应的处理",
        solution: "根据查询结果进行相应的处理，如释放锁等",
        level: "正常",
        id: "mysql.lock_details",
        name: "锁详情",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "无 SQL 报错并展示查询结果",
        category: "",
        family: "log"
    }

    if (mysqlVersion(params[3]["Value"].match(/\d+\.(?:\d+\.)*\d+/g)[0], "8")) {
        result.actual = "本检查不适用于该版本数据库"
        result.raw = ["本检查不适用于该版本数据库"]
        return {results: [result]}
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
