;(function (input) {
    var results = []
    if (!input[0]["metric"]) {
        for (var i = 0; i < 6; i++) {
            var result = {
                desc: "",
                effect: "",
                solution: "需要具体分析",
                level: "",
                id: "",
                name: "",
                mixraw: [],
                raw: [],
                actual: "",
                expected: "",
                category: "",
                family: "status"
            }
            switch (i) {
                case 0:
                    result.actual = "未发现相关记录"
                    result.desc = "等待请求的当前空闲客户端连接数"
                    result.name = "Waiting状态检查"
                    result.expected = "大于100"
                    result.id = "nginx.gstat." + "waiting"
                    result.category = "动态参数检查"
                    results.push(result)
                    break
                case 1:
                    result.actual = "未发现相关记录"
                    result.desc = "正在读取请求头"
                    result.name = "Reading状态检查"
                    result.expected = "大于200"
                    result.id = "nginx.gstat." + "reading"
                    result.category = "动态参数检查"
                    results.push(result)
                    break
                case 2:
                    result.actual = "未发现相关记录"
                    result.desc = "成功创建多少次握手"
                    result.name = "handled状态检查"
                    result.expected = "大于6000"
                    result.id = "nginx.gstat." + "server_handled"
                    result.category = "动态参数检查"
                    results.push(result)
                    break
                case 3:
                    result.actual = "未发现相关记录"
                    result.desc = "当前活动客户端连接的数量"
                    result.name = "Active connections状态检查"
                    result.expected = "大于200"
                    result.id = "nginx.gstat." + "active_connections"
                    result.category = "动态参数检查"
                    results.push(result)
                    break
                case 4:
                    result.actual = "未发现相关记录"
                    result.desc = "总共处理了多少个请求"
                    result.name = "Requests状态检查"
                    result.expected = "大于10000"
                    result.id = "nginx.gstat." + "server_accepts"
                    result.category = "动态参数检查"
                    results.push(result)
                    break
                case 5:
                    result.actual = "未发现相关记录"
                    result.desc = "响应写回客户端的当前连接数"
                    result.name = "Writing状态检查"
                    result.expected = "大于200"
                    result.id = "nginx.gstat." + "writing"
                    results.push(result)
                    break
            }
        }
        return {results: results}
    }
    var key = Object.keys(input[0]["metric"])
    for (var i = 0; i < key.length; i++) {
        var result = {
            desc: "",
            effect: "",
            solution: "需要具体分析",
            level: "低风险",
            id: "nginx.gstat",
            name: "客户端访问量检查",
            mixraw: [],
            raw: [],
            actual: "",
            expected: "",
            category: "",
            family: "status"
        }
        var errResult = {
            desc: "",
            effect: "",
            solution: "需要具体分析",
            level: "中风险",
            id: "nginx.gstat",
            name: "指标检查",
            mixraw: [],
            raw: [],
            actual: "",
            expected: "",
            category: "指标检查",
            family: "status"
        }
        switch (key[i]) {
            case "waiting":
                if (input[0]["metric"][key[i]] > 100) {
                    errResult.actual = input[0]["metric"][key[i]]
                    errResult.desc = "等待请求的当前空闲客户端连接数"
                    errResult.name = "Waiting状态检查"
                    errResult.expected = "大于100"
                    errResult.id = "nginx.gstat." + key[i]
                    errResult.raw = input[0]["metric"][key[i]]
                    errResult.category = "动态参数检查"
                    results.push(errResult)
                } else {
                    result.actual = input[0]["metric"][key[i]]
                    result.desc = "等待请求的当前空闲客户端连接数"
                    result.name = "Waiting状态检查"
                    result.expected = "大于100"
                    result.id = "nginx.gstat." + key[i]
                    result.raw = input[0]["metric"][key[i]]
                    result.category = "动态参数检查"
                    results.push(result)
                }
                break
            case "reading":
                if (input[0]["metric"][key[i]] > 200) {
                    errResult.actual = input[0]["metric"][key[i]]
                    errResult.desc = "正在读取请求头"
                    errResult.name = "Reading状态检查"
                    errResult.expected = "大于200"
                    errResult.id = "nginx.gstat." + key[i]
                    errResult.raw = input[0]["metric"][key[i]]
                    errResult.category = "动态参数检查"
                    results.push(errResult)
                } else {
                    result.actual = input[0]["metric"][key[i]]
                    result.desc = "正在读取请求头"
                    result.name = "Reading状态检查"
                    result.expected = "大于200"
                    result.id = "nginx.gstat." + key[i]
                    result.raw = input[0]["metric"][key[i]]
                    result.category = "动态参数检查"
                    results.push(result)
                }
                break
            case "server_handled":
                if (input[0]["metric"][key[i]] > 6000) {
                    errResult.actual = input[0]["metric"][key[i]]
                    errResult.desc = "成功创建多少次握手"
                    errResult.name = "handled状态检查"
                    errResult.expected = "大于6000"
                    errResult.id = "nginx.gstat." + key[i]
                    errResult.raw = input[0]["metric"][key[i]]
                    errResult.category = "动态参数检查"
                    results.push(errResult)
                } else {
                    result.actual = input[0]["metric"][key[i]]
                    result.desc = "成功创建多少次握手"
                    result.name = "handled状态检查"
                    result.expected = "大于6000"
                    result.id = "nginx.gstat." + key[i]
                    result.raw = input[0]["metric"][key[i]]
                    result.category = "动态参数检查"
                    results.push(result)
                }
                break
            case "active_connections":
                if (input[0]["metric"][key[i]] > 200) {
                    errResult.actual = input[0]["metric"][key[i]]
                    errResult.desc = "当前活动客户端连接的数量"
                    errResult.name = "Active connections状态检查"
                    errResult.expected = "大于200"
                    errResult.id = "nginx.gstat." + key[i]
                    errResult.raw = input[0]["metric"][key[i]]
                    errResult.category = "动态参数检查"
                    results.push(errResult)
                } else {
                    result.actual = input[0]["metric"][key[i]]
                    result.desc = "当前活动客户端连接的数量"
                    result.name = "Active connections状态检查"
                    result.expected = "大于200"
                    result.id = "nginx.gstat." + key[i]
                    result.raw = input[0]["metric"][key[i]]
                    result.category = "动态参数检查"
                    results.push(result)
                }
                break
            case "server_requests":
                if (input[0]["metric"][key[i]] > 10000) {
                    errResult.actual = input[0]["metric"][key[i]]
                    errResult.desc = "总共处理了多少个请求"
                    errResult.name = "Requests状态检查"
                    errResult.expected = "大于10000"
                    errResult.id = "nginx.gstat." + key[i]
                    errResult.raw = input[0]["metric"][key[i]]
                    errResult.category = "动态参数检查"
                    results.push(errResult)
                } else {
                    result.actual = input[0]["metric"][key[i]]
                    result.desc = "总共处理了多少个请求"
                    result.name = "Requests状态检查"
                    result.expected = "大于10000"
                    result.id = "nginx.gstat." + key[i]
                    result.raw = input[0]["metric"][key[i]]
                    result.category = "动态参数检查"
                    results.push(result)
                }
                break
            case "server_accepts":
                if (input[0]["metric"][key[i]] > 6000) {
                    errResult.actual = input[0]["metric"][key[i]]
                    errResult.desc = "总共处理了多少个连接"
                    errResult.name = "Accepts状态检查"
                    errResult.expected = "大于6000"
                    errResult.id = "nginx.gstat." + key[i]
                    errResult.raw = input[0]["metric"][key[i]]
                    results.push(errResult)
                } else {
                    result.actual = input[0]["metric"][key[i]]
                    result.desc = "总共处理了多少个连接"
                    result.name = "Accepts状态检查"
                    result.expected = "大于6000"
                    result.id = "nginx.gstat." + key[i]
                    result.raw = input[0]["metric"][key[i]]
                    results.push(result)
                }
                break
            case "writing":
                if (input[0]["metric"][key[i]] > 200) {
                    errResult.actual = input[0]["metric"][key[i]]
                    errResult.desc = "响应写回客户端的当前连接数"
                    errResult.name = "Writing状态检查"
                    errResult.expected = "大于200"
                    errResult.id = "nginx.gstat." + key[i]
                    errResult.raw = input[0]["metric"][key[i]]
                    results.push(errResult)
                } else {
                    result.actual = input[0]["metric"][key[i]]
                    result.desc = "响应写回客户端的当前连接数"
                    result.name = "Writing状态检查"
                    result.expected = "大于200"
                    result.id = "nginx.gstat." + key[i]
                    result.raw = input[0]["metric"][key[i]]
                    results.push(result)
                }
                break
        }
    }
    return {results: results}
})(input)
