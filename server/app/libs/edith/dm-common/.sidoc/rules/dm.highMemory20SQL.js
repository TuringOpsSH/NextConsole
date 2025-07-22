;(function (input) {
    var results = []
    var result = {
        desc: "高内存的20条SQL",
        effect: "高内存的20条SQL可能导致数据库性能下降，甚至引发数据库崩溃。",
        solution: "优化高内存的20条SQL，减少内存占用，提高数据库性能。",
        level: "正常",
        id: "dm.highMemory20SQL",
        name: "高内存的20条SQL",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "",
        category: "",
        family: ""
    }

    if (!input) {
        result.actual = "查询结果为空"
        return {results: [result]}
    }
    try {
        // for (let i = 0; i < input.length; i++) {
        //     obj = {}
        //     obj = $.copy(input[i])
        //     s = (obj["SqlText"]).replace(/\n/g, ` `)
        //     s1 = s.replace(/$/g, `\\$`)
        //     obj["SqlText"] = s1
        //     result.raw.push(obj)
        // }
        result.raw = input
    } catch (err) {
        $.print(err.message)
        result.level = "低风险"
        result.actual = "原始数据异常"
        result.solution = ""
    }
    // $.print(err.message)
    results.push(result)
    return {results: results}

})(input)
