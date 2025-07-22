; (function (input) {
    var okResult = {
        desc: "open files 设置正常",
        level: "正常",
        actual: "",
        expected: "open files 设置为10240以上",
        name: "open files 配置参数",
        id: "linux.ulimita",
        category: "config"
    }

    var errResult = {
        desc: "open files 设置过小",
        expected: "open files 设置为10240以上",
        solution: "建议设置为 10240以上",
        level: "中风险",
        actual: "",
        id: "linux.ulimita",
        name: "open files 配置参数",
        category: "config"
    }

    if (input == "") {
        errResult.actual  = "open files 未设置"
        return { results: [errResult] }
    }

    if (input["open files"] < 10240) {
        errResult.actual = input["open files"]
        errResult.desc = "open files 设置小于10240，当前为：" + input["open files"]
        errResult.level = "中风险"
        return { results: [errResult] }
    } else {
        // okResult.actual = input["open files"]
        return { results: [okResult] }
    }


})(input)
