; (function (input) {
    var okResult = {
        desc: "",
        solution: "",
        level: "正常",
        id: "linux.top10mem",
        name: "",
        category: "系统健康检查"
    }

    var errResult = {
        desc: "",
        effect: "",
        solution: "",
        level: "中风险",
        id: "linux.top10mem",
        name: "",
        category: "系统健康检查"
    }

    if (!input) {
        return { results: [errResult] }
    }

    return { results: [okResult] }

})(input)
