; (function (input) {
    var results = []
    var result = {
        desc: "检查SQL Server实例的排序规则是否符合要求",
        effect: "如果实例的排序规则不符合要求, 可能会导致查询结果不准确或无法正确排序",
        solution: "检查实例的排序规则是否符合要求, 如果不符合, 可以通过修改实例的排序规则来解决问题",
        level: "正常",
        id: "sqlserver.instance_collation",
        name: "实例的排序规则检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "实例的排序规则检查正常",
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

        // fields["sorting_rules_for_instances"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)