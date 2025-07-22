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
        solution: "检查相关外键并创建合适的索引",
        level: "正常",
        id: "oracle.foreignkey12c",
        name: "外键无索引检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "不存在外键无索引",
        category: "系统对象检查",
        family: "status"
    }
    
    if (!input) {
        result.actual = "未发现外键无索引"
        return { results: [result] }
    }

    if (result.family == "status"){
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        result.actual = "未发现外键无索引"
        return { results: [result] }
    }
    
    var reg = new RegExp('\\$', "g")
    for (i = 0; i < raw.length; i++) {
        result.actual = "发现外键无索引"
        result.level = "中风险"
        mixlevel = "中风险"
        var fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["name"] //string
        fields["name"] = fields["name"].replace(reg, "\\\$")
        // fields["owner"] //string
        // fields["constraint_name"] //string
        fields["constraint_name"] = fields["constraint_name"].replace(reg, "\\\$")
        // fields["table_name"] //string
        fields["table_name"] = fields["table_name"].replace(reg, "\\\$")
        // fields["column_name"] //string
        // fields["status"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }
    
    results.push(result)
    return { results: results }

})(input, params)
