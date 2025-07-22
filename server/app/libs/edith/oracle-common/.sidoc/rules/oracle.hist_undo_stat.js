; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "oracle.hist_undo_stat",
        name: "Hist Undo 使用情况检查",
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

        // fields["end_time"] //string
        // fields["active_size_mb"] //int
        // fields["unexpired_size_mb"] //int
        // fields["total_size_mb"] //int
        fields["end_time"] = fields["end_time"].substr(0, 4) + "-"
            + fields["end_time"].substr(4, 2) + "-"
            + fields["end_time"].substr(6, 2) + " "
            + fields["end_time"].substr(9, 2) + ":00:00"


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)
