; (function (input) {
    var results = []
    var result = {
        desc: "检查数据库文件增长类型是否为MB",
        effect: "防止数据库文件增长类型不为MB导致数据库性能下降",
        solution: "数据库的数据文件和日志文件建议按MB增长, 增长大小建议设置 200MB, 最大文件大小无限制",
        level: "正常",
        id: "sqlserver.file_growth_type",
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
        // fields["file_name"] //string
        // fields["file_type"] //string
        // fields["growth_type"] //string
        if (fields["growth_type"] != "MB") {
            mixlevel = "中风险"
            result.level = "中风险"
            result.actual += fields["database_name"] + "的" + fields["file_name"] + "(" + fields["file_type"] + ")增长类型为" + fields["growth_type"] + ";"
        }

        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)