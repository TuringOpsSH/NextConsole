; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "需要深入分析",
        level: "正常",
        id: "oracle.scnhealthcheck",
        name: "SCN 明细检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "SCN 检查正常",
        category: "系统安全及审计",
        family: "conf"
    }
    
    if (!input) {
        result.actual = "未发现SCN 明细检查数据"
        return { results: [result] }
    }

    if (result.family == "status"){
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        result.actual = "未发现SCN 明细检查数据"
        return { results: [result] }
    }

    for (i = 0; i < raw.length; i++) {
        mixlevel = ""
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["key"] //string
        // fields["value"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }
    
    results.push(result)
    return { results: results }

})(input)
