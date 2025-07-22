; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "关注 open cursor 使用",
        level: "正常",
        id: "oracle.cursor_monitor",
        name: "open cursor 使用比例最高的前10个会话检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "不超过75%",
        category: "系统对象检查",
        family: "status"
    }

    if (!input) {
        result.actual = "未发现 open cursor 使用信息"
        return { results: [result] }
    }

    if (result.family == "status") {
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        result.actual = "未发现 open cursor 使用信息"
        return { results: [result] }
    }

    for (i = 0; i < raw.length; i++) {
        mixlevel = ""
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["sid"] //int
        // fields["value"] //string
        // fields["parameter"] //string
        pct = Number(fields["value"]) / Number(fields["parameter"]) * 100
        if (pct > 75) {
            result.actual += fields["sid"] + "# Session open cursor 使用比例达" + Math.round(pct) + "%; "
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
