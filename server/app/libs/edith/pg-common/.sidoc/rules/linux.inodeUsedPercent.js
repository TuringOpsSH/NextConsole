; (function (input) {
    var results = []
    if (Number(input["IUse%"].replace(/%/g, "")) > 80) {
        results.push({
            desc: "inode 使用率是否超过80%，" + input["Mounted on"] + "为：" + input["IUse%"],
            effect: "可能影响文件系统IO",
            solution: "检查对应各目录inode使用情况，删除无用文件",
            level: "高风险",
            id: "linux.inodeUsedPercent",
            name: "inode 使用率（" + input["Mounted on"] + "）",
            category: "capacity",
            actual:Number(input["IUse%"].replace(/%/g, "")),
            expected:"inode 使用率是 < 80%"
        })
    } else {
        results.push({
            desc: "检查inode 使用率是否超过80%，" + input["Mounted on"] + "为：" + input["IUse%"],
            effect: "可能影响文件系统IO",
            solution: "检查对应各目录inode使用情况，删除无用文件",
            level: "正常",
            name: "inode 使用率（" + input["Mounted on"] + "）",
            id: "linux.inodeUsedPercent",
            category: "capacity",
            actual:Number(input["IUse%"].replace(/%/g, "")),
            expected:"检查inode 使用率是 < 80%"
        })
    }

    if (input["Mounted on"] == "/") {

        if (Number(input["IUse%"].replace(/%/g, "")) > 80) {
            var level = "高风险"
        } else {
            var level = "正常"
        }

        results.push({
            desc: "inode 使用率是否超过80%",
            effect: "可能影响文件系统IO",
            solution: "检查对应各目录inode使用情况，删除无用文件",
            level: level,
            id: "linux.inodeUsedPercent.wc",
            name: "inode 使用率（" + input["Mounted on"] + "）",
            category: "capacity",
            actual:Number(input["IUse%"].replace(/%/g, "")),
            expected:"检查inode 使用率是 < 80%"
        })

    }

    return { results: results }


})(input)
