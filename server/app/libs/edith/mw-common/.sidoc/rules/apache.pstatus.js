;(function (input) {
    var results = []
    var result1 = {
        desc: "server-status指标检查",
        effect: "",
        solution: "需要具体分析",
        level: "低风险",
        id: "apache.pstatus",
        name: "指标检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "无异常指标",
        category: "指标检查",
        family: "status"
    }
    var errResult1 = {
        desc: "server-status指标检查",
        effect: "",
        solution: "需要具体分析",
        level: "中风险",
        id: "apache.pstatus",
        name: "指标检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "无异常指标",
        category: "指标检查",
        family: "status"
    }
    var result2 = {
        desc: "server-status指标检查",
        effect: "",
        solution: "需要具体分析",
        level: "低风险",
        id: "apache.pstatus",
        name: "指标检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "无异常指标",
        category: "指标检查",
        family: "status"
    }
    var errResult2 = {
        desc: "server-status指标检查",
        effect: "",
        solution: "需要具体分析",
        level: "中风险",
        id: "apache.pstatus",
        name: "指标检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "无异常指标",
        category: "指标检查",
        family: "status"
    }

    if (input[0]["metric"]["network_info"]) {
        result1.actual = input[0]["metric"]["network_info"][0]["ipport"]
        result1.id = "apache.pstatus.network"
        result1.name = "端口监听检查"
        result1.raw = input[0]["metric"]["network_info"][0]
        result1.expected = "不为空"
        results[0] = result1
    } else {
        errResult1.actual = "空"
        errResult1.id = "apache.pstatus.network"
        errResult1.name = "端口监听检查"
        errResult1.raw = null
        errResult1.expected = "不为空"
        results.push(errResult1)
    }

    if (input[0]["metric"]["process_num"] !== 0) {
        errResult2.id = "apache.pstatus.process"
        errResult2.name = "Z进程检查"
        errResult2.expected = 0
        errResult2.actual = input[0]["metric"]["process_num"]
        errResult2.raw = input[0]["metric"]["process_num"]
        results.push(errResult2)
    } else {
        result2.id = "apache.pstatus.process"
        result2.name = "Z进程检查"
        result2.expected = 0
        result2.actual = 0
        result2.id = "apache.status.process"
        result2.raw = input[0]["metric"]["process_num"]
        results.push(result2)
    }

    return {results: results}
})(input)
