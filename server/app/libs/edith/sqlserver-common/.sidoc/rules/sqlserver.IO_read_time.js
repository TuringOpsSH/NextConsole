; (function (input) {
    var results = []
    var result = {
        desc: "检查SQL Server I/O读响应时间是否正常",
        effect: "当I/O读响应时间异常时, 可能会导致SQL Server性能下降",
        solution: "检查磁盘驱动器、数据库名称、文件名、总读取次数和每次读取的平均响应时间是否正常",
        level: "正常",
        id: "sqlserver.IO_read_time",
        name: "I/0读响应时间检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "I/0读响应时间检查正常",
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

        // fields["drive_letter"] //string
        // fields["database_name"] //string
        // fields["file_name"] //string
        // fields["total_number_of_reads"] //string
        // fields["_average_response_time_per_read"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)