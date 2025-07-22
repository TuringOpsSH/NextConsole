; (function (input, params) {
    var results = []
    var result = {
        _sid:"",
        desc: "二进制日志",
        effect: "记录二进制日志，用于数据恢复和主从同步",
        solution: "开启二进制日志",
        level: "中风险",
        id: "mysql.binary_log",
        name: "二进制日志",
        mixraw: [],
        raw: input,
        actual: input,
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
        if (input[0] == "You are not using binary logging") {
            result.actual = "未开启二进制日志"
            result.raw = ["未开启二进制日志"]
            return {results: [result]}
        }
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
