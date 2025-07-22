; (function (input) {
    results = []
    result = {
        desc: "",
        id: "linux.netused",
        mixraw: [],
        raw: [],
        actual: "",
        effect: "",
        solution: "",
        level: "正常",
        name: "网络使用率检查",
        expected: "网络使用率小于 80%",
        category: "系统容量检查",
        family: "status"
    }

    try {
        raw = input[0]["metric"]
        //$.print(raw)
        for (i = 0; i < raw.length; i++) {
            mixlevel = "正常"
            fields = raw[i]

            if (Number(fields["used"].replace(/%/g, "")) >= 80) {
                mixlevel = "中风险"
                result.actual += fields["net"] + "使用率为" + fields["used"] + "; "
                result.level = "中风险"
            }

            fields["mixlevel"] = mixlevel
            result.mixraw.push(fields)
        }
    } catch (err) {
        $.print(err.message)
        result.level = "低风险"
        result.actual = "原始数据异常"
    }
    
    //$.print(result)
    results.push(result)
    return { results: results }
})(input)
