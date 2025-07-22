
; (function (input, params) {

    var results = []
    var result = {
        _sid: "",
        desc: "innodb buffer pool size ",
        effect: "资源浪费或性能下降",
        solution: "innodb buffer pool size 占内存总量的50%-70%之间",
        level: "正常",
        id: "mysql.innodb_buffer_pool_size",
        name: "innodb buffer pool size",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "innodb buffer pool size 占内存总量的50%-70%之间",
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

    result.expected = "innodb buffer pool size 占内存总量的50%-70%之间"

    var pct = input[0]["innodb_buffer_pool_size"] / input[0]["memory"]

    if (pct < 0.5) {
        result.actual = pct
        result.level = "高风险"
        result.effect = "资源浪费"
    }

    if (pct > 0.7) {
        result.actual = pct
        result.level = "高风险"
        result.effect = "性能下降"
    }

    result.mixraw = input

    results.push(result)
    return { results: results }

})(input, params)
