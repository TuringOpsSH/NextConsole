; (function (input) {
    results = []
    result = {
        desc: "",
        id: "linux.etcPasswordCheck",
        mixraw: [],
        raw: [],
        actual: "",
        effect: "存在密码泄露风险",
        solution: "设置密码加密",
        level: "正常",
        name: "用户密码检查",
        expected: "设置密码加密",
        category: "安全合规检查",
        family: "conf"
    }

    try {
        raw = input
        // $.print(raw)
        for (i = 0; i < raw.length; i++) {
            mixlevel = "正常"
            fields = raw[i]

            if (fields["password"] != "x") {
                mixlevel = "高风险"
                result.actual += fields["user"] + "用户密码设置异常; "
                result.level = "高风险"
            }

            fields["mixlevel"] = mixlevel
            result.mixraw.push(fields)
        }
    } catch (err) {
        $.print(err.message)
        result.level = "低风险"
        result.actual = "原始数据异常"
    }
    
    // $.print(result)
    results.push(result)
    return { results: results }
})(input)