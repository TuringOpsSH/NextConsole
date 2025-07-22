;(function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "",
        level: "正常",
        id: "hostInfo",
        name: "主机基本信息",
        mixraw: [],
        raw: {
            hostname: "",
            uptime: 0,
            bootTime: 0,
            procs: 0,
            os: "",
            platform: "",
            platformFamily: "",
            platformVersion: "",
            kernelVersion: "",
            kernelArch: "",
            virtualizationSystem: "",
            virtualizationRole: "",
            hostId: ""
        },
        actual: "",
        expected: "",
        category: "",
        family: "conf"
    }

    if (!input) {
        return {results: [result]}
    }

    if (result.family == "status") {
        raw = input[0]["metric"]
    } else {
        raw = input
    }
    if (!raw) {
        return {results: [result]}
    }
    result.raw.hostname = raw.hostname
    result.raw.uptime = raw.uptime
    result.raw.bootTime = raw.bootTime
    result.raw.procs = raw.procs
    result.raw.os = raw.os
    result.raw.platform = raw.platform
    result.raw.platformFamily = raw.platformFamily
    result.raw.platformVersion = raw.platformVersion
    result.raw.kernelVersion = raw.kernelVersion
    result.raw.kernelArch = raw.kernelArch
    result.raw.virtualizationSystem = raw.virtualizationSystem
    result.raw.virtualizationRole= raw.virtualizationRole
    result.raw.hostId = raw.hostId
    results.push(result)
    return {results: results}
})(input)
