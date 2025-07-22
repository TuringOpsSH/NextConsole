; (function (input) {
    var okResult = {
        desc: "",
        solution: "",
        level: "正常",
        id: "linux.psef",
        name: "",
        category: "基本配置检查"
    }

    var errResult = {
        desc: "",
        effect: "",
        solution: "",
        level: "中风险",
        id: "linux.psef",
        name: "",
        category: "基本配置检查"
    }

    if (!input) {
        return { results: [errResult] }
    }

    return { results: [okResult] }

})(input)
