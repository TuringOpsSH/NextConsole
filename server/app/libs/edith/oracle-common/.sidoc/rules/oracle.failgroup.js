; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "oracle.failgroup",
        name: "磁盘组 failgroup 磁盘数量检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "同一磁盘组各 failgroup 应磁盘数量一致",
        category: "系统存储空间使用",
        family: "status"
    }
    
    if (!input) {
        result.actual = "未发现 failgroup"
        return { results: [result] }
    }

    if (result.family == "status"){
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        result.actual = "未发现 failgroup"
        return { results: [result] }
    }

    for (i = 0; i < raw.length; i++) {
        mixlevel = ""
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["name"] //string
        // fields["type"] //string
        // fields["failgroup"] //string
        // fields["disk_cnt"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }
    
    results.push(result)
    return { results: results }

})(input)
