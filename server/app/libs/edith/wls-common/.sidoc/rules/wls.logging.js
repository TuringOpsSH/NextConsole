; (function (input) {
    var okResult = {
        level: "None",
        id: "wls.logging"
    }

    var errResult = {
        desc: "日志设置为默认值",
        effect: "日志数量过少，会导致无法诊断问题",
        solution: "设置为按照大小轮转，单个文件5M，最多10个文件",
        level: "low",
        id: "wls.logging",
        name: "没有正确的配置日志",
    }

    if (input == "") {
        return { results: [errResult] }
    }
    // log(tojson(input))
    // log(input["rotationType"])

    if (input["rotationType"] != "bySize") {
        errResult.desc = "未按照大小轮转"
        return { results: [errResult] }
    }
    if (input["fileCount"] != "10") {
        errResult.desc = "日志数量不符合标准"
        return { results: [errResult] }
    }

    if (input["fileMinSize"] != "5000") {
        errResult.desc = ""

    }

    if (input["fileMinSize"] != "5000") {
        errResult.desc = "日志数量不符合标准"
        return { results: [errResult] }
    }
    return { results: [] }
})(input)