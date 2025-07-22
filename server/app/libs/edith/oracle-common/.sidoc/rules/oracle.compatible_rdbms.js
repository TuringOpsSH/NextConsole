; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "参考文档(Doc ID 1933068.1)，调整的命令语法:alter diskgroup DATA set attribute 'compatible.rdbms'='12.1.0.0.0';",
        level: "正常",
        id: "oracle.compatible_rdbms",
        name: "RDBMS软件的ASM磁盘使用情况检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "使用空间 < 2TB",
        category: "系统存储空间使用",
        family: "status"
    }

    if (!input) {
		result.actual = "RDBMS软件的ASM磁盘使用未超过2TB"
        return { results: [result] }
    }

    if (result.family == "status") {
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
		result.actual = "RDBMS软件的ASM磁盘使用未超过2TB"
        return { results: [result] }
    }

    for (i = 0; i < raw.length; i++) {
        mixlevel = ""
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["diskgroup_name"] //string
        // fields["path"] //string
        // fields["os_mb"] //string
        // fields["total_mb"] //string
        // fields["compatible_asm"] //string
        // fields["compatible_rdbms"] //string

        if (Number(fields["total_mb"]) >= 2000000) {
            result.actual += fields["diskgroup_name"] + "使用: " + fields["total_mb"] + "mb;"
            result.level = "高风险"
            mixlevel = "高风险"
        } else {
            mixlevel = "正常"
        }

        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)
