; (function (input) {
    var results = []
    var result = {
        desc: "检查SQL Server的补丁版本是否符合要求",
        effect: "确保SQL Server的补丁版本是最新的, 以提高安全性和性能",
        solution: "安装最新的SQL Server补丁",
        level: "正常",
        id: "sqlserver.patch_version",
        name: "SQLServer的补丁检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "SQLServer的补丁检查正常",
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

        // fields["database_patch"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)