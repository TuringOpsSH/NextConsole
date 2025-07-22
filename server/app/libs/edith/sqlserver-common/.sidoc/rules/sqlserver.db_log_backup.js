; (function (input) {
    var results = []
    var result = {
        desc: "检查数据库事务日志备份是否正常",
        effect: "检查数据库事务日志备份是否正常",
        solution: "排查为NULL的结果日志备份是否正常, 如果不正常则进行修复",
        level: "正常",
        id: "sqlserver.db_log_backup",
        name: "数据库事务日志备份检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "数据库事务日志备份检查正常",
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

    for (i = 0; i < raw.length; i++) {
        mixlevel = "正常"
        fields = {}
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["database_name"] //string
        // fields["database_recovery_mode"] //string
        // fields["backup_type"] //string
        // fields["last_backup_time"] //string
        if (fields["last_backup_time"] == "NULL" && fields["backup_type"] != "NULL") {
            mixlevel = "中风险"
            result.level = "中风险"
            result.actual += fields["database_name"] + "状态为" + fields["last_backup_time"] + ";"
        }

        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)