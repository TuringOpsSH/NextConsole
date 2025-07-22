; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "利用率过高可能影响业务",
        solution: "查看磁盘 I/O 情况",
        level: "正常",
        id: "linux.diskAvgUtil",
        name: "磁盘繁忙检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "20 秒内磁盘平均利用率 < 65%",
        category: "系统容量检查",
        family: "status"
    }

    try {
        raw = input[0]["metric"]["average"]
        // $.print(raw)
        for (i = 0; i < raw.length; i++) {
            mixlevel = "正常"
            fields = $.copy(raw[i])

            if (fields["%util"] >= 65) {
                mixlevel = "高风险"
                result.actual += fields["DEV"] + " 20 秒内磁盘平均利用率 > 65%, " + "当前为" + fields["%util"] + "%; "
                result.level = "高风险"
            }

            fields["utilpct"] = fields["%util"]
            fields["avgqusz"] = fields["avgqu-sz"]
            fields["avgrqsz"] = fields["avgrq-sz"]
            fields["rd_secs"] = fields["rd_sec/s"]
            fields["wr_secs"] = fields["wr_sec/s"]
            fields["mixlevel"] = mixlevel
            result.mixraw.push(fields)
        }

    } catch (err) {
        $.print(err.message)
        result.level = "低风险"
        result.actual = "原始数据异常"
        result.solution = "查看 sar 命令是否安装, 如未安装 sar 命令可忽略此告警"
    }

    //$.print(result)
    results.push(result)
    return { results: results }

})(input)