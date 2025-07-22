; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "如sysaux 表空间满, 严重时可能影响用户登录数据库",
        solution: "关注sysaux 表空间使用, 定期清理统一审计记录",
        level: "正常",
        id: "oracle.unified_audit_option",
        name: "统计审计记录是否存放在sysaux 表空间检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "统计审计记录分别存放",
        category: "系统安全及审计",
        family: "conf"
    }

    if (!input) {
        result.actual = "未发现统一审计设置信息"
        return { results: [result] }
    }

    if (result.family == "status") {
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        result.actual = "未发现统一审计设置信息"
        return { results: [result] }
    }

    for (i = 0; i < raw.length; i++) {
        mixlevel = ""
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["parameter_name"] //string
        // fields["parameter_value"] //string
        if (fields["parameter_name"] == "DB AUDIT TABLESPACE" && fields["parameter_value"] == "SYSAUX") {
            mixlevel = "中风险"
            result.level = "中风险"
            result.actual = "未发现统一审计设置信息"
        } else {
            mixlevel = "正常"
        }


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)
