; (function (input) {
    var results = []
    var result = {
        desc: "检查数据库的读写模式是否正常",
        effect: "确保数据库的读写模式正常, 以避免数据丢失或损坏",
        solution: "检查数据库的读写模式设置, 确保其符合业务需求和最佳实践",
        level: "正常",
        id: "sqlserver.db_read_write_model",
        name: "数据库的读写模式检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "数据库的读写模式检查正常",
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
        // fields["database_read_and_write_mode"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)