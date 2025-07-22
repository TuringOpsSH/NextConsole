; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "检查调整计划任务窗口",
        level: "正常",
        id: "oracle.scheduler_windows",
        name: "计划任务窗口状态检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "计划任务窗口状态正常",
        category: "系统对象检查",
        family: "conf"
    }

    if (!input) {
        result.actual = "未发现计划任务窗口异常信息"
        return { results: [result] }
    }

    if (result.family == "status") {
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        result.actual = "未发现计划任务窗口异常信息"
        return { results: [result] }
    }

    for (i = 0; i < raw.length; i++) {
        result.actual = "计划任务窗口状态异常"
        result.level = "中风险"
        mixlevel = "中风险"
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["window_name"] //string
        // fields["next_start_date"] //string
        // fields["enabled"] //string
        // fields["active"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)
