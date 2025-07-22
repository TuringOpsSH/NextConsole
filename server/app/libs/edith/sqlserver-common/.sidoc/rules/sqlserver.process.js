; (function (input) {
    var results = []
    var result = {
        desc: "检查当前连接数是否正常",
        effect: "确保SQL Server的连接数不会超过其最大限制",
        solution: "增加SQL Server的最大连接数限制或优化查询以减少连接数",
        level: "正常",
        id: "sqlserver.process",
        name: "当前连接数检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "当前连接数检查正常",
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

        // fields["process_count"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)