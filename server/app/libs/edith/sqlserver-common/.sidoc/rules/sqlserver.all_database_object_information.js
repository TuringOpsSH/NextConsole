; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "sqlserver.all_database_object_information",
        name: "所有数据库检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "所有数据库检查正常",
        category: "",
        family: "any"
    }

    // 非空且元素是字符串认定为执行遇到异常
    try {
        if (Array.isArray(input) && input.length > 0) {
            var allStrings = input.every(function (item) {
                return typeof item === 'string';
            });
            if (allStrings) {
                return { results: [result] };
            }
        }
    } catch (error) {
        return { results: [result] }
    }

    try {
        raw = input
        result.raw = $.copy(input)
    } catch (err) {
        $.print(err.message)
        return { results: [result] }
    }

    if (!raw) {
        return { results: [result] }
    }

    if (raw.length != 0) {
        if (typeof raw[0] === 'string') {
            $.print("all_database_object_information", raw)
            return { results: [result] }
        }
    }

    for (i = 0; i < raw.length; i++) {
        mixlevel = "正常"
        fields = {}
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["database_id"] //string
        // fields["database_name"] //string
        // fields["create_date"] //string
        // fields["recovery_model_desc"] //string
        // fields["collation_name"] //string
        // fields["user_access_desc"] //string
        // fields["state_desc"] //string
        // fields["create_stats_on"] //string
        // fields["update_stats_on"] //string
        // fields["close_on"] //string
        // fields["shrink_on"] //string
        // fields["update_stats_async_on"] //string
        // fields["compatibility_level"] //string
        // fields["log_reuse_wait_desc"] //string
        // fields["page_verify_option_desc"] //string
        // fields["is_cdc_enabled"] //string
        // fields["td"] //string
        // fields["mirroring_state"] //string
        // fields["data_file_size_mb"] //string
        // fields["log_size_mb"] //string
        // fields["database_size_mb"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)