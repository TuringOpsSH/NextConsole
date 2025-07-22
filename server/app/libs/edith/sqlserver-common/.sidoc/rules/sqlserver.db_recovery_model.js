; (function (input) {
    var results = []
    var result = {
        desc: "检查数据库恢复模式是否为FULL",
        effect: "检查数据库恢复模式是否为FULL",
        solution: "数据库的恢复模式最好使用FULL,并且做好日志备份",
        level: "正常",
        id: "sqlserver.db_recovery_model",
        name: "数据库恢复模式检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "数据库恢复模式检查正常",
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
        // fields["recovery_mode"] //string
        if (fields["recovery_mode"] != "FULL") {
            mixlevel = "中风险"
            result.level = "中风险"
            result.actual += fields["database_name"] + "恢复模式为" + fields["recovery_mode"] + ";"
        }

        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)