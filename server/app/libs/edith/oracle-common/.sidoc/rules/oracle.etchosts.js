; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "oracle.etchosts",
        name: "主机文件配置检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "",
        category: "巡检总结和建议",
        family: "conf"
    }
    
    if (!input) {
        return { results: [result] }
    }

    if (result.family == "status"){
        raw = input[0]["metric"]
    } else {
        raw = input.split("\n")
    }

    if (!raw) {
        return { results: [result] }
    }

    for (i = 0; i < raw.length; i++) {
        mixlevel = ""
        fields = {}
        // Check fields, reset mixlevel and result.level here:
        fields["IP"] = raw[i].split("=")[0].trim()
        fields["names"] = raw[i].split("=")[1].trim()
        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }
    
    results.push(result)
    return { results: results }

})(input)
