;(function (input, params) {
    var results = []
    var result = {
        _sid: "",
        desc: "无主键或唯一键的表（前100条）",
        effect: "表中没有主键会导致从库复制严重延迟",
        solution: "请添加主键或唯一键",
        level: "正常",
        id: "mysql.table_without_primary_key_or_unique_key_top_100",
        name: "无主键或唯一键的表",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "不存在无主键或唯一键的表",
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

    result.level = "中风险"
    result.effect = "表中没有主键会导致从库复制严重延迟"
    result.actual = "详细请查看通用报告中：数据库总体概况-无主键或唯一键的表 章节"
    result.expected = "不存在无主键或唯一键的表"
    result.mixraw = input

    results.push(result)
    return {results: results}

})(input, params)
