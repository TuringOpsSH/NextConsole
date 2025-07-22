; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "数据库可能存在异常",
        solution: "检查集群状态",
        level: "正常",
        id: "oracle.crsctlstat",
        name: "集群状态检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "无 OFFLINE 或 UNKNOWN 状态",
        category: "集群状态",
        family: "status"
    }

    if (!input) {
        result.actual = "未发现集群信息"
        return { results: [result] }
    }

    try {
        raw = input[0]["metric"].split("\n")
    } catch (err) {
        raw = input.split("\n")
    }


    if (!raw) {
        result.actual = "未发现集群信息"
        return { results: [result] }
    }


    try {
        var name = ""
        for (i = 0; i < raw.length; i++) {
            mixlevel = ""
            fields = {}

            fields["detail"] = raw[i]
            if (raw[i].match(/ora\./g) || raw[i].match(/---/g) || raw[i].match("details") || raw[i].match("Resources") || raw[i].match("command-not-found")) {
                fields["mixlevel"] = ""
                if (raw[i].match(/ora\./g)) {
                    name = raw[i].toString()
                }
            } else {
                if (name == "ora.gsd") {
                    fields["mixlevel"] = "正常"
                } else if (raw[i].match("OFFLINE")) {
                    if (raw[i].match("ONLINE") || raw[i].match("UNKNOWN")) {
                        fields["mixlevel"] = "中风险"
                        result.actual += name + "存在 OFFLINE 且节点状态不一致; "
                        result.level = "中风险"
                    } else {
                        fields["mixlevel"] = "正常"
                    }
                } else if (raw[i].match("UNKNOWN")) {
                    if (raw[i].match("ONLINE")) {
                        fields["mixlevel"] = "中风险"
                        result.actual += name + "存在 UNKNOWN 且节点状态不一致; "
                        result.level = "中风险"
                    } else {
                        fields["mixlevel"] = "正常"
                    }
                } else {
                    fields["mixlevel"] = "正常"
                }
            }

            result.mixraw.push(fields)
        }
    } catch (err) {
        $.print(err.message)
    }

    results.push(result)
    return { results: results }

})(input)
