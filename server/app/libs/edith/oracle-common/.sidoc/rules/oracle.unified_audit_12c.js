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
        id: "oracle.unified_audit_12c",
        name: "统一审计设置检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "统一审计设置正常",
        category: "系统安全及审计",
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
        // fields["parameter"] //string
        // fields["value"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }
    
    results.push(result)
    return { results: results }

})(input, params)
