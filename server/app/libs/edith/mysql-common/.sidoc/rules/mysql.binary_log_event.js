; (function (input, params) {
    var results = []
    var result = {
        _sid: "",
        desc: "二进制日志事件",
        effect: "该规则用于检测 MySQL 二进制日志事件是否正常",
        solution: "请检查 MySQL 二进制日志事件是否正常",
        level: "正常",
        id: "mysql.binary_log_event",
        name: "二进制日志事件",
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
        return { results: [result] }
    }

    if (typeof input[0] == "string") {
        result.expected = "无 SQL 报错并展示查询结果"
        result.level = "中风险"
        result.actual = input
        result.raw = input
        results.push(result)
        return { results: results }
    }
    result.raw = input

    for (i = 0; i < input[0].length; i++) {
        var ks = Object.keys(input[0][i])
        for (j = 0; j < ks.length; j++) {
            input[0][i][ks[j]] = input[0][i][ks[j]].replace(/\n/g, " ").replace(/`/g, "")
        }
    }

    results.push(result)
    return { results: results }

})(input, params)
