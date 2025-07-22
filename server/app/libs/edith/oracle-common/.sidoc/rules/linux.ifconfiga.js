; (function (input) {
    var okResult = {
        desc: "",
        solution: "",
        level: "正常",
        id: "linux.ifconfiga",
        name: "",
        category: "基本配置检查",
        actual:"",
        expected:""
    }

    var errResult = {
        desc: "",
        effect: "",
        solution: "",
        level: "中风险",
        id: "linux.ifconfiga",
        name: "",
        category: "基本配置检查",
        actual:"",
        expected:""
    }

    if (!input) {
        return {
            results: [errResult]
        }
    }

    return {
        results: [okResult]
    }

})(input)
