; (function (input, params) {
    try {
        if (Number(params[3].Value) < 12) {
            return
        }
    } catch { }

    var results = []
    var result = {
        desc: "",
        effect: "影响用户登录使用数据库",
        solution: "及时修改用户口令无",
        level: "正常",
        id: "oracle.userinfo12c",
        name: "用户口令有效期检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "用户口令有效期大于90天",
        category: "系统安全及审计",
        family: "status"
    }

    if (!input) {
        return { results: [result] }
    }

    if (result.family == "status") {
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        return { results: [result] }
    }

    var reg = new RegExp('\\$', "g")
    for (i = 0; i < raw.length; i++) {
        mixlevel = ""
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["name"] //string
        fields["name"] = fields["name"].replace(reg, "\\\$")
        // fields["username"] //string
        fields["username"] = fields["username"].replace(reg, "\\\$")
        // fields["default_tablespace"] //string
        // fields["temporary_tablespace"] //string
        // fields["created"] //string
        // fields["lock_date"] //string
        // fields["expiry_date"] //string
        // fields["profile"] //string
        // fields["account_status"] //string
        // fields["yesno"] //string
        if (fields["yesno"] == "YES") {
            result.desc += fields["username"] + "用户口令将于90天内过期; "
            result.actual += fields["username"] + "用户口令将于90天内过期; "
            result.level = "中风险"
            mixlevel = "中风险"
        } else {
            mixlevel = "正常"
        }


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }
    // if (result.desc == "") {
    //     result.desc = "用户口令有效期检查正常"
    //     result.actual = "用户口令有效期检查正常"
    // }

    results.push(result)
    return { results: results }

})(input, params)
