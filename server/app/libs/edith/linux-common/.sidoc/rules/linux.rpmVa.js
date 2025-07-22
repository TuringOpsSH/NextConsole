; (function (input) {
    var okResult = {
        desc: "检查系统关键文件/etc、/boot等目录下文件是否出现文件丢失、文件权限改变等情况",
        solution: "如果由系统正常变更引起可以忽略此告警",
        effect: "可能包含异常告警信息",
        level: "正常",
        id: "linux.rpmVa",
        name: "rpm 完整性检查",
        raw: [],
        actual: "",
        expected: "/etc、/boot等目录下文件未出现文件丢失、文件权限改变等情况",
        category: "系统健康检查"
    }

    var errResult = {
        desc: "检查系统关键文件/etc、/boot等目录下文件是否出现文件丢失、文件权限改变等情况",
        solution: "如果由系统正常变更引起可以忽略此告警",
        effect: "可能包含异常告警信息",        
        level: "中风险",
        id: "linux.rpmVa",
        name: "rpm 完整性检查",
        raw: [],
        actual: "",
        expected: "/etc、/boot等目录下文件未出现文件丢失、文件权限改变等情况",
        category: "系统健康检查"
    }

    errResult.raw = input
    okResult.raw = input

    if (!input) {
        okResult.actual = "/etc、/boot等目录下文件未出现文件丢失、文件权限改变等情况"
        return { results: [okResult] }
    } else {
        errResult.actual = "/etc、/boot等目录下出现文件丢失、文件权限改变等情况"
        return { results: [errResult] }
    }

})(input)