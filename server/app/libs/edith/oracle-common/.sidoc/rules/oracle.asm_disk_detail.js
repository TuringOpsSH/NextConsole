; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "oracle.asm_disk_detail",
        name: "ASM 磁盘明细信息检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "",
        category: "系统存储空间使用",
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

        // fields["group_number"] //string
        // fields["diskgroupname"] //string
        // fields["namedisk"] //string
        // fields["path"] //string
        // fields["state"] //string
        // fields["total_mb"] //string
        // fields["os_mb"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }
    
    results.push(result)
    return { results: results }

})(input)
