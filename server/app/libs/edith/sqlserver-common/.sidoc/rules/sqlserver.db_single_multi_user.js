; (function (input) {
    var results = []
    var result = {
        desc: "检查数据库用户访问设置是否正确配置",
        effect: "确保数据库用户访问设置正确配置, 防止未授权的用户访问数据库",
        solution: "检查数据库用户访问设置是否正确配置, 只授权必要的用户访问数据库",
        level: "正常",
        id: "sqlserver.db_single_multi_user",
        name: "数据库用户访问设置检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "数据库用户访问设置检查正常",
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
        // fields["database_user_access_settings"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)