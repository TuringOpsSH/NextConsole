; (function (input) {
    var okResult = {
        desc: "CPU使用率正常",
        level: "正常",
        metric: "",
        datetime: "",
        name: "CPU使用率检查",
        id: "linux.cpuUsedPercent",
        category: "capacity",
        actual:"",
        expected:""


    }

    var errResult = {
        desc: "CPU使用率过高",
        effect: "可能影响业务",
        solution: "排查各应用使用CPU情况",
        metric: "",
        datetime: "",
        level: "高风险",
        id: "linux.cpuUsedPercent",
        name: "CPU使用率检查",
        category: "capacity",
        actual:"",
        expected:""
    }


    if (input["metric"] > 75.0) {
        errResult.desc = "CPU使用率过高"
        errResult.metric = (Math.round(input["metric"] * 100) / 100)
        errResult.datetime = input["datetime"]
        errResult.actual = input["metric"].toString()
        errResult.expected = "CPU使用率过高 < 75"
        return { results: [errResult] }
    } else {
        okResult.metric = (Math.round(input["metric"] * 100) / 100)
        okResult.datetime = input["datetime"]
        errResult.actual = input["metric"].toString()
        errResult.expected = "CPU使用率过高 < 75"
        return { results: [okResult] }
    }


})(input)