; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "oracle.dataguard_status",
        name: "DG 相关日志信息检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "DG 相关日志信息检查正常",
        category: "系统备份",
        family: "status"
    }
    
    if (!input) {
        result.actual = "未发现 DG 相关日志信息"
        return { results: [result] }
    }

    if (result.family == "status"){
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        result.actual = "未发现DG 相关日志信息"
        return { results: [result] }
    }

    for (i = 0; i < raw.length; i++) {
        mixlevel = ""
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["inst_id"] //string
        // fields["timestamp"] //string
        // fields["dest_id"] //string
        // fields["error_code"] //string
        // fields["message"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }
    
    results.push(result)
    return { results: results }

})(input)
