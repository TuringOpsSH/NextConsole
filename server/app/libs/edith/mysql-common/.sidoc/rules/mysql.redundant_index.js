; (function (input, params) {
    var results = []
    var result = {
        _sid: "",
        desc: "冗余索引",
        effect: "影响查询效率",
        solution: "删除冗余索引",
        level: "正常",
        id: "mysql.redundant_index",
        name: "冗余索引",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "无冗余索引",
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

    result.level = "中风险"
    result.expected = "无冗余索引"
    result.effect = "影响查询效率"
    result.solution = "删除冗余索引"


    results.push(result)
    return { results: results }

})(input, params)
