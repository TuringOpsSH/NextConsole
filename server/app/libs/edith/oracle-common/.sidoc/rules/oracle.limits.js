; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "oracle.limits",
        name: "资源限制配置检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "符合最佳实践要求",
        category: "基本配置检查",
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
        if (raw[i].match("=")){
            fields["user"] = "-"
            fields["type"] = "-"
            fields["item"] = raw[i].split("=")[0].trim()
            fields["value"] = raw[i].split("=")[1].trim()
            fields["mixlevel"] = ""
        } else {
            fields["user"] = raw[i].split(" ")[0]
            fields["type"] = raw[i].split(" ")[1]
            fields["item"] = raw[i].split(" ")[2]
            fields["value"] = raw[i].split(" ")[3]
            fields["mixlevel"] = ""
        }
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)
