; (function (input, params) {
    try {
        if (Number(params[3].Value) >= 12) {
            return
        }
    } catch { }

    var results = []
    var result = {
        desc: "",
        effect: "影响数据库正常使用",
        solution: "检查并修复数据文件",
        level: "正常",
        id: "oracle.datafile",
        name: "数据文件可用性检查",
        mixraw: [],
        actual: "",
        expected: "数据文件可用",
        category: "数据文件",
        family: "status"
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

        // fields["type"] //string
        // fields["tablespace_name"] //string
        // fields["file_name"] //string
        // fields["size_mb"] //int
        // fields["max_size_mb"] //int
        // fields["autoextensible"] //string
        // fields["status"] //string
        if (fields["status"] != "AVAILABLE" && fields["type"] == "Datafile") {
            mixlevel = "高风险"
            result.level = "高风险"
            result.actual += fields["file_name"] + "异常; "
        } else {
            mixlevel = "正常"
        }

        if (fields["status"] != "AVAILABLE" && fields["status"] != "ONLINE" && fields["type"] == "Tempfile") {
            mixlevel = "高风险"
            result.level = "高风险"
            result.actual += fields["file_name"] + "异常; "
        } else {
            mixlevel = "正常"
        }

        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }
    
    results.push(result)
    return { results: results }

})(input, params)
