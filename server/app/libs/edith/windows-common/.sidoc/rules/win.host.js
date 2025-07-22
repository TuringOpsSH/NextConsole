;(function (input) {
    var results = []
    if (input == "") {
        return {results: [results]}
    }

    var result = {
        desc: "主机基本信息检查",
        effect: "可能影响业务",
        solution: "",
        level: "正常",
        id: "win.diskUsedPercent",
        name: "windows主机基本信息检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "windows磁盘分区使用率小于70%",
        category: "基本配置检查",
        family: "conf"
    }


    //系统内核架构检查
    if (input["kernelArch"] != "x86_64") {

        results.push({
            desc: "内核架构:" + input["kernelArch"],
            effect: "可能影响业务",
            solution: "建议使用64位架构",
            level: "中风险",
            id: "win.arch",
            name: "内核架构检查",
            mixraw: [],
            raw: [],
            actual: input["kernelArch"],
            expected: "x86_64",
            category: "系统配置检查",
            family: "conf",
        })
    } else {
        results.push({
            desc: "内核架构:" + input["kernelArch"],
            effect: "可能影响业务",
            solution: "建议使用64位架构",
            level: "正常",
            id: "win.arch",
            name: "内核架构检查",
            mixraw: [],
            raw: [],
            actual: input["kernelArch"],
            expected: "x86_64",
            category: "系统配置检查",
            family: "conf",
        })
    }
    return {results: results}
})(input)