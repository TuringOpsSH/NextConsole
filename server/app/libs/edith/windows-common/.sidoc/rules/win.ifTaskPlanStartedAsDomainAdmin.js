;(function (input) {
    var results = []
    var result = {
        desc: "检查任务计划是否已域admin身份启动",
        effect: "可能影响业务",
        solution: "关闭任务计划已经以域管理员身份",
        level: "正常",
        id: "win.ifTaskPlanStartedAsDomainAdmin",
        name: "检查任务计划是否已域admin身份启动",
        mixraw: [],
        raw: "",
        actual: "",
        expected: "关闭任务计划已经以域管理员身份",
        category: "基本配置检查",
        family: "conf"
    }

    try {
        raw = input
        if (raw.includes("user is normal")) {
            result.level="正常"
        }else {
            result.level="中风险"
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
