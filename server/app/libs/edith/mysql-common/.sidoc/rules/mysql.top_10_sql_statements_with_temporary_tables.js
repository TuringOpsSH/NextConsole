; (function (input, params) {
    var results = []
    var result = {
        _sid: "",
        desc: "有临时表的前10条SQL语句",
        effect: "展示有临时表的前10条SQL语句",
        solution: "无需处理，仅供参考",
        level: "正常",
        id: "mysql.top_10_sql_statements_with_temporary_tables",
        name: "有临时表语句Top10",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "无 SQL 报错并展示查询结果",
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

    for (var i = 0; i < input.length; i++) {
        for (var j = 0; j < input[i].length; j++) {
            input[i][j]["query"] = input[i][j]["query"].replace(/`/g, " ")
        }
    }


    results.push(result)
    return { results: results }

})(input, params)
