; (function (input) {
    var results = []
    var result = {
        desc: "查看各数据库Bufferpool使用情况检查",
        effect: "检查各数据库Bufferpool使用情况是否正常",
        solution: "根据检查结果进行相应的处理",
        level: "正常",
        id: "sqlserver.view_the_usage_of_bufferpools_in_various_databases",
        name: "查看各数据库Bufferpool使用情况检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "查看各数据库Bufferpool使用情况检查正常",
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

    if (raw.length != 0) {
        if (typeof raw[0] === 'string') {
            $.print("view_the_usage_of_bufferpools_in_various_databases", raw)
            return { results: [result] }
        }
    }

    for (i = 0; i < raw.length; i++) {
        mixlevel = "正常"
        fields = {}
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["buffer_pool_rank"] //string
        // fields["database_name"] //string
        // fields["cachedsize_mb"] //string
        // fields["buffer_pool_percent"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)