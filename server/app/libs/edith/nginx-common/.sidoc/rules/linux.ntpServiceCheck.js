; (function (input) {
    var okResult = {
        desc: "NTP 服务已启动",
        level: "正常",
        datetime: "",
        name: "NTP 服务检查",
        actual: "",
        expected: "启用 NTP 服务",
        id: "linux.ntpCheck",
        category: "health"
    }

    var errResult = {
        desc: "NTP 服务未开启",
        effect: "",
        datetime: "",
        actual: "",
        expected: "启用 NTP 服务",
        solution: "",
        level: "中风险",
        id: "linux.ntpCheck",
        name: "NTP 服务检查",
        category: "health"
    }

    if (input == "") {
        return { results: [errResult] }
    }
    if (input["metric"].match("not-installed") || input["metric"].match("disabled") || input["metric"].match("dead")) {
        errResult.datetime = input["datetime"]
        errResult.actual  = "未启用 NTP 服务"
        return { results: [errResult] }
    } else {
        okResult.actual = "已启用 NTP 服务"
        okResult.datetime = input["datetime"]
        return { results: [okResult] }
    }


})(input)