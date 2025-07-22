; (function (input, params) {
    var results = []
    var result = {
        _sid: "",
        desc: "查询所有用户",
        effect: "权限过高，不符合审计规则",
        solution: "修改权限，删除不必要的用户",
        level: "正常",
        id: "mysql.query_all_users",
        name: "所有用户",
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

    for (var i = 0; i < input.length; i++) {
        for (var j = 0; j < input[i].length; j++) {
            if (input[i][j]["HOST"] == "%") {
                input[i][j]["inspectionLevel"] = "中风险"
                result.level = "中风险"
                result.actual = input[i][j]["HOST"]
                result.expected = "不含有 % 的用户"
                result.effect = "权限过高，不符合审计规则"
            }
        }
    }

    result.mixraw = input

    results.push(result)
    return { results: results }

})(input, params)
