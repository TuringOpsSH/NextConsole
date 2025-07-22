;(function (input) {
    var results = []
    var result = {
        desc: "检查admin是否改名",
        effect: "可能导致系统无法正常运行或增加潜在的安全风险",
        solution: "修改admin名",
        level: "正常",
        id: "win.ifAdminNameChange",
        name: "检查admin是否改名",
        mixraw: [],
        raw: "",
        actual: "",
        expected: "admin改名",
        category: "基本配置检查",
        family: "conf"
    }

    try {
        raw = input
        if (raw.includes("does not change name")) {
            result.level = "中风险"
        } else {
            result.level = "正常"
        }
        result.raw = raw
        result.actual = raw
    } catch (err) {
        $.print(err.message)
        result.level = "低风险"
        result.actual = "原始数据异常"
    }
    results.push(result)
    return {results: results}

})(input)
