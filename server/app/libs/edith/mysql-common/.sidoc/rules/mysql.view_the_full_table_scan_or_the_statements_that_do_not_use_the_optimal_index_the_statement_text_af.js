; (function (input, params) {
    var results = []
    var result = {
        _sid: "",
        desc: "查看全表扫描或者没有使用到最优索引的语句（经过标准化转化的语句文本），默认情况下按照全表扫描次数与语句总次数百分比和语句总延迟时间(执行时间)降序排序",
        effect: "查看全表扫描或者没有使用到最优索引的语句",
        solution: "优化SQL语句，使用最优索引",
        level: "正常",
        id: "mysql.view_the_full_table_scan_or_the_statements_that_do_not_use_the_optimal_index_the_statement_text_af",
        name: "全表扫描或未用最优索引的SQL",
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
