; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "sqlserver.user_and_process_details",
        name: "用户和进程详情检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "用户和进程详情检查正常",
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

    var reg = new RegExp('\\$', "g")
    for (i = 0; i < raw.length; i++) {
        mixlevel = "正常"
        fields = {}
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["spid"] //string
        // fields["status"] //string
        // fields["loginame"] //string
        fields["loginame"] = fields["loginame"].replace(reg, "\\\$")
        // fields["dbname"] //string
        // fields["cpu"] //string
        // fields["physical_io"] //string
        // fields["login_time"] //string
        // fields["last_batch"] //string
        // fields["hostname"] //string
        // fields["cmd"] //string
        // fields["blocked"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)