; (function (input, params) {
    var results = []
    var result = {
        _sid: "",
        desc: "MGR详情",
        effect: "",
        solution: "",
        level: "正常",
        id: "mysql.mgr_details",
        name: "MGR详情",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "",
        category: "",
        family: "log"
    }

    if (!mysqlVersion(params[3]["Value"].match(/\d+\.(?:\d+\.)*\d+/g)[0], "5.7")) {
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
