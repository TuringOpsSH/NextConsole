; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "oracle.mount",
        name: "文件系统挂载信息检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "",
        category: "文件系统挂载信息检查",
        family: "conf"
    }
    
    if (!input) {
        return { results: [result] }
    }

    if (result.family == "status"){
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
        // fields["name"] //string
        // fields["created"] //string
        // fields["resetlogs_change"] //int
        // fields["resetlogs_time"] //string
        // fields["log_mode"] //string
        // fields["checkpoint_change"] //int
        // fields["open_mode"] //string
        // fields["protection_mode"] //string
        // fields["protection_level"] //string
        // fields["database_role"] //string
        // fields["force_logging"] //string
        // fields["platform_id"] //int
        // fields["platform_name"] //string
        // fields["flashback_on"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }
    
    results.push(result)
    return { results: results }

})(input)
