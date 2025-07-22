; (function (input) {
    var results = []
    var result = {
        desc: "客户端访问httpd服务，获取页面非正常状态的次数",
        effect: "评估系统的可用性",
        solution: "请检查应用程序是否有接口发生错误或有页面发生错误",
        level: "低风险",
        id: "apache.status.errreq",
        name: "非正常页面检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "不存在非200状态码的请求",
        category: "日志排查",
        family: "status"
    }

    if (!input) {
        result.actual = "暂无异常访问记录"
        result.level = "低风险"
        return { results: [result] }
    }
    result.actual = "存在异常访问记录，详见下方“Apache 动态参数项检查”"
    result.mixraw = input[0]["metric"]
    result.raw = input[0]["metric"]
    var count = 0
    for (var i = 0; i < input[0]["metric"].length; i++) {
        count = count + input[0]["metric"][i]["count"]
    }
    if (count > 50) {
        result.level = "中风险"
    }

    results.push(result)
    return { results: results }

})(input)
