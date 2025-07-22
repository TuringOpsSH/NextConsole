; (function (input, params) {
    var results = []
    var result = {
        _sid: "",
        desc: "查询从未使用过的索引（只显示前50条内的详细内容）",
        effect: "影响查询效率",
        solution: "删除无效索引",
        level: "正常",
        id: "mysql.invalid_index_index_never_used",
        name: "无效索引",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "0",
        category: "",
        family: "log"
    }

    if (!mysqlVersion(params[3]["Value"].match(/\d+\.(?:\d+\.)*\d+/g)[0], "5.7")) {
        result.actual = "本检查不适用于该版本数据库"
        result.raw = ["本检查不适用于该版本数据库"]
        return {results: [result]}
    }

    result._sid = params[2]["Value"]
    
    if (input == null) {
        result.actual = "0条"
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

    var rrr = []

//    rrr = [[{
//        "无效索引数量":input[0].length
//    }]]


//    for (var i = 0; i<50; i++) {
//        if (!(input[0][i].object_schema in rrr)) {
//            var c = {}
//            c[input[0][i].object_name] = [input[0][i].index_name]
//            rrr[input[0][i].object_schema] = c
//        } else {
//            if (!(input[0][i].object_name in rrr[input[0][i].object_schema])) {
//                var c = {}
//                c[input[0][i].object_name] = [input[0][i].index_name]
//                rrr[input[0][i].object_schema][input[0][i].object_name] = [input[0][i].index_name]
//            } else {
//                rrr[input[0][i].object_schema][input[0][i].object_name].push(input[0][i].index_name)
//            }
//        }
//    }

    var max_show = 0

    if (input[0].length > 50) {
        max_show = 50
    } else {
        max_show = input[0].length
    }

    for (var i = 0; i < max_show; i++) {
        rrr.push(input[0][i])
    }

    result.raw = [rrr]
    result.level = "中风险"
    result.expected = "0条"
    result.actual = input[0].length + "条"
    result.effect = "影响查询效率"
    result.solution = "删除无效索引"
    result.mixraw = input


    results.push(result)
    return { results: results }

})(input, params)
