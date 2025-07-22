; (function (input) {
    results = []
    result = {
        desc: "",
        id: "linux.cpuUsedPercent",
        mixraw: [],
        raw: [],
        actual: "",
        effect: "可能影响业务运行",
        solution: "排查各应用使用 CPU 情况",
        level: "正常",
        name: "CPU 使用率检查",
        expected: "使用率小于 75%",
        category: "系统容量检查",
        family: "status"
    }

    try {
        raw = input
        for (i = 0; i < raw.length; i++) {
            mixlevel = "正常"
            fields = raw[i]
            fields["metric"] = fields["metric"].toFixed(2)

            if (Number(fields["metric"]) >= 75) {
                mixlevel = "高风险"
                result.actual = "使用率大于 75%"
                result.level = "高风险"
            }

            fields["mixlevel"] = mixlevel
            result.mixraw.push(fields)
        }
    } catch (err) {
        $.print(err.message)
        result.actual = "无数据"
    }

    results.push(result)
    return { results: results }
})(input)
