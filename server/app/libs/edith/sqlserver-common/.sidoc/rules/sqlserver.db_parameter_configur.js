; (function (input) {
    var results = []
    var result = {
        desc: "检查数据库参数配置是否正常",
        effect: "确保数据库参数配置符合SQL Server的最佳实践",
        solution: "根据SQL Server的最佳实践, 调整数据库参数配置",
        level: "正常",
        id: "sqlserver.db_parameter_configur",
        name: "数据库参数配置检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "数据库参数配置检查正常",
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

        // fields["parameter_name"] //string
        // fields["parameter_value"] //string
        // fields["parameter_description"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)