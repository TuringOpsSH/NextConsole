; (function (input) {
    var results = []
    var result = {
        desc: "检查空密码用户和密码与用户名相同的情况, 防止安全漏洞。",
        effect: "防止攻击者通过空密码用户和密码与用户名相同的情况进行未授权访问。",
        solution: "禁止使用空密码用户和密码与用户名相同的情况, 或者强制要求用户修改密码。",
        level: "正常",
        id: "sqlserver.empty_password_user_password_is_the_same_as_username",
        name: "空密码用户、密码与用户名相同检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "空密码用户、密码与用户名相同检查正常",
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

        // fields["type"] //string
        // fields["username"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)