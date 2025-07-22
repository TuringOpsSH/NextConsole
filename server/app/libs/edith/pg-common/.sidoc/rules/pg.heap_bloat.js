;(function (input) {
    var results = []
    var result = {
        desc: "Autovacuum堆膨胀",
        effect: "",
        solution: "",
        level: "正常",
        id: "heap_bloat",
        name: "Autovacuum堆膨胀检查",
        mixraw: [],
        raw: {},
        actual: "",
        expected: "",
        category: "",
        family: "conf"
    }

    if (!input) {
        result.actual = "查询结果为空"
        return {results: [result]}
    }
    try {
        raw = $.copy(input)
        var entries = Object.entries(raw["heap_bloat"])
        var res = []
        for (var i = 0; i < entries.length; i++) {
            if (entries[i].length == 2) {
                var obj = {}
                obj = $.copy(entries[i][1])

                obj["real_size_bytes"]=(obj["real_size_bytes"]/1024).toFixed(2)
                obj["extra_size_bytes"]=(obj["extra_size_bytes"]/1024).toFixed(2)
                obj["bloat_ratio_factor"]=obj["bloat_ratio_factor"].toFixed(2)
                obj["bloat_ratio_percent"]=obj["bloat_ratio_percent"].toFixed(2)
                res.push(obj)
            }
        }
        res = OrderByNum(res)
        raw["heap_bloat"] = res

        raw["heap_bloat_total"]["real_size_bytes_sum"]=(raw["heap_bloat_total"]["real_size_bytes_sum"]/1024/1024).toFixed(2)
        raw["heap_bloat_total"]["real_size_bytes_sum"]=(raw["heap_bloat_total"]["bloat_size_bytes_sum"]/1024).toFixed(2)
        raw["heap_bloat_total"]["bloat_ratio_factor_avg"]=(raw["heap_bloat_total"]["bloat_ratio_factor_avg"]).toFixed(2)
        raw["heap_bloat_total"]["bloat_ratio_percent_avg"]=(raw["heap_bloat_total"]["bloat_ratio_percent_avg"]).toFixed(2)
        raw["heap_bloat_total"]["live_data_size_bytes_sum"]=(raw["heap_bloat_total"]["live_data_size_bytes_sum"]).toFixed(2)

        result.raw = raw
    } catch (err) {
        $.print(err.message)
        result.level = "低风险"
        result.actual = "原始数据异常"
        result.solution = ""
    }
    results.push(result)
    return {results: results}
})(input)
