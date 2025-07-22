; (function (input) {
    var results = []
    var result = {
        desc: "检查SQL Server的CPU最大并行度是否设置正确",
        effect: "如果CPU最大并行度设置不正确, 可能会导致CPU利用率过高, 影响系统性能",
        solution: "根据服务器的CPU核心数和负载情况, 设置合适的CPU最大并行度值, 建议不要超过CPU核心数的2倍",
        level: "正常",
        id: "sqlserver.max_parallelism_degree",
        name: "CPU最大并行度检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "CPU最大并行度检查正常",
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

        // fields["cpu_maximum_parallelism"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)