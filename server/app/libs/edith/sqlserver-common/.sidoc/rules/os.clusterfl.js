; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "os.clusterfl",
        name: "集群参数检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "",
        category: "集群参数检查",
        family: "log"
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
        if (input[0]['metric'].match('Get-Cluster')) {
            return { results: [result] }
        }

        raw = {}
        tmpraw = input[0]['metric'].split("\r\n")
        for (i = 0; i < tmpraw.length; i++) {
            if (tmpraw[i].match(':')) {
                arr = tmpraw[i].split(':')
                raw[arr[0].trim()] = arr[1].trim()
            }
        }
        result.raw = $.copy(raw)

    } catch (err) {
        $.print(err.message)
        return { results: [result] }
    }

    for (var key in raw) {
        mixlevel = "正常"
        fields = {}
        fields["name"] = key
        fields["value"] = raw[key]
        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)