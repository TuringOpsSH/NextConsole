; (function (input, params) {
    try {
        if (Number(params[3].Value) >= 12) {
            return
        }
    } catch { }

    var results = []
    var result = {
        desc: "",
        effect: "可能影响数据库使用",
        solution: "检查组件状态并修复",
        level: "正常",
        id: "oracle.comp",
        name: "comp 检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "数据库组件状态正常",
        category: "数据库组件及参数设置",
        family: "status"
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

        // fields["comp_id"] //string
        // fields["comp_name"] //string
        // fields["version"] //string
        // fields["status"] //string
        // fields["modified"] //string

        if (fields["status"] != "VALID" && fields["status"] != "OPTION OFF") {
			//如果APEX的Level为INVALID的话改成中风险
			if (fields["comp_id"] == "APEX"){
				mixlevel = "中风险"
				result.level = "中风险"
				result.actual += "; "+fields["comp_name"]+"组件状态告警"
			}else{
				mixlevel = "高风险"
				result.level = "高风险"
				result.actual += "; "+fields["comp_name"]+"组件状态异常"
			
			}
        } else {
            mixlevel = "正常"
        }
		
		

        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input, params)

