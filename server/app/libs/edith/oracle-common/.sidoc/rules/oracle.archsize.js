; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "oracle.archsize",
        name: "归档日志日生成量检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "归档日志日生成量正常",
        category: "系统备份",
        family: "status"
    }
    
    if (!input) {
        result.actual = "未发现归档日志生成信息"
        return { results: [result] }
    }

    if (result.family == "status"){
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        result.actual = "未发现归档日志生成信息"
        return { results: [result] }
    }

    for (i = 0; i < raw.length; i++) {
        mixlevel = ""
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["first_time"] //string
        // fields["size"] //string
        fields["first_time"] = fields["first_time"].substr(0, 4) + "-"
            + fields["first_time"].substr(4, 2) + "-"
            + fields["first_time"].substr(6, 2) + " "
            + "00:00:00"

        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }
    
    results.push(result)
    return { results: results }

})(input)
