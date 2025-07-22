; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "sqlserver.all_database_file_information",
        name: "所有数据库文件信息检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "所有数据库文件信息检查正常",
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
        // fields["file_id"] //string
        // fields["file_name"] //string
        // fields["file_path"] //string
        fields["file_path"] = fields["file_path"].replace(reg, "\\\\")
        // fields["file_type"] //string
        // fields["file_status"] //string
        // fields["pct_increase"] //string
        // fields["growth"] //string
        // fields["size_mb"] //string
        // fields["avg_read"] //string
        // fields["avg_write"] //string
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