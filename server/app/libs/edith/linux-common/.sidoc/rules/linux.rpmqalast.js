; (function (input) {
    var okResult = {
        desc: "检查是否存在RHEL6安装RHEL7 RPM包、RHEL7是否安装RHEL6 RPM包或RHEL系统安装CentOS软件包",
        solution: "尽量使安装版本与系统版本匹配以避免兼容性问题",
        effect: "当版本不匹配时可能存在rpm兼容性问题",
        level: "正常",
        id: "linux.rpmqalast",
        name: "rpm 状态检查",
        raw: [],
        actual: "",
        expected: "尽量使安装版本与系统版本匹配以避免兼容性问题",
        category: "系统健康检查"
    }

    var errResult = {
        desc: "检查是否存在RHEL6安装RHEL7 RPM包、RHEL7是否安装RHEL6 RPM包或RHEL系统安装CentOS软件包",
        effect: "可能存在rpm兼容性问题",
        solution: "尽量使安装版本与系统版本匹配以避免兼容性问题",
        level: "中风险",
        id: "linux.rpmqalast",
        name: "rpm 状态检查",
        raw: [],
        actual: "",
        expected: "尽量使安装版本与系统版本匹配以避免兼容性问题",
        category: "系统健康检查"
    }

    if (!input) {
        return { results: [okResult] }
    }

    el6 = 0
    el7 = 0
    el8 = 0

    raw6 = []
    raw7 = []
    raw8 = []

    for (i = 0; i < input.length; i++) {
        if (!input[i].match("edith-")) {
            if (input[i].match(".el6.")) {
                el6 += 1
                raw6.push(input[i])
            } else if (input[i].match(".el7.")) {
                el7 += 1
                raw7.push(input[i])
            } else if (input[i].match(".el8.")) {
                el8 += 1
                raw8.push(input[i])
            }
        }
    }

    // 通过包数量简单判断操作系统版本，合并数量少的两个数组作为异常数据进行展示
    if (raw6.length >= raw7.length && raw6.length >= raw8.length) { // el6
        errResult.raw = raw7.concat(raw8)
    } else if (raw7.length >= raw6.length && raw7.length >= raw8.length) { // el7
        errResult.raw = raw6.concat(raw8)
    } else { // el8
        errResult.raw = raw6.concat(raw7)
    }

    errResult.actual += "当前系统存在el6包" + el6 + "个，存在el7包" + el7 + "个，存在el8包" + el8 + "个"
    okResult.actual += "当前系统存在el6包" + el6 + "个，存在el7包" + el7 + "个，存在el8包" + el8 + "个"

    if (el6 != 0 && el7 != 0) {
        return { results: [errResult] }
    } else if (el6 != 0 && el8 != 0) {
        return { results: [errResult] }
    } else if (el7 != 0 && el8 != 0) {
        return { results: [errResult] }
    } else {
        return { results: [okResult] }
    }
})(input)