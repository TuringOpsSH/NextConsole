; (function (input) {
    var okResult = {
        desc: "将两个或者更多的物理网卡绑定成一个虚拟网卡实现本地网卡的冗余、带宽扩容和负载均衡",
        effect: "存在网卡单点故障风险",
        solution: "对网卡进行绑定配置以实现冗余",
        level: "正常",
        id: "linux.bonding",
        name: "网卡绑定检查",
        category: "系统健康检查",
        actual: "已设置",
        expected: "主要网卡处于绑定状态",
        raw: {}
    }

    var errResult = {
        desc: "将两个或者更多的物理网卡绑定成一个虚拟网卡实现本地网卡的冗余、带宽扩容和负载均衡",
        effect: "存在网卡单点故障风险",
        solution: "对网卡进行绑定配置以实现冗余",
        level: "中风险",
        id: "linux.bonding",
        name: "网卡绑定检查",
        category: "系统健康检查",
        actual: "未设置",
        expected: "主要网卡处于绑定状态",
        raw: {}
    }

    if (!input) {
        return { results: [errResult] }
    }

    if (input["/proc/net/bonding/*"] == "" && input["nmcli connection show (team)"] == "") {
        errResult.raw.bonding1 = "未设置"
        errResult.raw.bonding2 = "未设置"
        return { results: [errResult] }
    } else {
        okResult.raw.bonding1 = input["/proc/net/bonding/*"]
        okResult.raw.bonding2 = input["nmcli connection show (team)"]
        return { results: [okResult] }
    }

}) (input)
