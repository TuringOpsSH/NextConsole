; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "sqlserver.average_readwrite_blocking_time_per_database_file",
        name: "每个数据库文件的平均读写阻塞时间检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "每个数据库文件的平均读写阻塞时间检查正常",
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

    var reg = new RegExp('\\\\', "g");
    for (i = 0; i < raw.length; i++) {
        mixlevel = "正常"
        fields = {}
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["database_name"] //string
        // fields["avg_read_stall_ms"] //string
        // fields["avg_write_stall_ms"] //string
        // fields["file_size_mb"] //string
        // fields["physical_name"] //string
        fields["physical_name"] = fields["physical_name"].replace(reg, "\\\\")
        // fields["type_desc"] //string
        // fields["io_stall_read_ms"] //string
        // fields["num_of_reads"] //string
        // fields["io_stall_write_ms"] //string
        // fields["num_of_writes"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)