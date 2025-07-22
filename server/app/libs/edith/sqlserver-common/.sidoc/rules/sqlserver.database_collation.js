; (function (input) {
    var results = []
    var result = {
        desc: "检查数据库的排序规则是否符合SQL Server的要求",
        effect: "如果数据库的排序规则不符合SQL Server的要求, 可能会导致查询结果不准确或者无法正常执行",
        solution: "请修改数据库的排序规则, 使其符合SQL Server的要求",
        level: "正常",
        id: "sqlserver.database_collation",
        name: "数据库的排序规则检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "数据库的排序规则检查正常",
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
        // fields["sort_rule_name"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)