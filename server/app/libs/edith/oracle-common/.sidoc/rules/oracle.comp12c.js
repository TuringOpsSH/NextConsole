; (function (input, params) {
    try {
        if (Number(params[3].Value) < 12) {
            return
        }
    } catch { }

    var results = []
    var result = {
        desc: "",
        effect: "可能影响数据库使用",
        solution: "检查组件状态并修复",
        level: "正常",
        id: "oracle.comp12c",
        name: "数据库组件状态检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "数据库组件状态正常",
        category: "数据库组件及参数设置",
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

    var reg = new RegExp('\\$', "g")
    for (i = 0; i < raw.length; i++) {
        mixlevel = ""
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["name"] //string
        fields["name"] = fields["name"].replace(reg, "\\\$")
        // fields["comp_id"] //string
        // fields["comp_name"] //string
        // fields["version"] //string
        // fields["status"] //string
        // fields["modified"] //string
        if (fields["status"] != "VALID" && fields["status"] != "OPTION OFF") { //TODO 原检查中无OPTION OFF
            mixlevel = "高风险"
            result.level = "高风险"
            result.actual += "; "+fields["comp_name"]+"组件状态异常"
        } else {
            mixlevel = "正常"
        }

        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }
    
    results.push(result)
    return { results: results }

})(input, params)
