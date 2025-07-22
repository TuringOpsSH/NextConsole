; (function (input, params) {
    try {
        if (Number(params[3].Value) >= 12) {
            return
        }
    } catch { }

    var results = []
    var result = {
        desc: "",
        effect: "不符合安全合规要求",
        solution: "检查权限分配是否合理",
        level: "正常",
        id: "oracle.userpriv",
        name: "用户权限检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "合理分配用户权限",
        category: "系统安全及审计",
        family: "conf"
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

    for (i = 0; i < raw.length; i++) {
        mixlevel = ""
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["username"] //string
        // fields["granted_role"] //string
        // fields["admin_option"] //string
        // fields["default_role"] //string
        // fields["yesno"] //string
        if (fields["yesno"] != "NO") {
            if (fields["granted_role"] == "DBA" || fields["granted_role"] == "SYSDBA" || fields["granted_role"] == "SYSOPER") {
                result.actual += fields["username"] + "拥有dba权限; "
            } else {
                result.actual += fields["username"] + "拥有高风险权限(" + fields["granted_role"] + "); "
            }
            result.level = "中风险"
            mixlevel = "中风险"
        } else {
            mixlevel = "正常"
        }

        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }
    // if (result.desc == "") {
    //     result.actual = "用户权限检查正常"
    // }

    results.push(result)
    return { results: results }

})(input, params)
