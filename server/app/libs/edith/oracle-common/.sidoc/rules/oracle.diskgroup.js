; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "关注磁盘组使用",
        level: "正常",
        id: "oracle.diskgroup",
        name: "磁盘组使用率检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "使用率 < 75%",
        category: "系统存储空间使用",
        family: "status"
    }

    var result_offline = {
        desc: "",
        effect: "",
        solution: "检查修复磁盘组",
        level: "正常",
        id: "oracle.diskgroupoffline",
        name: "磁盘组offline 情况检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "磁盘组无 offline",
        category: "系统存储空间使用",
        family: "status"
    }

    if (!input) {
        return { results: [result, result_offline] }
    }

    if (result.family == "status") {
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        return { results: [result, result_offline] }
    }

    for (i = 0; i < raw.length; i++) {
        mixlevel = ""
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["name"] //string
        // fields["au_size"] //string
        // fields["state"] //string
        // fields["type"] //string
        // fields["total_disk_size_mb"] //string
        // fields["dg_total_mb"] //string
        try {
            fields["dg_total_mb"] = Number(fields["dg_total_mb"]).toFixed(2).toString()
        } catch (err) {
            $.print(err)
        }
        // fields["dg_free_mb"] //string
        try {
            fields["dg_free_mb"] = Number(fields["dg_free_mb"]).toFixed(2).toString()
        } catch (err) {
            $.print(err)
        }
        // fields["dg_used_pct"] //string
        try {
            fields["dg_used_pct"] = Number(fields["dg_used_pct"]).toFixed(2).toString()
        } catch (err) {
            $.print(err)
        }
        // fields["offline_disks"] //string
        // fields["redundancy"] //string

        if (Number(fields["dg_used_pct"]) >= 75) {
            result.actual += fields["name"] + "使用率: " + fields["dg_used_pct"] + "%(剩余" + fields["dg_free_mb"] + "MB);"
            result.level = "高风险"
            mixlevel = "高风险"
        } else {
            mixlevel = "正常"
        }

        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)


    for (i = 0; i < raw.length; i++) {
        mixlevel = ""
        fields = raw[i]

        // Check fields, reset mixlevel and result_offline.level here:

        // fields["name"] //string
        // fields["au_size"] //string
        // fields["state"] //string
        // fields["type"] //string
        // fields["total_disk_size_mb"] //string
        // fields["dg_total_mb"] //string
        // fields["dg_free_mb"] //string
        // fields["dg_used_pct"] //string
        // fields["offline_disks"] //string
        // fields["redundancy"] //string

        if (Number(fields["offline_disks"]) > 0) {
            result_offline.actual += fields["name"] + "存在 offline disk;"
            result_offline.level = "高风险"
            mixlevel = "高风险"
        } else {
            if (mixlevel != "高风险") {
                mixlevel = "正常"
            }
        }


        fields["mixlevel"] = mixlevel
        result_offline.mixraw.push(fields)
    }

    results.push(result_offline)

    return { results: results }

})(input)
