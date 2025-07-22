; (function (input) {
    var results = []
    var result = {
        desc: "检查数据库中所有schema为dbo的视图是否有效",
        effect: "发现无效视图",
        solution: "只检查schema是dbo的视图, 无效视图以实际为主",
        level: "正常",
        id: "sqlserver.invalid_view",
        name: "无效视图检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "无效视图检查正常",
        category: "",
        family: "any"
    }

    // 非空且元素是字符串认定为执行遇到异常
    try {
        if (Array.isArray(input) && input.length > 0) {
            var allStrings = input.every(function (item) {
                return typeof item === 'string';
            });
            if (allStrings) {
                return { results: [result] };
            }
        }
    } catch (error) {
        return { results: [result] }
    }
    
    try {
        raw = input
        result.raw = $.copy(input)
    } catch (err) {
        $.print(err.message)
        return { results: [result] }
    }
    
    if(!raw){
        return { results: [result] }
    }

    for (i = 0; i < raw.length; i++) {
        mixlevel = "正常"
        fields = {}
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["database_name"] //string
        // fields["view_name"] //string

        mixlevel = "中风险"
        result.level = "中风险"
        result.actual += fields["database_name"] + "发现无效视图" + fields["view_name"] + ";"

        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)