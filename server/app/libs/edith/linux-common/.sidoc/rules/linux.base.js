; (function (input) {

    var results = []    
    if (input["SELinux"] == "disabled") {
        results.push({
            desc: "",
            solution: "设置 SELinux 为 disabled",
            level: "正常",
            id: "linux.base",
            name: "SELinux 检查",
            category: "系统配置检查",
            actual: "abled",
            expected: "disabled",
            effect: "可能使某些程序无法正常运行"
        })
        return { results: results }
    } else {
        results.push({
            desc: "",
            solution: "设置 SELinux 为 disabled",
            level: "中风险",
            id: "linux.base",
            name: "SELinux 检查",
            category: "系统配置检查",
            actual: input["SELinux"] ,
            expected: "disabled",
            effect: "可能使某些程序无法正常运行"
        })
        return { results: results }
    }


})(input)
