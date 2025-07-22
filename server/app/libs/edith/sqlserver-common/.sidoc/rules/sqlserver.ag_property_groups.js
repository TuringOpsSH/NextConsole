; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "sqlserver.ag_property_groups",
        name: "AG属性检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "AG属性检查正常",
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

        // fields["group_id"] //string
        // fields["name"] //string
        // fields["resource_id"] //string
        // fields["resource_group_id"] //string
        // fields["failure_condition_level"] //string
        // fields["health_check_timeout"] //string
        // fields["automated_backup_preference"] //string
        // fields["automated_backup_preference_desc"] //string
        // fields["version"] //string
        // fields["basic_features"] //string
        // fields["dtc_support"] //string
        // fields["db_failover"] //string
        // fields["is_distributed"] //string
        // fields["cluster_type"] //string
        // fields["cluster_type_desc"] //string
        // fields["required_synchronized_secondaries_to_commit"] //string
        // fields["sequence_number"] //string
        // fields["is_contained"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)