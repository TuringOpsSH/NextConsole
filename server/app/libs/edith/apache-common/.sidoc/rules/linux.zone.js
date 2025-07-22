; (function (input) {

    if (input['/etc/sysconfig/clock(ZONE)'] != "") {
        actual = input['/etc/sysconfig/clock(ZONE)']
    } else {
        actual = input['timedatectl(Time zone)']
    }

    var okResult = {
        desc: "检查时区是否为 Asia/Shanghai",
        effect: "当系统时区设置与应用运行要求不一致时可能造成应用异常",
        solution: "无特殊要求时一般须设置为 Asia/Shanghai",
        level: "正常",
        id: "linux.zone",
        name: "时区设置检查",
        expected: "Asia/Shanghai",
        category: "health",
        actual: actual
    }

    var errResult = {
        desc: "检查时区是否为 Asia/Shanghai",
        effect: "当系统时区设置与应用运行要求不一致时可能造成应用数据异常",
        solution: "无特殊要求时一般须设置为 Asia/Shanghai",
        expected: "Asia/Shanghai",
        level: "高风险",
        id: "linux.zone",
        name: "时区设置检查",
        category: "health",
        actual: actual
    }

    if (input['/etc/sysconfig/clock(ZONE)'].match("Asia/Shanghai") ||
        input['timedatectl(Time zone)'].match("Asia/Shanghai")) {
        return {
            results: [okResult]
        }
    } else {
        return {
            results: [errResult]
        }
    }

})(input)
