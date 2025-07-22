; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "MTU 较大而内存参数 vm.min_free_kbytes 较小时可能会造成网络缓冲区预留的可用空间较少, 从而出现大量丢包导致网络连接问题",
        solution: "需综合考虑 vm.min_free_kbytes 及 MTU 设置情况决定是否修改",
        level: "正常",
        id: "oracle.lo",
        name: "主机文件配置检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "MTU 设置为 16436",
        category: "巡检总结和建议",
        family: "conf"
    }

    if (!input) {
        result.actual = "未发现相关信息"
        return { results: [result] }
    }

    if (result.family == "status") {
        raw = input[0]["metric"]
    } else {
        raw = input.split("\n")
    }

    if (!raw) {
        result.actual = "未发现相关信息"
        return { results: [result] }
    }

    for (i = 0; i < raw.length; i++) {
        fields = {}

        fields["item"] = raw[i].split(":")[0]
        fields["value"] = raw[i].split(":")[1]
        if (fields["item"] == "Current config") {
            if (fields["value"] == "N/A") {
                fields["value"] = "巡检用户没有权限查询 MTU 值"
            } else if (Number(fields["value"]) > 16436) {
                result.desc = "MTU 参数设置过大, 建议设置为 16436"
                result.actual = "MTU 设置为: " + fields["value"]
                result.level = "中风险"
            }
        }

        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)
