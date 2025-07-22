; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "检查启动状态为Stopped的服务, 是否发生异常",
        level: "正常",
        id: "sqlserver.db_service_check",
        name: "数据库服务检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "数据库服务检查正常",
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

        // fields["service_name"] //string
        // fields["activate_the_account"] //string
        // fields["start_mode"] //string
        // fields["startup_status"] //string
        if (fields["startup_status"] == "Stopped") {
            mixlevel = "高风险"
            result.level = "高风险"
            result.actual = fields["service_name"] + "状态为" + fields["startup_status"] + ";"
        }

        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)