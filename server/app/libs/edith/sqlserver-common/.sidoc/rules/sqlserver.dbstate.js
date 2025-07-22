; (function (input) {
    var results = []
    var result = {
        desc: "检查数据库状态是否正常",
        effect: "检查数据库状态是否正常, 如果状态不为ONLINE, 则认为存在高风险",
        solution: "检查数据库状态是否正常, 如果状态不为ONLINE, 则需要进一步排查原因",
        level: "正常",
        id: "sqlserver.dbstate",
        name: "数据库的状态检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "数据库的状态检查正常",
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
        // fields["state"] //string
        if (fields["state"] != "ONLINE") {
            mixlevel = "高风险"
            result.level = "高风险"
            result.actual = fields["database_name"] + "状态为" + fields["state"] + ";"
        }

        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)