; function isInArray(arr, value) {
    for (var i = 0; i < arr.length; i++) {
        if (value === arr[i]) {
            return true;
        }
    }
    return false;
}

; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "存在安全合规隐患",
        solution: "检查权限分配是否合理",
        level: "正常",
        id: "oracle.sysdba",
        name: "SYSDBA 权限用户检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "非 SYS, SYSDG, SYSKM, SYSBACKUP 用户无 SYSDBA 权限",
        category: "系统安全及审计",
    }

    if (!input) {
        result.desc += "未采集到数据"
        result.actual += "未采集到数据"
        result.level = "低风险"
        return { results: [result] }
    }

    if (result.family == "status") {
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        result.desc += "未采集到数据"
        result.actual += "未采集到数据"
        result.level = "低风险"
        return { results: [result] }
    }

    User = ['SYS', 'SYSDG', 'SYSKM', 'SYSBACKUP']
    erruser = []
    for (i = 0; i < raw.length; i++) {
        mixlevel = ""
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["username"] //string
        // fields["sysdba"] //string
        // fields["sysoper"] //string
        // fields["yesno"] //string
        if (fields["yesno"] == "YES") {
            if (!isInArray(fields["username"])) {
                mixlevel = "中风险"
                erruser.push(fields["username"])
                result.desc = "非SYS, SYSDG, SYSKM, SYSBACKUP用户具有SYSDBA权限"
                result.actual = "非SYS, SYSDG, SYSKM, SYSBACKUP用户具有SYSDBA权限"
            } else {
                mixlevel = "正常"
            }
        }


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    if (erruser.length > 0) {
        result.actual += ", 用户名为: "
        for (i = 0; i < erruser.length; i++) {
            result.actual += erruser[i] + ", "
        }
    }

    results.push(result)
    return { results: results }

})(input)
