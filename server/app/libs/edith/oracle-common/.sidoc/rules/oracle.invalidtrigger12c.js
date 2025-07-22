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
        solution: "检查并重新编译失效触发器",
        level: "正常",
        id: "oracle.invalidtrigger12c",
        name: "失效触发器检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "不存在失效触发器",
        category: "系统对象检查",
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
        result.actual = "发现失效触发器"
        result.level = "中风险"
        mixlevel = "中风险"
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["name"] //string
        fields["name"] = fields["name"].replace(reg, "\\\$")
        // fields["owner"] //string
        // fields["trigger_name"] //string
        fields["trigger_name"] = fields["trigger_name"].replace(reg, "\\\$")
        // fields["trigger_type"] //string
        // fields["status"] //string
        // fields["table_owner_table_name"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }
    
    results.push(result)
    return { results: results }

})(input, params)
