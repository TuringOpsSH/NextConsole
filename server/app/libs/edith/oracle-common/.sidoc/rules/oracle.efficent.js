; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "oracle.efficent",
        name: "实例运行性能检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "指标值 >= 90%",
        category: "系统运行状态",
        family: "conf"
    }

    if (!input) {
        result.actual = "未发现实例运行性能信息"
        return { results: [result] }
    }

    if (result.family == "status") {
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        result.actual = "未发现实例运行性能信息"
        return { results: [result] }
    }

    for (i = 0; i < raw.length; i++) {
        mixlevel = ""
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["name"] //string
        // fields["value"] //string
        if (fields["name"].match("-") && fields["name"].match(":")) {
            fields["value"] = fields["name"] + " -- " + fields["value"]
            fields["name"] = "观察时间"
            fields["mixlevel"] = ""
        } else {
            if (Number(fields["value"]) < 90) {
                fields["mixlevel"] = "中风险"
                result.level = "中风险"
                result.actual += fields["name"] + "指标过低, 当前为" + fields["value"] + "%;"
            } else {
                fields["mixlevel"] = "低风险"
            }
        }

        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)
