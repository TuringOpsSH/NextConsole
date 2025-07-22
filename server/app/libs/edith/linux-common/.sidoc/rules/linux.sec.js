; (function (input) {
    results = []
    result = {
        desc: "",
        id: "linux.sec",
        mixraw: [],
        raw: [],
        actual: "",
        effect: "存在安全隐患, 可能不满足安全合规要求",
        solution: "根据自身情况进行整改",
        level: "正常",
        name: "协议安全检查",
        expected: "禁止 root 用户远程 SSH 登录, 禁止 root 用户登录 FTP, 禁止匿名用户登录 FTP",
        category: "安全合规检查",
        family: "conf"
    }

    try {
        raw = $.copy(input)
        // $.print(raw)
        mixlevel = "正常"

        fields = {}
        fields["item"] = "禁止 root 用户远程 SSH 登录"
        fields["actual"] = raw["/etc/ssh/sshd_config(^PermitRootLogin no)"]
        fields["expected"] = "PermitRootLogin no"
        if (raw["/etc/ssh/sshd_config(^PermitRootLogin no)"] != "PermitRootLogin no") {
            mixlevel = "中风险"
            result.actual += "未禁止 root 用户远程 SSH 登录; "
            result.level = "中风险"

            fields["mixlevel"] = mixlevel
            result.mixraw.push(fields)
        } else {
            fields["mixlevel"] = "正常"
            result.mixraw.push(fields)
        }

        fields = {}
        fields["item"] = "禁止 root 用户登录 FTP"
        fields["actual"] = raw["/etc/vsftpd/ftpusers(^root)"]
        fields["expected"] = "root"
        if (raw["/etc/vsftpd/ftpusers(^root)"] != "root") {
            mixlevel = "中风险"
            result.actual += "未禁止 root 用户登录 FTP; "
            result.level = "中风险"

            fields["mixlevel"] = mixlevel
            result.mixraw.push(fields)
        } else {
            fields["mixlevel"] = "正常"
            result.mixraw.push(fields)
        }

        fields = {}
        fields["item"] = "禁止匿名用户登录 FTP"
        fields["actual"] = raw["/etc/vsftpd/vsftpd.conf(^anonymous_enable=YES)"]
        fields["expected"] = "anonymous_enable != YES"
        if (raw["/etc/vsftpd/vsftpd.conf(^anonymous_enable=YES)"] != "anonymous_enable=YES") {
            mixlevel = "中风险"
            result.actual += "未禁止匿名用户登录 FTP; "
            result.level = "中风险"

            fields["mixlevel"] = mixlevel
            result.mixraw.push(fields)
        } else {
            fields["mixlevel"] = "正常"
            result.mixraw.push(fields)
        }

    } catch (err) {
        $.print(err.message)
        result.level = "低风险"
        result.actual = "原始数据异常"
    }

    // $.print(result)
    results.push(result)



    result = {
        desc: "",
        id: "linux.othersec",
        mixraw: [],
        raw: [],
        actual: "",
        effect: "存在安全隐患, 可能不满足安全合规要求",
        solution: "根据自身情况进行整改",
        level: "正常",
        name: "其他安全检查",
        expected: "符合其他安全检查要求",
        category: "安全合规检查",
        family: "conf"
    }

    try {
        raw = $.copy(input)
        // $.print(raw)
        mixlevel = "正常"

        fields = {}
        fields["item"] = "设置 Shell 空闲等待时间"
        fields["actual"] = raw["TMOUT"]
        fields["expected"] = "(非空)"
        if (raw["TMOUT"] == "") {
            mixlevel = "中风险"
            result.actual += "未设置 Shell 空闲等待时间; "
            result.level = "中风险"

            fields["mixlevel"] = mixlevel
            result.mixraw.push(fields)
        } else {
            fields["mixlevel"] = "正常"
            result.mixraw.push(fields)
        }

        fields = {}
        fields["item"] = "关闭 CTRL+ALT+DEL 快捷键"
        fields["actual"] = raw["/etc/init/control-alt-delete.conf(^exec)"]
        fields["expected"] = "exec"
        if (raw["/etc/init/control-alt-delete.conf(^exec)"] != "exec") {
            mixlevel = "中风险"
            result.actual += "未关闭 CTRL+ALT+DEL 快捷键; "
            result.level = "中风险"

            fields["mixlevel"] = mixlevel
            result.mixraw.push(fields)
        } else {
            fields["mixlevel"] = "正常"
            result.mixraw.push(fields)
        }

        fields = {}
        fields["item"] = "设置 umask 为 0027"
        fields["actual"] = raw["umask"]
        fields["expected"] = "0027"
        if (raw["umask"] != "0027") {
            mixlevel = "中风险"
            result.actual += "未设置 umask 为 0027; "
            result.level = "中风险"

            fields["mixlevel"] = mixlevel
            result.mixraw.push(fields)
        } else {
            fields["mixlevel"] = "正常"
            result.mixraw.push(fields)
        }

        fields = {}
        fields["item"] = "不存在 equiv 文件或 rhosts 文件"
        fields["actual"] = ".rhosts: " + raw["find .rhosts"] + "; hosts.equiv: " + raw["find hosts.equiv"]
        fields["expected"] = ".rhosts: ; hosts.equiv: "
        if (raw["find .rhosts"] != "" && raw["find hosts.equiv"] != "") {
            mixlevel = "中风险"
            result.actual += "存在 equiv 文件或 rhosts 文件; "
            result.level = "中风险"

            fields["mixlevel"] = mixlevel
            result.mixraw.push(fields)
        } else {
            fields["mixlevel"] = "正常"
            result.mixraw.push(fields)
        }

        fields = {}
        fields["item"] = "关闭路由转发"
        fields["actual"] = raw["ip_forward"]
        fields["expected"] = "0"
        if (raw["ip_forward"] != "0") {
            mixlevel = "中风险"
            result.actual += "未关闭路由转发; "
            result.level = "中风险"

            fields["mixlevel"] = mixlevel
            result.mixraw.push(fields)
        } else {
            fields["mixlevel"] = "正常"
            result.mixraw.push(fields)
        }

        fields = {}
        fields["item"] = "禁止 ICMP 源路由"
        fields["actual"] = raw["accept_source_route"]
        fields["expected"] = "0"
        if (raw["accept_source_route"] != "0") {
            mixlevel = "中风险"
            result.actual += "未禁止 ICMP 源路由; "
            result.level = "中风险"

            fields["mixlevel"] = mixlevel
            result.mixraw.push(fields)
        } else {
            fields["mixlevel"] = "正常"
            result.mixraw.push(fields)
        }


        fields = {}
        fields["item"] = "记录命令历史数量小于 10000"
        fields["actual"] = raw["HISTSIZE"]
        fields["expected"] = "< 10000"
        if (Number(raw["HISTSIZE"]) >= 10000) {
            mixlevel = "中风险"
            result.actual += "记录命令历史数量大于等于 10000; "
            result.level = "中风险"

            fields["mixlevel"] = mixlevel
            result.mixraw.push(fields)
        } else {
            fields["mixlevel"] = "正常"
            result.mixraw.push(fields)
        }


        fields = {}
        fields["item"] = "关闭命令时间戳记录"
        fields["actual"] = raw["HISTTIMEFORMAT"]
        fields["expected"] = "(空)"
        if (raw["HISTTIMEFORMAT"] != "") {
            mixlevel = "中风险"
            result.actual += "开启了命令时间戳记录; "
            result.level = "中风险"

            fields["mixlevel"] = mixlevel
            result.mixraw.push(fields)
        } else {
            fields["mixlevel"] = "正常"
            result.mixraw.push(fields)
        }


    } catch (err) {
        $.print(err.message)
        result.level = "低风险"
        result.actual = "原始数据异常"
    }

    // $.print(result)
    results.push(result)
    return { results: results }
})(input)