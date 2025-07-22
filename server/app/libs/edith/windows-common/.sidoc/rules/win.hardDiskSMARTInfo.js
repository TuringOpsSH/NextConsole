;(function (input) {
    var results = []
    var result = {
        desc: "查看磁盘驱动器信息是否正常",
        effect: "可能会导致数据丢失、系统崩溃、应用程序无法正常工作等严重后果",
        solution: "备份数据，检查磁盘是否损坏",
        level: "正常",
        id: "win.hardDiskSMARTInfo",
        name: "查看磁盘驱动器信息",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "所有磁盘驱动器状态正常",
        category: "系统运行状态",
        family: "conf"
    }
    try {
        raw = input
        for (i = 0; i < raw.length; i++) {
            mixlevel = "正常"
            fields = $.copy(raw[i])
            if (fields["status"] != "OK") {
                mixlevel = "高风险"
                result.level = "高风险"
                result.actual += fields["caption"] + "磁盘驱动器状态不正常;"
            } else {
                mixlevel = "正常"
            }
            fields["mixlevel"] = mixlevel
            result.mixraw.push(fields)
        }
        if (result.level == "正常") {
            result.actual = "所有磁盘驱动器状态正常"
        }
        result.raw = raw
    } catch (err) {
        $.print(err.message)
        result.level = "低风险"
        result.actual = "原始数据异常"
    }
    results.push(result)
    return {results: results}
})(input)