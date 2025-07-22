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
        solution: "进一步检查资源使用",
        level: "正常",
        id: "oracle.resourcelimit12c",
        name: "资源使用检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "使用比例小于80%",
        category: "数据文件",
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
        // fields["resource_name"] //string
        // fields["current_utilization"] //string
        // fields["max_utilization"] //string
        // fields["initial_allocation"] //string
        // fields["limit_value"] //string
        // fields["yesno"] //string
        if (fields["yesno"] != "NO") {
            result.desc += fields["resource_name"] + "异常; "
            result.level = "中风险"
            mixlevel = "中风险"

        } else {
            result.level = "正常"
            mixlevel = "正常"
        }

        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }
    
    results.push(result)
    return { results: results }

})(input, params)
