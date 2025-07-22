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
        solution: "检查并重新编译失效对象",
        level: "正常",
        id: "oracle.invalidobj12c",
        name: "失效对象检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "不存在失效对象",
        category: "系统对象检查",
        family: "conf"
    }
    
    if (!input) {
        result.actual = "未发现失效对象"
        return { results: [result] }
    }

    if (result.family == "status"){
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        result.actual = "未发现失效对象"
        return { results: [result] }
    }

    var reg = new RegExp('\\$', "g")
    for (i = 0; i < raw.length; i++) {
        result.actual = "发现失效对象"
        result.level = "中风险"
        mixlevel = "中风险"
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["name"] //string
        fields["name"] = fields["name"].replace(reg, "\\\$") 
        // fields["owner"] //string
        // fields["object_name"] //string
        // fields["object_type"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }
    
    results.push(result)
    return { results: results }

})(input, params)
