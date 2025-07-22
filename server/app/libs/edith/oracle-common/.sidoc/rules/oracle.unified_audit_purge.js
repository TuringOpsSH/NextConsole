; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "oracle.unified_audit_purge",
        name: "统一审计清理任务检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "启用统一审计清理任务",
        category: "系统安全及审计",
        family: "status"
    }

    if (!input) {
        result.desc = "未发现统一审计清理任务"
        result.actual = "未发现统一审计清理任务"
        return { results: [result] }
    }

    if (result.family == "status") {
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        result.desc = "未发现统一审计清理任务"
        result.actual = "未发现统一审计清理任务"
        return { results: [result] }
    }

    for (i = 0; i < raw.length; i++) {
        mixlevel = ""
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["job_name"] //string
        // fields["job_status"] //string
        // fields["audit_trail"] //string
        // fields["job_frequency"] //string
        // fields["use_last_archive_timestamp"] //string
        // fields["job_container"] //string
        if (fields["job_status"] != "ENABLED") {
            mixlevel = "中风险"
            result.level = "中风险"
            result.actual = "未启用统一审计清理任务"
        } else {
            mixlevel = "正常"
        }

        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)
