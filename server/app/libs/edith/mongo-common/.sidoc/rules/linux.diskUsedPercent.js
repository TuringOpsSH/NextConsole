; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "可能影响业务",
        solution: "查看文件系统占用情况，排查问题或扩容",
        level: "正常",
        id: "linux.diskUsedPercent",
        name: "文件系统使用率检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "文件系统使用率低于 70%",
        category: "基本配置检查",
        family: "conf"
    }

    try {
        raw = input
        // $.print(raw)
        for (i = 0; i < raw.length; i++) {
            mixlevel = "正常"
            fields = $.copy(raw[i])

            // Check fields, reset mixlevel and result.level here:
            if (raw[i]["fstype"] != "tmpfs" && raw[i]["fstype"] != "sysfs" && raw[i]["fstype"] != "proc" && raw[i]["fstype"] != "cgroupfs" && raw[i]["fstype"] != "isofs") {
                fields["path"] = raw[i]["path"]
                fields["fstype"] = raw[i]["fstype"]
                fields["total"] = $.byte2mb(raw[i]["total"])
                fields["free"] = $.byte2mb(raw[i]["free"])
                fields["used"] = $.byte2mb(raw[i]["used"])
                fields["usedPercent"] = raw[i]["usedPercent"].toFixed(2).toString() + "%"
                if (raw[i]["usedPercent"] >= 90) {
                    mixlevel = "高风险"
                    result.level = "高风险"
                    result.actual += fields["path"] + "使用率超过 90%, " + "当前为" + fields["usedPercent"] + "(剩余" + fields["free"] + "MB);"

                } else if (raw[i]["usedPercent"] >= 70) {
                    mixlevel = "中风险"
                    if (result.level != "高风险") {
                        result.level = "中风险"
                    }
                    result.actual += fields["path"] + "使用率超过 70%, " + "当前为" + fields["usedPercent"] + "(剩余" + fields["free"] + "MB);"
                }

                fields["mixlevel"] = mixlevel
                result.mixraw.push(fields)
            }

        }
    } catch (err) {
        $.print(err.message)
        result.level = "低风险"
        result.actual = "原始数据异常"
    }

    // $.print(result)
    results.push(result)
    return { results: results }

})(input)
