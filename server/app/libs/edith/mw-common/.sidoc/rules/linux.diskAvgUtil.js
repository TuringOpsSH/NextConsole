; (function (input) {
    var okResult = {
        desc: "20秒内磁盘平均利用率正常",
        level: "正常",
        DEV: "",
        name: "磁盘繁忙检查",
        id: "linux.diskAvgUtil",
        category: "基本配置检查",
        actual: "",
        expected: ""
    }

    var errResult = {
        desc: "20秒内磁盘平均利用率>65%",
        effect: "注意排查，利用率过高可能影响业务",
        solution: "查看磁盘I/O情况，排查问题",
        DEV: "",
        level: "高风险",
        id: "linux.diskAvgUtil",
        name: "磁盘繁忙检查",
        category: "基本配置检查",
        actual: "",
        expected: ""
    }
    if (input == "") {
        return { results: [errResult] }
    }
    if (input["%util"] >= 65) {
        errResult.DEV = input["DEV"]
        errResult.actual = input["%util"].toString()
        errResult.expected = "20秒内磁盘平均利用率 < 65%"
        return { results: [errResult] }
    } else {
        okResult.DEV = input["DEV"]
        errResult.actual = input["%util"].toString()
        errResult.expected = "20秒内磁盘平均利用率 < 65%"
        return { results: [okResult] }
    }

})(input)