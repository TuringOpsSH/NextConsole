;(function (input) {
    var results = []
    var result = {
        desc: "数据文件信息",
        effect: "当数据文件信息不完整或异常时，可能导致数据操作错误或数据丢失。",
        solution: "检查数据文件信息，确保其完整性和正确性。",
        level: "正常",
        id: "dm.dataDocInfo",
        name: "数据文件信息",
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
