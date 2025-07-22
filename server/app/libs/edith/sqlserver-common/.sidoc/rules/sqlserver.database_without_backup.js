; (function (input) {
    var results = []
    var result = {
        desc: "检查SQL Server数据库是否有备份, 如果没有则报告异常",
        effect: "确保数据库备份的可用性和完整性",
        solution: "为数据库设置备份计划, 定期备份数据库",
        level: "正常",
        id: "sqlserver.database_without_backup",
        name: "无备份的数据库检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "无备份的数据库检查正常",
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

        // fields["database_name__"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)