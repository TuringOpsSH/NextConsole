; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "作为调优或问题排查时的参考。大多数情况下，不推荐使用0，具体配置建议请参考 https://learn.microsoft.com/zh-cn/sql/database-engine/configure-windows/configure-the-max-degree-of-parallelism-server-configuration-option?view=sql-server-ver16#recommendations",
        level: "正常",
        id: "sqlserver.db_startup_parameters",
        name: "数据库启动参数检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "数据库启动参数检查正常",
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

        // fields["configuration_id"] //string
        // fields["name"] //string
        // fields["value"] //string
        // fields["minimum"] //string
        // fields["maximum"] //string
        // fields["value_in_use"] //string
        // fields["description"] //string
        // fields["is_dynamic"] //string
        // fields["is_advanced"] //string

        if (fields["name"] == "max degree of parallelism") {
            if (fields["value"] == 0) {
                mixlevel = "中风险"
                result.level = "中风险"
                result.actual += "max degree of parallelism 值为0"
            }
        }

        if (fields["name"] == "max server memory (MB)") {
            if (fields["value"] == 2147483647) {
                mixlevel = "中风险"
                result.level = "中风险"
                result.actual += "max server memory (MB) 值为2147483647，可能未配置"
            }
        }

        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)