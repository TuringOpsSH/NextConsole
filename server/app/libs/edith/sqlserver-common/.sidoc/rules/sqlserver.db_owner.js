; (function (input) {
    var results = []
    var result = {
        desc: "检查数据库所有者是否使用拥有sysadmin角色的用户",
        effect: "防止数据库所有者权限不足, 导致无法进行必要的操作",
        solution: "数据库所有者最好使用拥有sysadmin角色的用户",
        level: "正常",
        id: "sqlserver.db_owner",
        name: "数据库所有者检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "数据库所有者检查正常",
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
        // fields["owner"] //string

        // WIN-G88R2JKFBF0\Administrator
        // sa

        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)