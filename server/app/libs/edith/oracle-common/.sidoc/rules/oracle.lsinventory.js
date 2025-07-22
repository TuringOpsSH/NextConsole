; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "oracle.lsinventory",
        name: "补丁安装情况检查/lsinventory",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "",
        category: "数据文件",
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
    
    
    //for (i = 0; i < raw.length; i++) {
    //    mixlevel = ""
    //    fields = raw[i]
    //
    //    // Check fields, reset mixlevel and result.level here:
    //
    //    // fields["action_time"] //string
    //    // fields["action"] //string
    //    // fields["namespace"] //string
    //    // fields["version"] //string
    //    // fields["id"] //string
    //    // fields["comments"] //string
    //
    //
    //    fields["mixlevel"] = mixlevel
    //    result.mixraw.push(fields)
    //}
    
    results.push(result)
    return { results: results }

})(input)
