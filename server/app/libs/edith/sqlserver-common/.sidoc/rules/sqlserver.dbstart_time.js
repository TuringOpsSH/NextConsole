; (function (input) {
    var results = []
    var result = {
        desc: "检查SQL Server数据库上次重启时间是否正常",
        effect: "如果数据库上次重启时间不正常, 可能会影响数据库的性能和稳定性",
        solution: "检查数据库上次重启时间是否符合预期, 如果不符合, 需要进行相应的维护和修复操作",
        level: "正常",
        id: "sqlserver.dbstart_time",
        name: "数据库上次重启时间检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "数据库上次重启时间检查正常",
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

        // fields["sql"] //string
        // fields["last_server_restart_time"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)