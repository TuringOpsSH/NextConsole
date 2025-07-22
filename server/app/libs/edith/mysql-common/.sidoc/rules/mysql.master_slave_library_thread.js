; (function (input, params) {
    var results = []
    var result = {
        _sid: "",
        desc: "主从库线程",
        effect: "检测主从库线程是否正常",
        solution: "根据实际情况进行处理",
        level: "正常",
        id: "mysql.master_slave_library_thread",
        name: "主从库线程",
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
