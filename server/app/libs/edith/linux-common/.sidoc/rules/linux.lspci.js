; (function (input) {
    var results = {
        desc: "PCI配置信息展示",
        effect: "无",
        solution: "无",
        level: "正常",
        id: "linux.lspci",
        name: "PCI配置信息展示",
        raw: [],
        actual: "",
        expected: "PCI配置正常",
        category: "系统配置检查",
    }

    for (i = 0; i < input.length; i++) {
        if (input[i].match("Ethernet controller") || input[i].match("SCSI controller") || input[i].match("fabric")) {
            results.raw.push(input[i])
        }
    }

    return { results: [results] }

})(input)
