; (function (input, params) {
    var results = []
    var result = {
        _sid: "",
        desc: "每张表的索引区分度（前100条）",
        effect: "区分度较差，开发者应该重新评估SQL语句涉及的字段，选择区分度高的多个字段创建索引",
        solution: "重新评估SQL语句涉及的字段，选择区分度高的多个字段创建索引",
        level: "正常",
        id: "mysql.index_discrimination_of_each_table_top_100",
        name: "每张表的索引区分度",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "sel_persent > 0.1",
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
            if (input[i][j]["sel_persent"] < 0.1) {
                input[i][j]["inspectionLevel"] = "中风险"
                result.level = "中风险"
                result.expected = "sel_persent > 0.1"
                result.actual = "sel_persent = " + input[i][j]["sel_persent"]
                result.effect = "区分度较差，开发者应该重新评估SQL语句涉及的字段，选择区分度高的多个字段创建索引"
            }
        }
    }

    result.mixraw = input

    results.push(result)
    return { results: results }

})(input, params)
