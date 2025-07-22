; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "检查 DG 配置参数",
        level: "正常",
        id: "oracle.dg_parameters",
        name: "DG 配置参数检查",
        mixraw: [],
        raw: [],
        actual: "DG 配置参数检查正常",
        expected: "DG 配置参数检查正常",
        category: "",
        family: "conf"
    }
    
    if (!input) {
        result.actual = "未发现配置信息"
        return { results: [result] }
    }
    // $.print(input)
    if (result.family == "status"){
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        result.actual = "未发现配置信息"
        return { results: [result] }
    }
    result.raw=raw
    results.push(result)
    return { results: results }

})(input)
