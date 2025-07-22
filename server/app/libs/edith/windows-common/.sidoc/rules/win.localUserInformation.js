;(function (input) {
    var results = []
    var result = {
        desc: "windows收集本地用户信息",
        effect: "可能影响业务",
        solution: "",
        level: "正常",
        id: "win.localUserInformation",
        name: "windows收集本地用户信息",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "",
        category: "基本配置检查",
        family: "conf"
    }
    try {
        raw = input
        const res = new Map();
        for (let i = 0; i < raw.length; i++) {
            for (const key in raw[i]) {
                serve = {}
                serve["account"] = key
                serve["content"] = raw[i][key]
                result.raw.push(serve)
                // console.log(`${key}: ${person[key]}`);
            }
        }
    } catch (err) {
        $.print(err.message)
        result.level = "低风险"
        result.actual = "原始数据异常"
    }
    results.push(result)
    return {results: results}
})(input)