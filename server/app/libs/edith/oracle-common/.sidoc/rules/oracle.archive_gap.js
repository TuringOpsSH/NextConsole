; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "导致 ADG 无效",
        solution: "检查归档传输及日志应用状况, 联系 DBA 处理",
        level: "正常",
        id: "oracle.archive_gap",
        name: "DG 归档缺失检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "无 DG 归档缺失",
        category: "系统备份",
        family: "status"
    }
    
    if (!input) {
        result.actual = "未发现相关记录"
        return { results: [result] }
    }

    if (result.family == "status"){
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        result.actual = "未发现相关记录"
        return { results: [result] }
    }

    for (i = 0; i < raw.length; i++) {
        mixlevel = "高风险"
        result.level = "高风险"
        result.actual = "发现日志间隙"
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["instance"] //string
        // fields["high_thread"] //string
        // fields["low_lsq"] //string
        // fields["high_hsq"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }
    
    results.push(result)
    return { results: results }

})(input)
