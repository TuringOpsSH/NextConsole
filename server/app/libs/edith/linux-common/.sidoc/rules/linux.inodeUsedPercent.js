; (function (input) {
    results = []
    result = {
        desc: "",
        id: "linux.inodeUsedPercent",
        mixraw: [],
        raw: [],
        actual: "",
        effect: "可能影响文件系统 IO",
        solution: "检查对应各目录 Inode 使用情况，删除无用文件",
        level: "正常",
        name: "Inode 使用率检查",
        expected: "使用率小于 80%",
        category: "系统容量检查",
        family: "status"
    }

    try {
        raw = input[0]["metric"]
        for (i = 0; i < raw.length; i++) {
            mixlevel = "正常"
            fields = raw[i]

            if (Number(fields["IUse%"].replace(/%/g, "")) >= 80) {
                mixlevel = "高风险"
                result.actual += fields["Mounted on"] + "Inode 使用率为" + fields["IUse%"] + "; "
                result.level = "高风险"
            }

            fields["IUse_PCT"] = fields["IUse%"]
            fields["Mounted"] = fields["Mounted on"]
            fields["mixlevel"] = mixlevel
            result.mixraw.push(fields)
        }
    } catch (err) {
        $.print(err.message)
        result.level = "低风险"
        result.actual = "原始数据异常"
    }

    results.push(result)
    return { results: results }
})(input)