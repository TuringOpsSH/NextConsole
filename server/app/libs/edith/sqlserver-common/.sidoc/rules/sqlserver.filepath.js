; (function (input) {
    var results = []
    var result = {
        desc: "检查数据库文件的存放位置是否正确",
        effect: "确保数据库文件存放位置正确, 避免数据丢失或无法访问",
        solution: "检查数据库文件的存放位置是否正确, 如果不正确则修改为正确的位置",
        level: "正常",
        id: "sqlserver.filepath",
        name: "数据库文件的存放位置检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "数据库文件的存放位置检查正常",
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

    var reg = new RegExp('\\\\', "g");
    for (i = 0; i < raw.length; i++) {
        mixlevel = "正常"
        fields = {}
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["database_name"] //string
        // fields["file_name"] //string
        // fields["file_type"] //string
        // fields["storage_location"] //string
        fields["storage_location"] = fields["storage_location"].replace(reg, "\\\\")


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)