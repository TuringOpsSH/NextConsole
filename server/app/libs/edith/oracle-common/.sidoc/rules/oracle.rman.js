; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "无法基于 rman 还原数据库",
        solution: "检查系统备份",
        level: "正常",
        id: "oracle.rman",
        name: "系统备份(rman)检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "系统备份正常",
        category: "系统备份",
        family: "status"
    }

    if (!input) {
        result.actual = "未发现系统备份"
        result.level = "中风险"
        result.solution = "进行系统备份"
        return { results: [result] }
    }

    if (result.family == "status") {
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        result.actual = "未发现系统备份"
        result.level = "中风险"
        result.solution = "进行系统备份"
        return { results: [result] }
    }
    
    for (i = 0; i < raw.length; i++) {
        mixlevel = ""
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["date"] //string
        // fields["stat"] //string
        if (fields["stat"] != "COMPLETED") {
            result.actual = "系统备份异常"
            result.level = "中风险"
            mixlevel = "中风险"
        } else {
            result.actual = "系统备份正常(最近一次)"
            result.level = "正常" // 使用最后一次的结果作为整体结果
            mixlevel = "正常"
        }


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }
    if (result.level == "正常") {
        result.actual = result.expected
    }

    results.push(result)
    return { results: results }

})(input)
