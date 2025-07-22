; (function (input) {
    var results = []
    var result = {
        desc: "检查数据库日志大小和使用率是否正常",
        effect: "如果数据库日志大小和使用率不正常, 可能会导致数据库性能下降或者数据库崩溃",
        solution: "可以通过定期清理日志或者增加日志文件大小来解决问题",
        level: "正常",
        id: "sqlserver.db_log_size",
        name: "数据库日志大小和使用率检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "数据库日志大小和使用率检查正常",
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
        // fields["total_log_size"] //string
        // fields["log_space_usage"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)