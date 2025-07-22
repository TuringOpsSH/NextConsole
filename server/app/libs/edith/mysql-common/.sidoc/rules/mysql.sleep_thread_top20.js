;(function (input, params) {
    var results = []
    var result = {
        _sid: "",
        desc: "sleep线程TOP20",
        effect: "需要扩大最大连接数",
        solution: "扩大最大连接数",
        level: "正常",
        id: "mysql.sleep_thread_top20",
        name: "sleep线程Top20",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "无 SQL 报错并展示查询结果sleep 线程不超过 max_connections 的 30%",
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

    if (input.length == 2) {
        if (input[0]["Value"] > input[1]["Value"]) {
            if (input[1]["Value"] / input[0]["Value"] > 0.3) {
                result.level = "中风险"
                result.actual = input[1]["Value"] / input[0]["Value"]
                result.expected = result.expected + "sleep 线程不超过 max_connections 的 30%"
                result.effect = result.effect + "需要扩大最大连接数"
            }
        }
    }

    result.mixraw = input

    results.push(result)
    return {results: results}

})(input, params)
