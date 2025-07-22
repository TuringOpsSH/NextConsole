; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "oracle.physic_read_per_second",
        name: "每秒物理读检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "每秒物理读正常",
        category: "系统运行状态",
        family: "conf"
    }
    
    if (!input) {
        return { results: [result] }
    }

    if (result.family == "status"){
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
        // fields["snap_id"] //string
        fields["end_interval_time"] = fields["end_interval_time"].substr(0, 4) + "-"
            + fields["end_interval_time"].substr(4, 2) + "-"
            + fields["end_interval_time"].substr(6, 2) + " "
            + fields["end_interval_time"].substr(9, 2) + ":"
            + fields["end_interval_time"].substr(11, 2) + ":00"

        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }
    
    results.push(result)
    return { results: results }

})(input)
