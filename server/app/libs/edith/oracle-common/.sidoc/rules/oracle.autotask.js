; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "oracle.autotask",
        name: "系统自动任务检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "系统自动任务设置合理",
        category: "系统对象检查",
        family: "conf"
    }

    if (!input) {
        result.actual = "未发现系统自动任务"
        return { results: [result] }
    }

    if (result.family == "status") {
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        result.actual = "未发现系统自动任务"
        return { results: [result] }
    }

    for (i = 0; i < raw.length; i++) {
        mixlevel = ""
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["autotask"] //string
        // fields["conf"] //string
        // fields["warning"] //string
        if (fields["warning"] != "NO") {
            mixlevel = "中风险"
            result.level = "中风险"
            if (fields["autotask"] == "auto optimizer stats collection") {
                result.solution += "开启统计信息自动任务; "
                result.actual += fields["autotask"] + "未自动运行; "
            } else if (fields["autotask"] == "auto space advisor" || fields["autotask"] == "sql tuning advisor") {
                result.solution += "关闭空间建议和语句调整建议自动任务; "
                result.actual += fields["autotask"] + "自动运行; "
            }
        } else {
            mixlevel = "正常"
        }

        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)
