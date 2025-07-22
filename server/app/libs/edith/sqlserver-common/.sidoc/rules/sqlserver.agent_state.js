; (function (input) {
    var results = []
    var result = {
        desc: "检查SQL Server代理作业的状态和所有者是否正确",
        effect: "如果代理作业的状态或所有者不正确, 则可能会导致作业失败或未按预期运行",
        solution: "检查代理作业的状态和所有者是否正确, 如果不正确, 则更正",
        level: "正常",
        id: "sqlserver.agent_state",
        name: "作业状态和所有者检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "作业状态和所有者检查正常",
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

        // fields["job_name"] //string
        // fields["job_owner"] //string
        // fields["job_status"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)