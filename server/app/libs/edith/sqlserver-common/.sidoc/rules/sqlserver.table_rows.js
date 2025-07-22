; (function (input) {
    var results = []
    var result = {
        desc: "检查SQL Server表的行数是否正常",
        effect: "确保表的行数符合预期, 避免数据丢失或错误",
        solution: "检查表的行数是否与预期相符, 如果不符合, 则需要进一步排查问题",
        level: "正常",
        id: "sqlserver.table_rows",
        name: "表行数检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "表行数检查正常",
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

    if (raw.length != 0) {
        if (typeof raw[0] === 'string') {
            $.print("table_rows", raw)
            return { results: [result] }
        }
    }

    for (i = 0; i < raw.length; i++) {
        mixlevel = "正常"
        fields = {}
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["database_name"] //string
        // fields["table_schema"] //string
        // fields["table_name"] //string
        // fields["tb_rows"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)