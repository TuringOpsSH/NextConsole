; (function (input, params) {
    try {
        if (Number(params[3].Value) >= 12) {
            return
        }
    } catch { }

    var results = []
    var result = {
        desc: "",
        effect: "可能影响数据库正常使用",
        solution: "关注表空间使用，及时清理扩容",
        level: "正常",
        id: "oracle.tbscheck",
        name: "表空间使用率检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "使用率小于75%",
        category: "系统存储空间使用",
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

        // fields["tablespace_name"] //string
        fields["tablespace_name"] = fields["tablespace_name"].replace(reg, "\\\$")
        // fields["bigfile"] //string
        // fields["count_file"] //string
        // fields["usedpct"] //string
        // fields["xxx"] //string
        // fields["total"] //string
        // fields["used"] //string
        // fields["free"] //string
        // fields["extent_total"] //string
        // fields["max_fragment_mb"] //string
        // fields["fsfi"] //string
        // fields["yesno"] //string

        if (Number(fields["xxx"]) >= 90) {
            mixlevel = "高风险"
            result.actual += fields["tablespace_name"] + "使用率大于90%, 当前值为" + fields["xxx"] + "% (剩余"+ Number(fields["free"]).toFixed(2) +"MB); "
            result.level = "高风险"
        } else if (Number(fields["xxx"]) >= 75) {
            mixlevel = "中风险"
            if (result.level != "高风险") {
                result.level = "中风险"
            }
            result.actual += fields["tablespace_name"] + "使用率大于75%, 当前值为" + fields["xxx"] + "% (剩余"+ Number(fields["free"]).toFixed(2) +"MB); "
        } else {
            mixlevel = "低风险"
        }

        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input, params)
