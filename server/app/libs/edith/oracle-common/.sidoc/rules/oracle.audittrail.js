; (function (input, params) {
    try {
        if (Number(params[3].Value) >= 12) {
            return
        }
    } catch { }

    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "oracle.audittrail",
        name: "近期审计明细检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "",
        category: "系统安全及审计",
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

        // fields["username"] //string
        // fields["tm"] //string
        // fields["obj_name"] //string
        // fields["action_name"] //string
        // fields["sql_text"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input, params)
