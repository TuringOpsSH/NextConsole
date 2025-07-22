; (function (input) {
    var okResult = {
        desc: "文件系统空间充足",
        level: "正常",
        name: "文件系统使用率",
        id: "linux.diskUsage",
        category: "capacity",
        actual: "",
        expected: ""
    }

    var errResult = {
        desc: "文件系统空间不足",
        effect: "可能影响业务",
        solution: "查看文件系统占用情况，排查问题或扩容",
        fstype: "fstype",
        path: "path",
        diskUsedPercent: "",
        level: "高风险",
        id: "linux.diskUsage",
        name: "文件系统使用率",
        category: "capacity",
        actual: "",
        expected: ""
    }
    if (input == "") {
        return { results: [errResult] }
    }

    if (input["usedPercent"] >= 85 && input["fstype"] != "isofs") {
        errResult.fstype = input["fstype"]
        errResult.path = input["path"]
        errResult.diskUsedPercent = input["usedPercent"].toFixed(2).toString() + "%"
        errResult.actual = "路径为" + input["path"] + "的文件系统使用率为: " + input["usedPercent"].toFixed(2).toString() + "%"
        errResult.expected = "磁盘使用率 < 85%"
        return { results: [errResult] }
    } else {
        errResult.actual = input["usedPercent"].toFixed(2).toString() + "%"
        errResult.expected = "磁盘使用率 < 85%"
        return { results: [] }
    }

})(input)
