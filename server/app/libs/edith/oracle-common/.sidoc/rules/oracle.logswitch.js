; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "检查联机日志大小设置, 合理降低切换频率",
        level: "正常",
        id: "oracle.logswitch",
        name: "联机日志切换频率检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "一小时联机日志切换不超过20次",
        category: "数据文件",
        family: "status"
    }

    if (!input) {
        result.actual = "未发现日志切换数据"
        return { results: [result] }
    }

    if (result.family == "status") {
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        result.actual = "未发现日志切换数据"
        return { results: [result] }
    }

    for (i = 0; i < raw.length; i++) {
        mixlevel = ""
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["day"] //string
        // fields["h00"] //string
        // fields["h01"] //string
        // fields["h02"] //string
        // fields["h03"] //string
        // fields["h04"] //string
        // fields["h05"] //string
        // fields["h06"] //string
        // fields["h07"] //string
        // fields["h08"] //string
        // fields["h09"] //string
        // fields["h10"] //string
        // fields["h11"] //string
        // fields["h12"] //string
        // fields["h13"] //string
        // fields["h14"] //string
        // fields["h15"] //string
        // fields["h16"] //string
        // fields["h17"] //string
        // fields["h18"] //string
        // fields["h19"] //string
        // fields["h20"] //string
        // fields["h21"] //string
        // fields["h22"] //string
        // fields["h23"] //string
        // fields["total"] //string
        if (Number(fields["h00"]) > 20 ||
            Number(fields["h01"]) > 20 ||
            Number(fields["h02"]) > 20 ||
            Number(fields["h03"]) > 20 ||
            Number(fields["h04"]) > 20 ||
            Number(fields["h05"]) > 20 ||
            Number(fields["h06"]) > 20 ||
            Number(fields["h07"]) > 20 ||
            Number(fields["h08"]) > 20 ||
            Number(fields["h09"]) > 20 ||
            Number(fields["h10"]) > 20 ||
            Number(fields["h11"]) > 20 ||
            Number(fields["h12"]) > 20 ||
            Number(fields["h13"]) > 20 ||
            Number(fields["h14"]) > 20 ||
            Number(fields["h15"]) > 20 ||
            Number(fields["h16"]) > 20 ||
            Number(fields["h17"]) > 20 ||
            Number(fields["h18"]) > 20 ||
            Number(fields["h19"]) > 20 ||
            Number(fields["h20"]) > 20 ||
            Number(fields["h21"]) > 20 ||
            Number(fields["h22"]) > 20 ||
            Number(fields["h23"]) > 20) {
            mixlevel = "中风险"
            result.level = "中风险"
            result.actual = "个别联机日志一小时切换超过20次"
        } else {
            mixlevel = "正常"
        }


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)
