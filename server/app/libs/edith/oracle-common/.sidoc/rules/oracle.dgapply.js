; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "检查日志传输及应用",
        level: "正常",
        id: "oracle.dgapply",
        name: "DG 日志应用检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "DG 日志应用检查正常",
        category: "系统备份",
        family: "status"
    }

    if (!input) {
        result.actual = "未发现相关记录"
        return { results: [result] }
    }

    if (result.family == "status") {
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        result.actual = "未发现相关记录"
        return { results: [result] }
    }

    for (i = 0; i < raw.length; i++) {
        mixlevel = ""
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["thread"] //string
        // fields["name"] //string
        // fields["open_mode"] //string
        // fields["protection_mode"] //string
        // fields["protection_level"] //string
        // fields["database_role"] //string
        // fields["switchover_status"] //string
        // fields["applog"] //string
        // fields["nowlog"] //string
        // fields["YESNO"] //string
        if ((Number(fields["nowlog"]) - Number(fields["applog"])) > 3) {
            result.desc == "DG 日志应用延时过大"
            result.actual = "DG 日志应用延时过大"
            result.level = "高风险"
            mixlevel = "高风险"
        } else {
            mixlevel = "正常"
        }

        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)
