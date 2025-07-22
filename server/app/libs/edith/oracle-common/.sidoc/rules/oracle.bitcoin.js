; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "及时清理",
        level: "正常",
        id: "oracle.bitcoin",
        name: "Bit 币勒索病毒检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "未发现勒索病毒",
        category: "系统安全及审计",
        family: "status"
    }

    if (!input) {
        result.actual = result.expected
        return { results: [result] }
    }

    if (result.family == "status") {
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        result.actual = result.expected
        return { results: [result] }
    }

    for (i = 0; i < raw.length; i++) {
        result.actual = "未发现勒索病毒"
        mixlevel = "高风险"
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["owner"] //string
        // fields["object_name"] //string
        // fields["object_type"] //string
        // fields["created"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)
