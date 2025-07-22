; (function (input) {
    var results = []
    var result = {
        desc: "检查各个数据库的对象情况, 包括表、视图、存储过程等",
        effect: "发现数据库对象异常情况, 如表缺失、视图无法访问等",
        solution: "根据异常情况进行相应的修复操作, 如创建缺失的表、修复无法访问的视图等",
        level: "正常",
        id: "sqlserver.object_status_of_each_database",
        name: "各个数据库的对象情况检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "各个数据库的对象情况检查正常",
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

    if (!raw) {
        return { results: [result] }
    }

    for (i = 0; i < raw.length; i++) {
        mixlevel = "正常"
        fields = {}
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["database_name"] //string
        // fields["xtype"] //string
        // fields["cnt"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)