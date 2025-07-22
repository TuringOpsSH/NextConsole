; (function (input, params) {
    try {
        if (Number(params[3].Value) < 12) {
            return
        }
    } catch { }

    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "检查定时任务",
        level: "正常",
        id: "oracle.jobs12c",
        name: "定时任务检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "定时任务状态正常",
        category: "系统对象检查",
        family: "status"
    }

    if (!input) {
        result.actual = "未发现定时任务"
        return { results: [result] }
    }

    if (result.family == "status") {
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        result.actual = "未发现定时任务"
        return { results: [result] }
    }

    var reg = new RegExp('\\$', "g")
    for (i = 0; i < raw.length; i++) {
        mixlevel = ""
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["name"] //string
        // fields["job"] //string
        // fields["priv_user"] //string
        // fields["what"] //string
        // fields["status"] //string
        // fields["warning"] //string

        fields["name"] = fields["name"].replace(reg, "\\\$") 
        if (fields["warning"] != "NO") {
            result.actual += "定时任务(" + fields["job"] + ")状态异常; "
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

})(input, params)