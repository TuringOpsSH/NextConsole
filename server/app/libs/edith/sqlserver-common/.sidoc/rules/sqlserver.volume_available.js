; (function (input) {
    var results = []
    var result = {
        desc: "检查磁盘剩余空间是否过低",
        effect: "当磁盘剩余空间过低时, 可能会导致系统运行缓慢或崩溃",
        solution: "及时清理磁盘空间, 或者增加磁盘容量",
        level: "正常",
        id: "sqlserver.volume_available",
        name: "磁盘剩余空间检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "磁盘剩余空间检查正常",
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

        // fields["drive_letter"] //string
        // fields["file_system"] //string
        // fields["total_size"] //string
        // fields["available_size"] //string
        // fields["disk_usage_rate"] //string
        if (fields["disk_usage_rate"].replace("%", "") > 70) {
            mixlevel = "中风险"
            result.level = "中风险"
            result.actual += fields["drive_letter"] + "使用率为" + fields["disk_usage_rate"] + ";"
        }

        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)