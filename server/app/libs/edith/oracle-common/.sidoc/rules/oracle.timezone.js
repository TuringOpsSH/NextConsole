; (function (input) {
    var results = []
    var result = {
        desc: "数据库时区设置检查",
        effect: "无",
        solution: "调整数据库时区设置",
        level: "正常",
        id: "oracle.timezone",
        name: "数据库时区设置检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "+08:00",
        category: "数据库组件及参数设置",
        family: "conf"
    }
    
    if (!input) {
        return { results: [result] }
    }

    if (result.family == "status"){
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

        // fields["db_time_zone"] //string
        // fields["dbtimezone"] //string
        if (fields["db_time_zone"] == "DB_time_zone") {
            //if (fields["dbtimezone"] !='+08:00' && fields["dbtimezone"] != '+00:00') {
            if (fields["dbtimezone"] !='+08:00') {
                mixlevel = "中风险"
                result.level = "中风险"
                result.actual += fields["dbtimezone"]
            } else {
                mixlevel = "正常"
            }
        }

        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }
    
    results.push(result)
    return { results: results }

})(input)

