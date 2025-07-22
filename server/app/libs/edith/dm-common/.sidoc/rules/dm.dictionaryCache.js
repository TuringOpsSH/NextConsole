;(function (input) {
    var results = []
    var result = {
        desc: "字典缓存",
        effect: "当字典缓存存在问题时，可能导致数据查询错误或性能下降。",
        solution: "建议检查字典缓存的配置和使用情况，确保其正常运行。如果发现问题，可以尝试重新加载字典缓存或修复相关的错误。",
        level: "正常",
        id: "dm.dictionaryCache",
        name: "字典缓存",
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
