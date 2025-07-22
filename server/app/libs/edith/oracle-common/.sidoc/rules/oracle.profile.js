; (function (input, params) {
    try {
        if (Number(params[3].Value) >= 12) {
            return
        }
    } catch { }

    var results = []
    var result = {
        desc: "",
        effect: "可能不满足需求",
        solution: "确认 PASSWORD_LIFE_TIME 设置是否满足需求",
        level: "正常",
        id: "oracle.profile",
        name: "PASSWORD_LIFE_TIME 检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "PASSWORD_LIFE_TIME 设置为 UNLIMITED",
        category: "系统安全及审计",
        family: "conf"
    }

    if (!input) {
        result.actual = "未发现 profile 信息"
        return { results: [result] }
    }

    if (result.family == "status") {
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        result.actual = "未发现 profile 信息"
        return { results: [result] }
    }

    for (i = 0; i < raw.length; i++) {
        mixlevel = ""
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["profile"] //string
        // fields["resource_name"] //string
        // fields["resource_type"] //string
        // fields["limit"] //string
        if (fields["resource_name"] == "PASSWORD_LIFE_TIME") {
            if (fields["limit"] != "UNLIMITED") {
                result.desc = "PASSWORD_LIFE_TIME 设置为" + fields["limit"]
                result.actual = "PASSWORD_LIFE_TIME 设置为" + fields["limit"]
                result.level = "低风险"
                mixlevel = "低风险"
            } else {
                mixlevel = "正常"
            }
        }

        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input, params)
