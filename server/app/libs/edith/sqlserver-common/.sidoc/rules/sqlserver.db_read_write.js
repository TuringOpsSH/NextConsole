; (function (input) {
    var results = []
    var result = {
        desc: "检查数据库读写比是否正常",
        effect: "如果数据库读写比不正常, 可能会导致数据库性能下降, 影响应用程序的响应时间。",
        solution: "优化数据库读写操作, 例如使用索引、减少不必要的查询等。",
        level: "正常",
        id: "sqlserver.db_read_write",
        name: "数据库读写比检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "数据库读写比检查正常",
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
        // fields["number_of_readings"] //string
        // fields["write_times"] //string
        // fields["reading_proportion"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)