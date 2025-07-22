; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "sqlserver.ag_information_and_status_check",
        name: "AG信息及状态检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "AG信息及状态检查正常",
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

        // fields["GroupName"] //string
        // fields["Replica"] //string
        // fields["Role"] //string
        // fields["health_check_timeout_ms"] //string
        // fields["failure_condition_level"] //string
        // fields["AvailabilityMode"] //string
        // fields["primary_recovery_health_desc"] //string
        // fields["secondary_recovery_health_desc"] //string
        // fields["FailoverMode"] //string
        // fields["recovery_health_desc"] //string
        // fields["synchronization_health_desc"] //string
        // fields["SeedingMode"] //string
        // fields["EndpointURL"] //string
        // fields["Listener"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)