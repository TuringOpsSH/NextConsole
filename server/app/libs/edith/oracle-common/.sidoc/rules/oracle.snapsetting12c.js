; (function (input, params) {
    try {
        if (Number(params[3].Value) < 12) {
            return
        }
    } catch { }

    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "oracle.snapsetting12c",
        name: "AWR 采样设置检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "",
        category: "系统运行状态",
        family: "conf"
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

    var reg = new RegExp('\\$', "g")
    for (i = 0; i < raw.length; i++) {
        mixlevel = ""
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["name"] //string
        fields["name"] = fields["name"].replace(reg, "\\\$")
        // fields["xsnap_interval"] //string
        // fields["xretention"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }
    
    results.push(result)
    return { results: results }

})(input, params)
