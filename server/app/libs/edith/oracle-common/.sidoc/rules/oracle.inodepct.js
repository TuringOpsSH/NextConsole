; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "可能影响文件系统IO",
        solution: "检查对应各目录 Inode 使用情况, 删除无用文件",
        level: "正常",
        id: "oracle.inodepct",
        name: "Inode 使用率检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "Inode 使用率低于 70%",
        category: "基本配置检查",
        family: "status"
    }

    if (!input) {
        return { results: [result] }
    }

    if (result.family == "status") {
        raw = input[0]["metric"].split("\n")
    } else {
        raw = input
    }

    if (!raw) {
        return { results: [result] }
    }

    for (i = 0; i < raw.length; i++) {
        mixlevel = "正常"
        fields = {}

        // Check fields, reset mixlevel and result.level here:
        fields["Mounted"] = raw[i].split(",")[0]
        fields["Filesystem"] = raw[i].split(",")[1]
        fields["Used"] = raw[i].split(",")[2]
        if (fields["Used"].replace("%", "") >= 90) {
            mixlevel = "高风险"
            result.level = "高风险"
            result.actual += fields["Mounted"] + " Inode 使用率超过 90%, " + "当前为" + fields["Used"] + "; "
        } else if (fields["Used"].replace("%", "") >= 70) {
            mixlevel = "中风险"
            if (result.level != "高风险") {
                result.level = "中风险"
            }
            result.actual += fields["Mounted"] + " Inode 使用率超过 70%, " + "当前为" + fields["Used"] + "; "
        }

        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)
