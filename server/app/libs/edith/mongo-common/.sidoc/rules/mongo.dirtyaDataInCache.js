;(function (input) {
    var results = []
    var result = {
        desc: "缓存中脏数据的比率",
        effect: "写入性能下降,数据丢失或损坏",
        solution: "增加物理内存，调整写入策略",
        level: "正常",
        id: "mongo.dirtyDataInCache",
        name: "缓存中脏数据比率",
        mixraw: [],
        raw: 0,
        actual: "",
        expected: "脏数据比率不应该长时间超过5%,，偶尔超过也没问题。最高不能超过20%",
        category: "",
        family: "conf"
    }

    if (!input) {
        result.actual = "查询结果为空"
        return {results: [result]}
    }
    try {
        raw = $.copy(input)
        var configured_bytes_wiredTiger_cache = raw.wiredTiger.cache["maximum bytes configured"]
        var dirty_bytes_in_cache = raw.wiredTiger.cache["tracked dirty bytes in the cache"];
        var wiretiger_dirtyUsedPercent = (dirty_bytes_in_cache/configured_bytes_wiredTiger_cache)*100;
        real_wiretiger_dirtyUsedPercent =parseFloat(wiretiger_dirtyUsedPercent.toFixed(4))
        // $.print("===============",real_wiretiger_cacheUsedPercent)
        result.raw = real_wiretiger_dirtyUsedPercent
        result.actual = real_wiretiger_dirtyUsedPercent
        if (real_wiretiger_dirtyUsedPercent > 0.2) {
            raw.level == "高风险"
        } else if (real_wiretiger_dirtyUsedPercent > 0.05) {
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
