; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "无",
        solution: "无",
        level: "正常",
        id: "oracle.db_time_per_second",
        name: "每秒DB Time检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "",
        category: "系统运行状态",
        family: "status"
    }

    if (!input) {
        return { results: [result] }
    }

    if (result.family == "status") {
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        return { results: [result] }
    }

    for (i = 0; i < raw.length; i++) {
        mixlevel = ""
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["end_interval_time"] //string
        // fields["value"] //string
        fields["end_interval_time"] = fields["end_interval_time"].substr(0, 4) + "-"
            + fields["end_interval_time"].substr(4, 2) + "-"
            + fields["end_interval_time"].substr(6, 2) + " "
            + fields["end_interval_time"].substr(9, 2) + ":00:00"

        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)
