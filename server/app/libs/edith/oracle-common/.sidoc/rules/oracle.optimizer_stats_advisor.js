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
        solution: "检查统计信息收集任务运行状况",
        level: "正常",
        id: "oracle.optimizer_stats_advisor",
        name: "优化器统计顾问记录失效天数检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "",
        category: "系统运行状态",
        family: "conf"
    }
    
    if (!input) {
        result.desc = "未发现相关记录" 
        result.actual = "未发现相关记录"
        result.level = "中风险"
        return { results: [result] }
    }

    if (result.family == "status"){
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        result.desc = "未发现相关记录" 
        result.actual = "未发现相关记录"
        result.level = "中风险"
        return { results: [result] }
    }

    for (i = 0; i < raw.length; i++) {
        mixlevel = "正常"
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["parameter_name"] //string
        // fields["parameter_value"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }
    
    results.push(result)
    return { results: results }

})(input, params)
