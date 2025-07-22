; (function (input) {
    var results = []
    var result = {
        desc: "检查没有主键的表",
        effect: "检查数据库中是否存在没有主键的表",
        solution: "为没有主键的表添加主键",
        level: "正常",
        id: "sqlserver.tables_without_primary_keys",
        name: "没有主键的表检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "没有主键的表检查正常",
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

    if (raw.length != 0) {
        if (typeof raw[0] === 'string') {
            $.print("tables_without_primary_keys", raw)
            return { results: [result] }
        }
    }

    for (i = 0; i < raw.length; i++) {
        mixlevel = "正常"
        fields = {}
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["table_catalog"] //string
        // fields["table_schema"] //string
        // fields["table_name"] //string

        mixlevel = "中风险"
        result.level = "中风险"
        result.actual = "发现没有主键的表"

        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)