; (function (input) {
    if (!input) {
        return { results: [] }
    }
    var results = []
    if (Number(input["kernel.sysrq"]) != 1) {
        results.push({
            desc: "" ,
            actual: input["kernel.sysrq"],
            expected: "kernel.sysrq 设置为 1",
            effect: "发生故障时可能无法收集部分信息",
            solution: "设置 kernel.sysrq 为 1",
            level: "中风险",
            id: "linux.sysrq",
            name: "是否启用魔术键检查",
            category: "系统健康检查"
        })
    } else {
        results.push({
            desc: "",
            actual: input["kernel.sysrq"],
            expected: "kernel.sysrq 设置为 1",
            effect: "发生故障时可能无法收集部分信息",
            solution: "设置 kernel.sysrq 为 1",
            level: "正常",
            id: "linux.sysrq",
            name: "是否启用魔术键检查",
            category: "系统健康检查"
        })
    }
    return { results: results }

})(input)
