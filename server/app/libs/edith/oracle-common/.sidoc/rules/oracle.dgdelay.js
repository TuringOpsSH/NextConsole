; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "检查日志传输及应用",
        level: "正常",
        id: "oracle.dgdelay",
        name: "DG 日志应用延时检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "DG 日志应用延时正常",
        category: "系统备份",
        family: "status"
    }

    if (!input) {
        result.desc = "未发现相关记录"
        result.actual = "未发现相关记录"
        return { results: [result] }
    }

    if (result.family == "status") {
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        result.desc = "未发现相关记录"
        result.actual = "未发现相关记录"
        return { results: [result] }
    }

    for (i = 0; i < raw.length; i++) {
        mixlevel = ""
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["process"] //string
        // fields["status"] //string
        // fields["group"] //string
        // fields["thread"] //string
        // fields["sequence"] //string
        // fields["delay_mins"] //string
        // fields["YESNO"] //string
        if (fields["YESNO"] == "YES") {
            result.actual = "DG 日志应用延时异常"
            result.level = "中风险"
            mixlevel = "中风险"
        } else {
            mixlevel = "正常"
        }

        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)
