; (function (input) {
    var results = []
    var result = {
        desc: "检查SQL Server数据库的排序规则是否正确",
        effect: "如果排序规则不正确, 可能会导致查询结果不准确或无法正常查询",
        solution: "请检查数据库的排序规则设置是否正确, 建议使用Windows排序规则",
        level: "正常",
        id: "sqlserver.collation",
        name: "排序规则检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "排序规则检查正常",
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

        // fields["name"] //string
        // fields["desc"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)