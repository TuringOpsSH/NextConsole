; (function (input, params) {
    try {
        if (Number(params[3].Value) < 12) {
            return
        }
    } catch { }

    var results = []
    var result = {
        desc: "",
        effect: "降低数据库性能",
        solution: "检查语句性能并进行相关优化",
        level: "正常",
        id: "oracle.fullscan12c",
        name: "最近7天单次逻辑读大于1000且进行全表扫描的语句检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "未发现满足条件的语句",
        category: "系统运行状态",
        family: "status"
    }

    if (!input) {
        result.actual = result.expected
        return { results: [result] }
    }

    if (result.family == "status") {
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        result.actual = result.expected
        return { results: [result] }
    }

    for (i = 0; i < raw.length; i++) {
        result.actual = "发现满足条件的语句"
        result.level = "中风险"
        mixlevel = "中风险"
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["sql_id"] //string
        // fields["plan_hash_value"] //string
        // fields["total_buffer_gets"] //string
        // fields["total_executions"] //string
        // fields["buffer_get_onetime"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }
    if (result.level == "正常") {
        result.actual = result.expected
    }

    results.push(result)
    return { results: results }

})(input, params)
