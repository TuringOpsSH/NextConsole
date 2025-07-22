; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "检查统计信息收集任务运行状况",
        level: "正常",
        id: "oracle.stats_job_running",
        name: "统计信息收集任务运行状况检查",
        mixraw: [],
        raw: [],
        actual: "不存在非 SUCCEEDED 的记录",
        expected: "检查统计信息收集任务运行状况正常",
        category: "系统运行状态",
        family: "status"
    }

    if (!input) {
        result.actual = "未发现统计信息收集任务运行信息"
        result.level = "高风险"
        return { results: [result] }
    }

    if (result.family == "status") {
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        result.actual = "未发现统计信息收集任务运行信息"
        result.level = "高风险"
        return { results: [result] }
    }

    for (i = 0; i < raw.length; i++) {
        mixlevel = ""
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["job_start_time"] //string
        // fields["job_status"] //string
        // fields["JOB_DURATION"] //string
        if (fields["job_status"] != "SUCCEEDED") {
            mixlevel = "高风险"
            result.level = "高风险"
            result.actual = "存在非 SUCCEEDED 的记录, 详情请查看原始数据"
        } 


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)