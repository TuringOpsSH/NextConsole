; (function (input) {
    var results = []
    var result = {
        desc: "检查Tempdb是否健康",
        effect: "确保Tempdb正常运行, 避免数据库异常",
        solution: "检查Tempdb数据文件数量是否正确, 检查Tempdb日志文件是否正常, 检查Tempdb文件是否自动增长",
        level: "正常",
        id: "sqlserver.tempdb_check",
        name: "Tempdb健康检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "Tempdb健康检查正常",
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

        // fields["number_of_tempdb_data_files"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)