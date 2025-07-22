;(function (input) {
    var okResult = {
        startupMode: "",
        datetime: "",
        id: "wls.serverRuntime",
        name: "Server运行状态",
        level: ""
    }

    var errResult = {
        effect: "Server运行状态异常",
        solution: "建议检查Server启动情况",
        startupMode: "",
        datetime: "",
        id: "wls.serverRuntime",
        name: "Server运行状态",
        level: ""
    }
    var level = ""
    if (input[0]["metric"] == "RUNNING") {
        okResult.startupMode = input[0]["metric"]
        okResult.datetime = input[0]["datetime"]
        okResult.level = "low"
        return {results: [okResult]}
    } else {
        if (input[0]["metric"] == "UNKNOWN") {
            level = "mid"
        } else {
            level = "high"
        }
        errResult.startupMode = input[0]["metric"]
        errResult.datetime = input[0]["datetime"]
        errResult.level = level
        return {results: [errResult]}
    }
})(input)