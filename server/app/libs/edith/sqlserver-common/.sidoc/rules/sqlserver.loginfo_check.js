; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "日志碎片会给数据库带来性能、空间利用率、可靠性和管理方面的隐患",
        solution: "定期执行日志碎片整理,将日志文件碎片合并,重建连续的日志空间。这可以极大地减少碎片带来的风险",
        level: "正常",
        id: "sqlserver.loginfo_check",
        name: "日志碎片检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "日志碎片检查正常",
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
        if (fields["inspection_results"] != "正常") {
            mixlevel = "中风险"
            result.level = "中风险"
            result.actual += fields["database_name"] + " " + fields["inspection_results"] + ";"
        }

        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)