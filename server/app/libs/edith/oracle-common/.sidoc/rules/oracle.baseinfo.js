; (function (input, params) {
    try {
        if (Number(params[3].Value) >= 12) {
            return
        }
    } catch { }

    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "根据告警内容分别处理",
        level: "正常",
        id: "oracle.baseinfo",
        name: "数据库基本配置检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "基本配置符合最佳实践",
        category: "基本配置检查",
        family: "conf"
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
        mixlevel = ""
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["parameter"] //string
        // fields["value"] //string
        if (fields["parameter"] == "Archiving Enabled") {
            if (fields["value"] != "ARCHIVELOG") {
                mixlevel = "中风险"; if (result.level != "高风险") { result.level = "中风险"; }
                result.actual += "Archiving Enabled预期为ARCHIVELOG即开启归档, 实际为" + fields["value"] + "; "
            } else {
                mixlevel = "正常"
            }
        }

        else if (fields["parameter"] == "Using SPFILE") {
            if (fields["value"] != "YES") {
                mixlevel = "高风险"; result.level = "高风险"
                result.actual += "Using SPFILE预期为YES(使用spfile), 实际为" + fields["value"] + "; "
            } else {
                mixlevel = "正常"
            }
        }

        else if (fields["parameter"] == "Redo logs being multiplexed") {
            if (fields["value"] != "YES") {
                mixlevel = "中风险"; if (result.level != "高风险") { result.level = "中风险"; }
                result.actual += "Redo logs being multiplexed预期为YES(Redo 日志组成员镜像), 实际为" + fields["value"] + "; "
            } else {
                mixlevel = "正常"
            }
        }

        else if (fields["parameter"] == "Redo logs the same size") {
            if (fields["value"] != "YES") {
                mixlevel = "中风险"; if (result.level != "高风险") { result.level = "中风险"; }
                result.actual += "Redo logs the same size预期为YES(Redo 日志大小一致), 实际为" + fields["value"] + "; "
            } else {
                mixlevel = "正常"
            }
        }

        else if (fields["parameter"] == "Number of Control Files") {
            if (fields["value"] == "1") {
                mixlevel = "中风险"; if (result.level != "高风险") { result.level = "中风险"; }
                result.actual += "Number of Control Files预期为!=1(控制文件镜像), 实际为" + fields["value"] + "; "
            } else {
                mixlevel = "正常"
            }
        }

        else if (fields["parameter"] == "Min Redo Log Size(MB)") {
            minredo = Number(fields["value"])
        }
        else if (fields["parameter"] == "SGA Granul Size(MB)") {
            sgags = Number(fields["value"])
        }

        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    if (sgags > minredo) {
        result.mixraw.push({
            parameter: "SGA Granul Size(MB) > Min Redo Log Size(MB)",
            value: "YES",
            mixlevel: "高风险"
        })
        result.actual += "SGA Granul Size(MB) > Min Redo Log Size(MB)预期为NO(小于 sga granule size), 实际为YES" + "; "
    } else {
        result.mixraw.push({
            parameter: "SGA Granul Size(MB) > Min Redo Log Size(MB)",
            value: "NO",
            mixlevel: "正常"
        })
    }

    results.push(result)
    return { results: results }

})(input, params)
