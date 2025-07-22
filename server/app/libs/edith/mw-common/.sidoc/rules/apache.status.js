function createRaw(key, v) {
    var r = {}
    r[key] = v
    return r
}

;(function (input) {
    var results = []
    if (!input) {
        var result = {
            desc: "server-status指标检查",
            effect: "",
            solution: "需要具体分析",
            level: "低风险",
            id: "apache.status",
            name: "指标检查",
            mixraw: [],
            raw: [],
            actual: "",
            expected: "无异常指标",
            category: "指标检查",
            family: "status"
        }
        return {results: [result]}
    }

    var key = Object.keys(input[0]["metric"])
    for (var i = 0; i < key.length; i++) {
        var result = {
            desc: "server-status指标检查",
            effect: "",
            solution: "需要具体分析",
            level: "低风险",
            id: "apache.status",
            name: "指标检查",
            mixraw: [],
            raw: [],
            actual: "",
            expected: "无异常指标",
            category: "指标检查",
            family: "status"
        }

        var errResult = {
            desc: "server-status指标检查",
            effect: "",
            solution: "需要具体分析",
            level: "中风险",
            id: "apache.status",
            name: "指标检查",
            mixraw: [],
            raw: [],
            actual: "",
            expected: "无异常指标",
            category: "指标检查",
            family: "status"
        }
        switch (key[i]) {
            case "cpu_load":
                if (parseFloat(input[0]["metric"][key[i]]) > 0.7) {
                    errResult.actual = input[0]["metric"][key[i]] * 100 + "%"
                    errResult.desc = "Apache进程的CPU使用率"
                    errResult.expected = "使用率低于70%"
                    errResult.id = "apache.status." + key[i]
                    errResult.raw = createRaw(key[i], input[0]["metric"][key[i]])
                    results.push(errResult)
                } else {
                    result.actual = input[0]["metric"][key[i]] * 100 + "%"
                    result.desc = "0" + "Apache进程的CPU使用率"
                    result.expected = "使用率低于70%"
                    result.id = "apache.status." + key[i]
                    result.raw = createRaw(key[i], input[0]["metric"][key[i]])
                    results.push(result)
                }
                break
            case "requests_currently_being_processed":
                if (input[0]["metric"][key[i]] > 200) {
                    errResult.actual = input[0]["metric"][key[i]]
                    errResult.desc = "当前正在处理的请求"
                    errResult.expected = "请求数小于200"
                    errResult.id = "apache.status." + key[i]
                    errResult.raw = createRaw(key[i], input[0]["metric"][key[i]])
                    results.push(errResult)
                } else {
                    result.actual = input[0]["metric"][key[i]]
                    result.desc = "当前正在处理的请求"
                    result.expected = "请求数小于200"
                    result.id = "apache.status." + key[i]
                    result.raw = createRaw(key[i], input[0]["metric"][key[i]])
                    results.push(result)
                }
                break
            case "idle_workers":
                if (input[0]["metric"][key[i]] < 50) {
                    errResult.actual = input[0]["metric"][key[i]]
                    errResult.desc = "空闲的活动数"
                    errResult.expected = "大于50"
                    errResult.id = "apache.status." + key[i]
                    errResult.raw = createRaw(key[i], input[0]["metric"][key[i]])
                    results.push(errResult)
                } else {
                    result.actual = input[0]["metric"][key[i]]
                    result.desc = "空闲的活动数"
                    result.expected = "大于50"
                    result.id = "apache.status." + key[i]
                    result.raw = createRaw(key[i], input[0]["metric"][key[i]])
                    results.push(result)
                }
                break
            default:
                result.desc = "动态参数，仅作展示"
                result.expected = "无"
                result.id = "apache.status." + key[i]
                result.raw = createRaw(key[i], input[0]["metric"][key[i]])
                results.push(result)
                break
        }
    }

    return {results: results}

})(input)
