; (function (input) {
    var okResult = {
        desc: "",
        solution: "",
        level: "正常",
        id: "linux.psaux",
        name: "",
        category: "health"
    }

    var errResult = {
        desc: "",
        effect: "",
        solution: "",
        level: "中风险",
        id: "linux.psaux",
        name: "",
        category: "health"
    }

    if (!input) {
        return { results: [errResult] }
    }

    return { results: [okResult] }

})(input)
