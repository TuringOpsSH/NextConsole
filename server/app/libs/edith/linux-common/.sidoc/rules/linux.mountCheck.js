; (function (input) {
    results = []
    result = {
        desc: "",
        id: "linux.mountCheck",
        mixraw: [],
        raw: [],
        actual: "",
        effect: "可能影响读写操作",
        solution: "修改文件系统状态为 read-write",
        level: "正常",
        name: "Mount 状态检查",
        expected: "文件系统状态为 read-write (除CD/DVD, /dev/sr0, iso9660, /sys/fs/cgroup下的tmpfs外)",
        category: "系统状态检查",
        family: "status"
    }

    try {
        raw = input
        //$.print(raw)
        for (i = 0; i < raw.length; i++) {
            mixlevel = "正常"
            fields = raw[i]

            if (fields["source"] == "tmpfs" && fields["mountpoint"] == "/sys/fs/cgroup") {
                // pass
            } else if (fields["type"] == "iso9660") {
                // pass
            } else if (!fields["opts"].match("rw") && fields["source"] != "/dev/sr0" && fields["source"] != "/dev/cdrom") {
                mixlevel = "高风险"
                result.actual += fields["source"] + "挂载于" + fields["mountpoint"] + "无rw属性" + "; "
                result.level = "高风险"
            }

            fields["mixlevel"] = mixlevel
            result.mixraw.push(fields)
        }
    } catch (err) {
        $.print(err.message)
        result.level = "低风险"
        result.actual = "原始数据异常"
    }
    //$.print(result)
    results.push(result)
    return { results: results }
})(input)