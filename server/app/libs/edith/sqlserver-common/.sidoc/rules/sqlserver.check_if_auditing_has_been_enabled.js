; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "如果未开启审计，就无法及时发现潜在的安全威胁和攻击行为，从而增加了系统遭受攻击和数据泄露的风险",
        solution: "开启审计",
        level: "正常",
        id: "sqlserver.check_if_auditing_has_been_enabled",
        name: "是否开启审计检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "开启审计",
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
        if (Array.isArray(raw) && raw.length === 0) {
            result.level = "中风险"
            result.actual = "未开启审计"
            return { results: [result] }
        }
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
        // fields["is_state_enabled"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)