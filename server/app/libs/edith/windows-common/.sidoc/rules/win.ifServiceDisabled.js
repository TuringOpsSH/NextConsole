;(function (input) {
    var results = []
    var result = {
        desc: "检查服务是否禁用",
        effect: "可能影响业务",
        solution: "",
        level: "正常",
        id: "win.ifServiceDisabled",
        name: "检查服务是否禁用",
        mixraw: [],
        raw: {},
        actual: "",
        expected: "服务没有被禁用",
        category: "基本配置检查",
        family: "conf"
    }

    try {
        raw = input
        const res = new Map();
        for (const key in input) {
            serve = {}
            serve["name"] = key
            serve["status"] = input[key]
            result.mixraw.push(serve)
            // console.log(`${key}: ${person[key]}`);
        }
    } catch (err) {
        $.print(err.message)
        result.level = "低风险"
        result.actual = "原始数据异常"
    }
    results.push(result)
    return {results: results}

})(input)
