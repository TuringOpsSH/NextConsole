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
        solution: "检查序列使用状况并调整序列缓存及最大值设置",
        level: "正常",
        id: "oracle.sequence12c",
        name: "Sequence 使用率检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "使用率小于70%",
        category: "系统对象检查",
        family: "status"
    }
    
    if (!input) {
        result.actual = "未发现异常序列"
        return { results: [result] }
    }

    if (result.family == "status"){
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        result.actual = "未发现异常序列"
        return { results: [result] }
    }

    for (i = 0; i < raw.length; i++) {
        result.actual = "发现异常序列"
        result.level = "中风险"
        mixlevel = "中风险"
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["name"] //string
        // fields["sequence_owner"] //string
        // fields["sequence_name"] //string
        // fields["used_pct"] //string
        // fields["min_value"] //string
        // fields["max_value"] //string
        // fields["increment_by"] //string
        // fields["cycle_flag"] //string
        // fields["order_flag"] //string
        // fields["cache_size"] //string
        // fields["last_number"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }
    
    results.push(result)
    return { results: results }

})(input, params)
