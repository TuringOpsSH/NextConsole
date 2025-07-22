; (function (input, params) {
    var results = []
    var result = {
        _sid: "",
        desc: "有多少线程正在使用表",
        effect: "该规则可以帮助用户了解当前有多少线程正在使用表，以便于排查表锁等问题。",
        solution: "如果发现线程数过多，可以考虑优化 SQL 语句，或者使用更高效的存储引擎。",
        level: "正常",
        id: "mysql.how_many_threads_are_using_the_table",
        name: "正在使用表的线程数量",
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
