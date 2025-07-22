; (function (input) {
    var results = []
    var result = {
        desc: "检查SQL Server最大工作线程数是否正常",
        effect: "如果最大工作线程数不正常, 可能会导致SQL Server性能下降",
        solution: "增加最大工作线程数或优化查询以减少工作线程数",
        level: "正常",
        id: "sqlserver.maxworkers",
        name: "最大工作线程数检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "最大工作线程数检查正常",
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

        // fields["max_workers_count"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)