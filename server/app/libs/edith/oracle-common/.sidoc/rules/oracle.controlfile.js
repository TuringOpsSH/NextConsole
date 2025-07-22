; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "控制文件用于记录数据库状态和物理结构等重要信息, 单个控制文件损坏将影响数据库正常启动和使用",
        solution: "增加控制文件",
        level: "正常",
        id: "oracle.controlfile",
        name: "控制文件是否镜像检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "控制文件镜像",
        category: "数据文件",
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

        // fields["name"] //string
        // fields["mirrored"] //string
        if (fields["mirrored"] =="NO") {
            mixlevel = "中风险"
            result.level = "中风险"
            result.actual = "控制文件未镜像"
        } else {
            mixlevel = "正常"
        }

        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }
    
    results.push(result)
    return { results: results }

})(input)
