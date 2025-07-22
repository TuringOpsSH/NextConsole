; (function (input) {
    var results = []
    var result = {
        desc: "检查SQL Server的版本是否符合要求",
        effect: "如果SQL Server的版本不符合要求, 可能会导致应用程序无法正常工作",
        solution: "请升级SQL Server的版本到符合要求的版本",
        level: "正常",
        id: "sqlserver.sql_version",
        name: "SQLServer的版本检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "SQLServer的版本检查正常",
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

        // fields["sql_version"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)