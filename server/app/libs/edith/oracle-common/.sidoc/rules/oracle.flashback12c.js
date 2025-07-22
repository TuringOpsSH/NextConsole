; (function (input, params) {
    try {
        if (Number(params[3].Value) < 12) {
            return
        }
    } catch { }

    var results = []
    var result = {
        desc: "",
        effect: "闪回空间总使用率过高时可能导致数据库异常",
        solution: "关注空间使用，及时清理扩容",
        level: "正常",
        id: "oracle.flashback12c",
        name: "闪回区空间使用率检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "闪回空间总使用率不超过75%",
        category: "系统存储空间使用",
        family: "status"
    }
    
    if (!input) {
        result.actual = "未使用闪回区"
        return { results: [result] }
    }

    if (result.family == "status"){
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        result.actual = "未使用闪回区"
        return { results: [result] }
    }
    
    var reg = new RegExp('\\$', "g")
    for (i = 0; i < raw.length; i++) {
        mixlevel = ""
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["name"] //string
        fields["name"] = fields["name"].replace(reg, "\\\$")
        // fields["file_type"] //string
        // fields["percent_space_used"] //string
        // fields["percent_space_reclaimable"] //string
        // fields["number_of_files"] //string

        if (Number(fields["percent_space_used"]) > 75) {
            result.actual = "闪回空间总使用率过高"
            mixlevel = "高风险"
            result.level = "高风险"
        } else {
            mixlevel = "正常"
        }


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }
    
    results.push(result)
    return { results: results }

})(input, params)
