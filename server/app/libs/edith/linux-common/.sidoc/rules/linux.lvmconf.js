; (function (input) {
    var okResult = {
        desc: "已设置 filter",
        solution: "如果系统有配置多路径，最好设置 filter",
        level: "正常",
        id: "linux.lvmconf",
        name: "/etc/lvm/lvm.conf 是否设置 filter 检查",
        category: "系统健康检查",
        actual: "",
        expected: "如果系统有配置多路径，最好设置 filter",
    }

    var errResult = {
        desc: "未设置 filter ",
        effect: "可能存在操作系统或租户卷损坏的风险",
        solution: "如果系统有配置多路径，最好设置 filter",
        level: "中风险",
        id: "linux.lvmconf",
        name: "/etc/lvm/lvm.conf 是否设置 filter 检查",
        category: "系统健康检查",
        actual: "",
        expected: "如果系统有配置多路径，最好设置 filter",
    }

    if (!input) {
        errResult.desc = "未获取到 lvm.conf 文件"
        return { results: [okResult] }
    }

    if (input.hasOwnProperty("preferred_names") && input.hasOwnProperty("filter")) {
        okResult.actual = okResult.desc + input["filter"]
        okResult.desc += input["filter"]
        return { results: [okResult] }
    } else {
        errResult.actual = "未设置 filter "
        return { results: [errResult] }
    }

})(input)
