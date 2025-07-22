;(function (input, params) {
    var results = []
    var result = {
        _sid: "",
        desc: "克隆进度和状态",
        effect: "该规则用于检查MySQL克隆进度和状态是否正常。",
        solution: "如果克隆进度和状态不正常，请参考MySQL文档进行排查。",
        level: "正常",
        id: "mysql.cloning_progress_and_status",
        name: "克隆状态",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "克隆进度和状态正常",
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
    return {results: results}

})(input, params)
