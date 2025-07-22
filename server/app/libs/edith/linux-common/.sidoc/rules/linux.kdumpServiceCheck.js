; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "启用 Kdump 服务",
        level: "正常",
        id: "linux.kdumpCheck",
        name: "Kdump 服务检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "启用 Kdump 服务",
        category: "系统服务检查",
        family: "status"
    }

    try {
        raw = input[0]

        mixlevel = "正常"
        fields = $.copy(raw)

        if (fields["metric"].match("not-installed") || fields["metric"].match("disabled") || fields["metric"].match("dead")) {
            mixlevel = "中风险"
            result.actual += "Kdump 服务状态为" + fields["metric"]
            result.level = "中风险"
        } else {
            result.actual += "Kdump 服务状态为" + fields["metric"]
        }

        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)


    } catch (err) {
        $.print(err.message)
        result.level = "低风险"
        result.actual = "原始数据异常"
    }

    //$.print(result)
    results.push(result)
    return { results: results }

})(input)