;(function (input) {
    var results = []
    var result = {
        desc: "windows检查任务计划执行用户",
        effect: "可能影响业务",
        solution: "",
        level: "正常",
        id: "win.whoExecutesTaskPlan",
        name: "windows检查任务计划执行用户情况",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "",
        category: "基本配置检查",
        family: "conf"
    }
    try {
        raw = input
        for (let i = 0; i < raw.length; i++) {
            var res = {}
            res["TaskName"] = raw[i]["TaskName"]
            usersArr = raw[i]["Users"]
            var users = ""
            for (let i = 0; i < usersArr.length; i++) {
                users += usersArr[i] + ";"
            }
            res["Users"] = users.trim()
            result.raw.push(res)
        }
    } catch (err) {
        $.print(err.message)
        result.level = "低风险"
        result.actual = "原始数据异常"
    }
    results.push(result)
    return {results: results}
})(input)