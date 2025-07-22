; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "oracle.topevent10g",
        name: "TOP Event 检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "",
        category: "系统运行状态",
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

        // fields["starttime"] //string
        // fields["endtime"] //string
        // fields["event"] //string
        // fields["waits"] //string
        // fields["time"] //string
        // fields["avgwait"] //string
        // fields["pctdbtime"] //string
        // fields["waitclfass"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }
    
    results.push(result)
    return { results: results }

})(input)
