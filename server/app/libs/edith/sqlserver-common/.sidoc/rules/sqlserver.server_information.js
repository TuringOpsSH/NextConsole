; (function (input) {
    var results = []
    var result = {
        desc: "检查SQL Server服务器信息是否正常",
        effect: "如果服务器信息不正常, 可能会影响应用程序的性能和稳定性",
        solution: "检查服务器信息是否正确配置, 例如内存、CPU、磁盘空间等",
        level: "正常",
        id: "sqlserver.server_information",
        name: "服务器信息检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "服务器信息检查正常",
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

        // fields["id"] //string
        // fields["name"] //string
        // fields["value"] //string
        fields["value"] = fields["value"].replace(reg, "\\\\")

        // if (fields["name"] == ){

        // }


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)