; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "sqlserver.ag_property_replicas",
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

        // fields["replica_id"] //string
        // fields["group_id"] //string
        // fields["replica_metadata_id"] //string
        // fields["replica_server_name"] //string
        // fields["owner_sid"] //string
        // fields["endpoint_url"] //string
        // fields["availability_mode"] //string
        // fields["availability_mode_desc"] //string
        // fields["failover_mode"] //string
        // fields["failover_mode_desc"] //string
        // fields["session_timeout"] //string
        // fields["primary_role_allow_connections"] //string
        // fields["primary_role_allow_connections_desc"] //string
        // fields["secondary_role_allow_connections"] //string
        // fields["secondary_role_allow_connections_desc"] //string
        // fields["create_date"] //string
        // fields["modify_date"] //string
        // fields["backup_priority"] //string
        // fields["read_only_routing_url"] //string
        // fields["seeding_mode"] //string
        // fields["seeding_mode_desc"] //string
        // fields["read_write_routing_url"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)