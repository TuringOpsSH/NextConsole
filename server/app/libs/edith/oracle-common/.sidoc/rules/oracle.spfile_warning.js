; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "检查并修正优先级设置",
        level: "正常",
        id: "oracle.spfile_warning",
        name: "spfile 参数设置优先级一致性检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "spfile 参数设置优先级一致",
        category: "数据库组件及参数设置",
        family: "status"
    }

    if (!input) {
        if (result.actual == "") {
            result.actual = "数据异常，请检查是否包含非法字符"
        }
        return { results: [result] }
    }

    if (result.family == "status") {
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        if (result.actual == "") {
            result.actual = "数据异常，请检查是否包含非法字符"
        }
        return { results: [result] }
    }

    for (i = 0; i < raw.length; i++) {
        mixlevel = ""
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["inst_id"] //int
        // fields["sid"] //string
        // fields["name"] //string
        // fields["value"] //string
        // fields["warning"] //string
        if (fields["warning"] == "YES") {
            mixlevel = "中风险"
            result.actual = "spfile 参数设置优先级不一致"
            result.level = "中风险"
        } else {
            mixlevel = "正常"
        }

        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    if (result.actual == "") {
        result.actual = "未发现优先级设置异常"
    }

    results.push(result)
    return { results: results }

})(input)

