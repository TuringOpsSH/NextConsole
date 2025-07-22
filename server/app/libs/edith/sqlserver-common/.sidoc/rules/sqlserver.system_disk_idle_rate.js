; (function (input) {
    var results = []
    var result = {
        desc: "检查Windows系统磁盘空闲率是否正常",
        effect: "如果Windows系统磁盘空闲率不正常, 可能会导致系统运行缓慢或崩溃",
        solution: "请检查系统磁盘空间使用情况, 释放不必要的文件或程序, 或者考虑升级硬盘容量",
        level: "正常",
        id: "sqlserver.system_disk_idle_rate",
        name: "Windows系统磁盘空闲率检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "Windows系统磁盘空闲率检查正常",
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
            $.print("system_disk_idle_rate", raw)
            return { results: [result] }
        }
    }

    for (i = 0; i < raw.length; i++) {
        mixlevel = "正常"
        fields = {}
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["dname"] //string
        // fields["free_mb"] //string
        // fields["free_gb"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)