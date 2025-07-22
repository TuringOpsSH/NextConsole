; (function (input) {
    var results = []
    var result = {
        desc: "检查SQL Server物理内存大小是否正常",
        effect: "如果物理内存大小不正常, 可能会导致SQL Server性能下降",
        solution: "增加物理内存或优化SQL Server配置",
        level: "正常",
        id: "sqlserver.physical_memory",
        name: "物理内存大小检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "物理内存大小检查正常",
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

        // fields["physical_memory"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)