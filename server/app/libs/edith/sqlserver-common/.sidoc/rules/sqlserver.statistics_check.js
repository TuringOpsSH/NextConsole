; (function (input) {
    var results = []
    var result = {
        desc: "检查SQL Server数据库文件增长类型是否正常",
        effect: "如果文件增长类型不正常, 可能会导致数据库性能下降, 甚至崩溃",
        solution: "检查数据库文件增长类型设置是否合理, 建议使用固定大小增长, 避免自动增长",
        level: "正常",
        id: "sqlserver.statistics_check",
        name: "文件增长类型检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "文件增长类型检查正常",
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
        // fields["inspection_results"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)