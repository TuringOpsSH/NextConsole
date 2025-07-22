; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "(此检查仅适用于11g以后版本)",
        level: "正常",
        id: "oracle.pdbstat",
        name: "数据库组件及参数设置检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "系统组件及参数设置符合最佳实践(此检查仅适用于11g以后版本)",
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

    var reg = new RegExp('\\$', "g")
    for (i = 0; i < raw.length; i++) {
        mixlevel = ""
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["con_id"] //string
        // fields["name"] //string        
        // fields["inst_id"] //string
        // fields["open_mode"] //string
        // fields["restricted"] //string
        if (fields["name"] == 'PDB$SEED') {
            if (fields["open_mode"] != "READ ONLY" || fields["restricted"] != "NO") {
                mixlevel = "高风险"
                result.level = "高风险"
                result.desc += fields["name"] + "异常; "
            } else {
                mixlevel = "正常"
            }
        } else {
            if (fields["open_mode"] != "READ WRITE" || fields["restricted"] != "NO") {
                mixlevel = "高风险"
                result.level = "高风险"
                result.desc += fields["name"] + "异常; "
            } else {
                mixlevel = "正常"
            }
        }
        
        fields["name"] = fields["name"].replace(reg, "\\\$")


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    result.actual = result.desc
    results.push(result)
    return { results: results }

})(input)

