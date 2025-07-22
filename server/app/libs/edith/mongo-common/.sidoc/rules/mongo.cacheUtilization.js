;(function (input) {
    var results = []
    var result = {
        desc: "缓存使用率",
        effect: "系统性能降低或者崩溃",
        solution: "增加服务器上可用的内存，优化查询",
        level: "正常",
        id: "mongo.cacheUtilization",
        name: "缓存使用率",
        mixraw: [],
        raw: 0,
        actual: "",
        expected: "缓存使用率小于百分之80",
        category: "",
        family: "conf"
    }

    if (!input) {
        result.actual = "查询结果为空"
        return {results: [result]}
    }
    try {
        raw = $.copy(input)
        var current_bytes_in_wiredTiger_cache = raw.wiredTiger.cache["bytes currently in the cache"]
        var configured_bytes_wiredTiger_cache = raw.wiredTiger.cache["maximum bytes configured"]
        var wiretiger_cacheUsedPercent = (current_bytes_in_wiredTiger_cache / configured_bytes_wiredTiger_cache) * 100;
        real_wiretiger_cacheUsedPercent = parseFloat(wiretiger_cacheUsedPercent.toFixed(4))
        // $.print("===============",real_wiretiger_cacheUsedPercent)
        result.raw = real_wiretiger_cacheUsedPercent
        result.actual = real_wiretiger_cacheUsedPercent
        if (real_wiretiger_cacheUsedPercent > 0.95) {
            raw.level == "高风险"
        } else if (real_wiretiger_cacheUsedPercent > 0.8) {
            raw.level == "中风险"
        }
    } catch (err) {
        $.print(err.message)
        result.level = "低风险"
        result.actual = "原始数据异常"
        result.solution = ""
    }
    results.push(result)
    return {results: results}

})(input)
