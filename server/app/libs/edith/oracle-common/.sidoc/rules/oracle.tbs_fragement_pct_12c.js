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
        solution: "关注表空间使用，择机进行碎片整理",
        level: "正常",
        id: "oracle.tbs_fragement_pct_12c",
        name: "表空间碎片检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "FSFI > 35",
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

        // fields["name"] //string
        fields["name"] = fields["name"].replace(reg, "\\\$")
        // fields["tablespace_name"] //string
        fields["tablespace_name"] = fields["tablespace_name"].replace(reg, "\\\$")
        // fields["xblocks"] //string

        if (Number(fields["xblocks"]) <= 35) {
            mixlevel = "中风险"
            result.actual = "表空间碎片比例较高, FSFI <= 35"
            result.level = "中风险"
            result.desc = "FSFI 的最大可能值为100, 值越小说明碎片越严重"
        }

        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input, params)
