;(function (input) {
    var results = []
    var result = {
        desc: "windows检查默认共享文件夹情况",
        effect: "可能影响业务",
        solution: "",
        level: "正常",
        id: "win.defaultSharedFolder",
        name: "windows检查默认共享文件夹情况",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "",
        category: "基本配置检查",
        family: "conf"
    }
    try {
        raw = input
        result.raw=raw
    } catch (err) {
        $.print(err.message)
        result.level = "低风险"
        result.actual = "原始数据异常"
    }
    results.push(result)
    return {results: results}
})(input)