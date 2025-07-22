; (function (input) {
    var results = []
    var result = {
        desc: "检查数据库大小和使用率是否正常",
        effect: "如果数据库大小和使用率不正常, 则可能会导致数据库性能下降或崩溃",
        solution: "检查数据库大小和使用率, 如果超过预期值, 则需要优化数据库或增加存储空间",
        level: "正常",
        id: "sqlserver.db_size",
        name: "数据库大小和使用率检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "数据库大小和使用率检查正常",
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

    for (i = 0; i < raw.length; i++) {
        mixlevel = "正常"
        fields = {}
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["database_name"] //string
        // fields["database_total_size"] //string
        // fields["unallocated"] //string
        // fields["space_usage"] //string
        if(Number(fields["db_max_size"]) != -1){
            if (Number(fields["space_usage"].replace('%', '')) >= 90) {
                mixlevel = "高风险"
                result.actual += fields["database_name"] + "使用率大于90%, 当前值为" + fields["space_usage"] + ";"
                result.level = "高风险"
            } else if (Number(fields["space_usage"].replace('%', '')) >= 75) {
                mixlevel = "中风险"
                if (result.level != "高风险") {
                    result.level = "中风险"
                }
                result.actual += fields["database_name"] + "使用率大于75%, 当前值为" + fields["space_usage"] + ";"
            } else {
                mixlevel = "低风险"
            }
        }else {
            mixlevel = "低风险"
        }

        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)