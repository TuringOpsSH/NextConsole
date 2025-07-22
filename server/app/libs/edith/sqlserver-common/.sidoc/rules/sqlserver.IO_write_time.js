; (function (input) {
    var results = []
    var result = {
        desc: "检查I/O写响应时间是否正常",
        effect: "如果I/O写响应时间异常, 可能会导致数据库性能下降",
        solution: "检查磁盘、文件和数据库是否正常, 优化磁盘和文件的读写操作",
        level: "正常",
        id: "sqlserver.IO_write_time",
        name: "I/0写响应时间检查#检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "I/0写响应时间检查#检查正常",
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

        // fields["_drive_letter"] //string
        // fields["database_name"] //string
        // fields["file_name"] //string
        // fields["total_number_of_reads"] //string
        // fields["_average_response_time_per_write"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)