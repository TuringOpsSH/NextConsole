; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "根据错误日志进行具体分析",
        solution: "检查错误日志并启动服务",
        level: "正常",
        id: "os.chronyd",
        name: "时钟同步服务状态检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "处于running状态且无error告警",
        category: "OS 检查",
        family: "log"
    }

    try {
        raw = input.split("\n")
        result.raw = $.copy(raw)
    } catch (err) {
        $.print(err.message)
        return { results: [result] }
    }

    for (i = 0; i < raw.length; i++) {
        mixlevel = "正常"
        fields = {}
        fields["line"] = raw[i]

        if (fields["line"].match("Active:")) {
            if (fields["line"].match("running")) {
                result.level = "正常"
            } else {
                result.level = "高风险"
                mixlevel = "高风险"
            }
        }

        if (fields["line"].match("error") && !fields["line"].match("Active:")) {
            if (result.level != "高风险") {
                result.level = "中风险"
                mixlevel = "中风险"
            }
        }

        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)