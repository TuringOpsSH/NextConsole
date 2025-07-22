;(function (input) {
    var results = []
    var result = {
        desc: "列出单客户端单日访问httpd服务大于500次请求的IP",
        effect: "系统可能受到攻击",
        solution: "在该IP不是测试或白名单IP的前提下考虑关闭其访问权限",
        level: "",
        id: "apache.status.gt500ip",
        name: "异常客户访问检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "单日单客户端访问小于500次",
        category: "日志排查",
        family: "status"
    }

    if (!input) {
        result.actual = "暂无异常访问记录"
        result.level = "低风险"
        return {results: [result]}
    }


    if (result.family == "status") {
        result.raw = input[0]["metric"]
    } else {
        result.raw = input
    }

    if (!result.raw) {
        result.actual = "暂无异常访问记录"
        result.level = "低风险"
        return {results: [result]}
    }

    for (var j = 0; j < input[0]["metric"].length; j++) {
        if (input[0]["metric"][j]["count"] > 500) {
            result.actual = "存在访问量大于500的IP，详见下方“Apache 动态参数项检查”"
            result.level = "中风险"
            result.mixraw.push({
                ip: input[0]["metric"][j]["ip"],
                count: input[0]["metric"][j]["count"],
            })
        }
    }

    results.push(result)
    return {results: results}

})(input)
