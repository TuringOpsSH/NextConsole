; (function (input) {
    var results = []
    if (!input) {
        return { results: results }
    }
    var ok = true
    for (i = 0; i < input.length; i++) {
        if (input[i].match("No NUMA configuration found")) {
            ok = false
        }
    }

    if (ok) {
        results.push({
            desc: "是否开启numa检查",
            solution: "开启numa",
            level: "正常",
            effect: "无影响",
            id: "linux.numastat",
            name: "是否开启numa检查",
            category: "系统健康检查",
            actual:"NUMA configuration found",
            expected:"NUMA configuration found"
        })
    } else {
        results.push({
            desc: "是否开启numa检查",
            effect: "无影响",
            solution: "开启numa",
            level: "中风险",
            id: "linux.numastat",
            name: "是否开启numa检查",
            category: "系统健康检查",
            actual:"No NUMA configuration found",
            expected:"NUMA configuration found"
        })
    }
    return { results: results }
})(input)
