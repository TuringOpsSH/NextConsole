; (function (input) {
    var okResult = {
        startupMode: "",
        datetime:"",
        id: "wls.serverRuntime",
        name: "Server运行状态"
    }

    var errResult = {
        effect: "Server运行状态异常",
        solution: "建议检查Server启动情况",
        startupMode: "",
        datetime: "",
        id: "wls.serverRuntime",
        name: "Server运行状态"
    }

   

    if (input[0]["metric"] == "RUNNING" ) {
        okResult.startupMode = input[0]["metric"]
        okResult.datetime = input[0]["datetime"]
        return { results: [okResult] }
    } else {
        errResult.startupMode = input[0]["metric"]
        errResult.datetime = input[0]["datetime"]
        return { results: [errResult] }
    }



})(input)