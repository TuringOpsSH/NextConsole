; (function (input) {
    var results = []
    var result = {
        desc: "SQL Server服务器错误日志检查",
        effect: "错误日志中记录的错误或警告信息可能标示某些未知的系统或软件问题,如果长期未检查,可能会带来故障或数据损坏的风险",
        solution: "定期检查服务器错误日志,发现和解决潜在问题",
        level: "正常",
        id: "sqlserver.server_error_log",
        name: "服务器错误日志检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "无错误日志",
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

    var reg = new RegExp('\\$', "g");
    for (i = 0; i < raw.length; i++) {
        mixlevel = "正常"
        fields = {}
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["logdate"] //string
        // fields["loginfo"] //string
        // fields["count"] //string
        fields["loginfo"] = fields["loginfo"].replace(reg, "\\\$")

        mixlevel = "中风险"
        result.level = "中风险"
        result.actual = "存在错误日志"


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)