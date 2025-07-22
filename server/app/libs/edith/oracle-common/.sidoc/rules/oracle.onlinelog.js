; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "oracle.onlinelog",
        name: "联机日志检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "",
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

        // fields["thread"] //string
        // fields["group"] //string
        // fields["member"] //string
        // fields["status"] //string
        // fields["sequence"] //string
        // fields["MB"] //string
        // fields["logtype"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }
    
    results.push(result)
    return { results: results }

})(input)
