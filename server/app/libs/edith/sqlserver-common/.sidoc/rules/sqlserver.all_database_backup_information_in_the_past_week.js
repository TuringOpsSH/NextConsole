; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "sqlserver.all_database_backup_information_in_the_past_week",
        name: "近一周所有数据库备份信息检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "近一周所有数据库备份信息检查正常",
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
        raw = input.slice(0, 100)
        result.raw = $.copy(input.slice(0, 100))
    } catch (err) {
        $.print(err.message)
        return { results: [result] }
    }

    if (!raw) {
        return { results: [result] }
    }

    if (raw.length != 0) {
        if (typeof raw[0] === 'string') {
            $.print("all_database_backup_information_in_the_past_week", raw)
            return { results: [result] }
        }
    }

    var reg = new RegExp('\\$', "g")
    for (i = 0; i < raw.length; i++) {
        mixlevel = "正常"
        fields = {}
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["server_name"] //string
        // fields["user_name"] //string
        fields["user_name"] = fields["user_name"].replace(reg, "\\\$")
        // fields["database_name"] //string
        // fields["bak_start_time"] //string
        // fields["bak_end_time"] //string
        // fields["bak_time_seconds"] //string
        // fields["bak_files"] //string
        // fields["bak_file_available"] //string
        // fields["bak_type"] //string
        // fields["bak_size_mb"] //string
        // fields["compressed_size_mb"] //string
        // fields["first_lsn"] //string
        // fields["last_lsn"] //string
        // fields["checkpoint_lsn"] //string
        // fields["database_backup_lsn"] //string
        // fields["software_major_version"] //string
        // fields["software_minor_version"] //string
        // fields["software_build_version"] //string
        // fields["recovery_model"] //string
        // fields["collation_name"] //string
        // fields["database_version"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)