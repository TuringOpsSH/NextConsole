; (function (input) {
    var okResult = {
        desc: "CPU负载正常",
        level: "正常",
        name: "CPU负载检查",
        id: "linux.cpuLoad",
        category: "基本配置检查",
        actual:"",
        expected:""
    }

    var errResult = {
        desc: "CPU负载异常",
        load1: "",
        load5: "",
        load15: "",
        datetime: "",
        effect: "CPU负载过高，可能影响业务",
        solution: "查看各应用CPU占用情况",
        level: "高风险",
        id: "linux.cpuLoad",
        name: "CPU负载检查",
        category: "基本配置检查",
        actual:"",
        expected:""
    }

    if (input == "") {
        return { results: [errResult] }
    }

    if (input["metric"].load1 >= 2.0) {
        datetime = input["datetime"]
        errResult.name = "CPU负载过高"
        errResult.load1 = "1分钟内CPU负载过高" + input["load1"]
        errResult.actual = input["metric"].load1
        errResult.expected = "cpu load < 2"
        return { results: [errResult] }
    }
    else if (input["metric"].load5 >= 2.0) {
        datetime = input["datetime"]
        errResult.name = "CPU负载过高"
        errResult.load5 = "5分钟内CPU负载过高" + input["load5"]
        errResult.actual = input["metric"].load5
        errResult.expected = "cpu load < 2"
        return { results: [errResult] }
    }
    else if (input["metric"].load15 >= 2.0) {
        datetime = input["datetime"]
        errResult.name = "CPU负载过高"
        errResult.load15 = "15分钟内CPU负载过高" + input["load15"]
        errResult.actual = input["metric"].load15
        errResult.expected = "cpu load < 2"
        return { results: [errResult] }
    } else {
        return { results: [] }
    }

})(input)