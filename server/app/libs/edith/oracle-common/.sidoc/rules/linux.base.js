; (function (input) {

    var results = []    
    if (input["SELinux"] == "disabled") {
        results.push({
            desc: "selinux检查,检查是否关闭",
            solution: "",
            level: "正常",
            id: "linux.base",
            name: "selinux检查",
            category: "基本配置检查",
            actual: "abled",
            expected: "disabled"
        })
        return { results: results }
    } else {
        results.push({
            desc: "selinux检查",
            effect: "关闭selinux",
            solution: "",
            level: "中风险",
            id: "linux.base",
            name: "selinux检查",
            category: "基本配置检查",
            actual: "abled",
            expected: "disabled"
        })
        return { results: results }
    }


})(input)
