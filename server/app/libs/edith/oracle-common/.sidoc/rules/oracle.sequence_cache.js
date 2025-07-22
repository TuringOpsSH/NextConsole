; (function (input, params) {
    try {
        if (Number(params[3].Value) >= 12) {
            return
        }
    } catch { }

    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "检查序列使用状况并调整序列缓存及最大值设置",
        level: "正常",
        id: "oracle.sequence_cache",
        name: "缓存数量小于500序列检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "CACHE_SIZE > 500",
        category: "系统对象检查",
        family: "status"
    }
    
    if (!input) {
        result.actual = "未发现序列使用信息"
        return { results: [result] }
    }

    if (result.family == "status") {
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        result.actual = "未发现序列使用信息"
        return { results: [result] }
    }

    for (i = 0; i < raw.length; i++) {
        result.level = "中风险"
        mixlevel = "中风险"
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["sequence_owner"] //string
        // fields["sequence_name"] //string
        // fields["cache_size"] //string
        // fields["order_flag"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }
    
    results.push(result)
    return { results: results }

})(input, params)
