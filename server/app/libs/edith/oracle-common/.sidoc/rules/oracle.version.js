; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "oracle.version",
        name: "数据库版本检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "",
        category: "conf",
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

        // fields["dbid"] //int
        fields["dbid"] = fields["dbid"].toString()
        // fields["name"] //string
        // fields["version"] //string
        // fields["cluster_database"] //string
        // fields["created"] //string
        // fields["resetlogs_change"] //int
        fields["resetlogs_change"] = fields["resetlogs_change"].toString()
        // fields["resetlogs_time"] //string
        // fields["log_mode"] //string
        // fields["checkpoint_change"] //int
        fields["checkpoint_change"] = fields["checkpoint_change"].toString()
        // fields["open_mode"] //string
        // fields["protection_mode"] //string
        // fields["protection_level"] //string
        // fields["database_role"] //string
        // fields["force_logging"] //string
        // fields["platform_id"] //int
        fields["platform_id"] = fields["platform_id"].toString()
        // fields["platform_name"] //string
        // fields["flashback_on"] //string


        fields["mixlevel"] = mixlevel
        if (!fields.hasOwnProperty('version')) {
            fields["version"] = '(升级 Edith 至 v1.2.3+ 可显示)'
        }
        if (!fields.hasOwnProperty('cluster_database')) {
            fields["cluster_database"] = '(升级 Edith 至 v1.2.3+ 可显示)'
        }
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)
