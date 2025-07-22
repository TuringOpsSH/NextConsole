; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "sqlserver.database_server_disk_io_and_cpu_statistics",
        name: "数据库服务器磁盘IO和CPU统计信息检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "数据库服务器磁盘IO和CPU统计信息检查正常",
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

        // fields["total_read"] //string
        // fields["total_write"] //string
        // fields["total_errors"] //string
        // fields["io_busy"] //string
        // fields["timeticks"] //string
        // fields["io_operation"] //string
        // fields["cpu_busy"] //string
        // fields["cpu_working"] //string
        // fields["cpu_idle"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)