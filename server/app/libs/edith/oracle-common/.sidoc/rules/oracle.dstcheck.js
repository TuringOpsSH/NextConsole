; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "检查数据库时区文件版本设置",
        level: "正常",
        id: "oracle.dstcheck",
        name: "时区文件版本检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "",
        category: "数据库组件及参数设置",
        family: "conf"
    }
    
    if (!input) {
        result.actual = "未发现 DST 版本检查记录"
        return { results: [result] }
    }

    if (result.family == "status"){
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        result.actual = "未发现 DST 版本检查记录"
        return { results: [result] }
    }

    for (i = 0; i < raw.length; i++) {
        mixlevel = ""
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["db_version"] //string
        // fields["dst_version"] //string
        // fields["regist_version"] //string
        if(fields["dst_version"] != fields["regist_version"]){
            result.actual += "DST 版本不一致;"
            regist.level = "中风险"
            mixlevel = "中风险"
        }

        if(fields["db_version"] == "19.0.0.0.0" && fields["dst_version"] != "32"){
            result.actual += "DST 版本应为32;"
            regist.level = "中风险"
            mixlevel = "中风险"
        }
        
        if(fields["db_version"] == "11.2.0.4.0" && fields["dst_version"] != "14"){
            result.actual += "DST 版本应为14;"
            regist.level = "中风险"
            mixlevel = "中风险"
        }
                
        if(fields["db_version"] == "12.2.0.1.0" && fields["dst_version"] != "28"){
            result.actual += "DST 版本应为28;"
            regist.level = "中风险"
            mixlevel = "中风险"
        }
        
        if(fields["db_version"] == "11.2.0.1.0" && fields["dst_version"] != "11"){
            result.actual += "DST 版本应为11;"
            regist.level = "中风险"
            mixlevel = "中风险"
        }
        
        if(mixlevel == ""){
            mixlevel = "正常"
        }
                
        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }
    
    results.push(result)
    return { results: results }

})(input)

