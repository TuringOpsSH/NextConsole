; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "集群环境下, 节点间 LMS 进程数量应保持一致",
        level: "正常",
        id: "oracle.lmscount",
        name: "LMS 进程数量检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "集群环境下, 节点间 LMS 进程数量应保持一致",
        category: "集群状态",
        family: "status"
    }
    
    if (!input) {
        result.desc = "未发现相关记录"
        result.actual = "未发现相关记录"
        return { results: [result] }
    }

    if (result.family == "status"){
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        result.actual = "未发现相关记录"
        return { results: [result] }
    }

    for (i = 0; i < raw.length; i++) {
        mixlevel = ""
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["inst_id"] //int
        // fields["count"] //int


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }
    
    results.push(result)
    return { results: results }

})(input)
