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
        solution: "无检查并重新编译失效索引",
        level: "正常",
        id: "oracle.invalididx",
        name: "失效索引检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "不存在失效索引",
        category: "系统对象检查",
        family: "status"
    }
    
    if (!input) {
        result.actual = "未发现失效索引"
        return { results: [result] }
    }

    if (result.family == "status"){
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        result.actual = "未发现失效索引"
        return { results: [result] }
    }

    for (i = 0; i < 10; i++) {
        result.actual = "发现失效索引"
        result.level = "中风险"
        mixlevel = "中风险"
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["owner"] //string
        // fields["index_name"] //string
        // fields["index_type"] //string
        // fields["partition_name"] //string
        // fields["status"] //string
        // fields["table_name"] //string
        // fields["tablespace_name"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }
    
    results.push(result)
    return { results: results }

})(input, params)
