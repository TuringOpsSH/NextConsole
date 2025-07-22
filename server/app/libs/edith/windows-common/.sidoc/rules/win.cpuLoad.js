; (function (input) {
    results = []
    result = {
        desc: "CPU 负载检查",
        id: "win.cpuLoad",
        mixraw: [],
        raw: [],
        actual: "",
        effect: "",
        solution: "",
        level: "正常",
        name: "CPU 负载检查",
        expected: "CPU 负载小于 2",
        category: "系统容量检查",
        family: "status"
    }

    try {
        raw = input
        // $.print(raw)
        for (i = 0; i < raw.length; i++) {
            mixlevel = "正常"
            fields = raw[i]

            if (Number(fields["metric"]["load1"]) > 2.0) {
                mixlevel = "高风险"
                result.actual += "CPU 1分钟负载 > 2; "
                result.level = "高风险"
            }

            if (Number(fields["metric"]["load5"]) > 2.0) {
                mixlevel = "高风险"
                result.actual += "CPU 5分钟负载 > 2; "
                result.level = "高风险"
            }

            if (Number(fields["metric"]["load15"]) > 2.0) {
                mixlevel = "高风险"
                result.actual += "CPU 15分钟负载 > 2; "
                result.level = "高风险"
            }

            fields["load1"] = fields["metric"]["load1"]
            fields["load5"] = fields["metric"]["load5"]
            fields["load15"] = fields["metric"]["load15"]
            fields["mixlevel"] = mixlevel
            result.mixraw.push(fields)
        }
    } catch (err) {
        $.print(err.message)
        result.level = "低风险"
        result.actual = "原始数据异常"
    }

    // $.print(result)
    results.push(result)
    return { results: results }
})(input)