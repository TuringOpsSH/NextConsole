; (function (input) {
    var results = []
    var result = {
        desc: "检查SQL Server数据库最小内存配置是否符合要求",
        effect: "确保SQL Server数据库最小内存配置符合最佳实践, 避免因内存不足导致数据库性能下降或崩溃",
        solution: "根据SQL Server版本和实际业务需求, 设置合理的数据库最小内存配置",
        level: "正常",
        id: "sqlserver.db_min_memory",
        name: "数据库最小内存配置检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "数据库最小内存配置检查正常",
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
        mixlevel = "-"
        fields = {}
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["database_minimum_memory_configuration"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)