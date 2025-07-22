; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "建议保留PDB状态保留信息(此检查仅适用于11g以后版本)",
        level: "正常",
        id: "oracle.pdbsavedstate",
        name: "PDB 状态保留检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "pdbsavedstate 正常(此检查仅适用于11g以后版本)",
        category: "数据库组件及参数设置",
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

        // fields["con_name"] //string
        // fields["instance_name"] //string
        // fields["state"] //string
        // fields["restricted"] //string
        if (fields["state"] != "OPEN") {
            mixlevel = "中风险"
            result.level = "中风险"
        } else {
            mixlevel = "正常"
        }


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)

