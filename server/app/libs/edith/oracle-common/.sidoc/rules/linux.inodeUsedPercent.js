function copy(obj){
    var objCopy = {};
    for(var key in obj){
        objCopy[key] = obj[key];
    }
    return objCopy;
};

; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "可能影响文件系统IO",
        solution: "检查对应各目录 Inode 使用情况, 删除无用文件",
        level: "正常",
        id: "linux.inodeUsedPercent",
        name: "Inode 使用率检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "Inode 使用率低于 80%",
        category: "基本配置检查",
        family: "status"
    }

    if (!input) {
        return { results: [result] }
    }

    if (result.family == "status") {
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        return { results: [result] }
    }

    for (i = 0; i < raw.length; i++) {
        mixlevel = "正常"
        fields = copy(raw[i])

        // Check fields, reset mixlevel and result.level here:

        fields["Mounted"] = raw[i]["Mounted on"]
        fields["Filesystem"] = raw[i]["Filesystem"]
        fields["Used"] = Number(raw[i]["IUse%"].replace(/%/g, ""))
        if (fields["Used"] >= 90) {
            mixlevel = "高风险"
            result.level = "高风险"
            result.actual += fields["Filesystem"] + " Inode 使用率超过 90%, " + "当前为" + raw[i]["IUse%"] + "; "
        } else if (fields["Used"] >= 70) {
            mixlevel = "中风险"
            if (result.level != "高风险") {
                result.level = "中风险"
            }
            result.actual += fields["Filesystem"] + " Inode 使用率超过 70%, " + "当前为" + raw[i]["IUse%"] + "; "
        }

        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)
