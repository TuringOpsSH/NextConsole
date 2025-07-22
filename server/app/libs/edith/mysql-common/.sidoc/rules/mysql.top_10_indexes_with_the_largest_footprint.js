; (function (input, params) {
    var results = []
    var result = {
        _sid: "",
        desc: "占用空间最大的前10个索引",
        effect: "",
        solution: "",
        level: "正常",
        id: "mysql.top_10_indexes_with_the_largest_footprint",
        name: "占用空间Top10的索引",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "",
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
