; (function (input) {
    if (!input) {return { results: [] }}

    var raw = {}
    for (i = 0; i < input["content"].length; i++) {
        if (input["content"][i].match("^PASS_MAX_DAYS")) {
            raw.PASS_MAX_DAYS = input["content"][i].replace("PASS_MAX_DAYS", "").replace(/^\s+|\s+$/gm, '');
        } else if (input["content"][i].match("^PASS_MIN_DAYS")) {
            raw.PASS_MIN_DAYS = input["content"][i].replace("PASS_MIN_DAYS", "").replace(/^\s+|\s+$/gm, '');
        } else if (input["content"][i].match("^PASS_MIN_LEN")) {
            raw.PASS_MIN_LEN = input["content"][i].replace("PASS_MIN_LEN", "").replace(/^\s+|\s+$/gm, '');
        } else if (input["content"][i].match("^PASS_WARN_AGE")) {
            raw.PASS_WARN_AGE = input["content"][i].replace("PASS_WARN_AGE", "").replace(/^\s+|\s+$/gm, '');
        }
    }

    var results = []
    
    // https://blog.csdn.net/u013739332/article/details/84631595
    if (raw.PASS_MAX_DAYS >= 90) {
        results.push({
            desc: "密码最大使用时间>=90, 当前设置为" + raw.PASS_MAX_DAYS,
            effect: "长期使用相同密码具有安全隐患",
            solution: "设置密码最大使用时间<90",
            name: "密码最大使用时间是否>=90检查",
            level: "中风险",
            id: "linux.etclogindefs1",
            category: "系统合规检查",
            actual:raw.PASS_MAX_DAYS,
            expected:"设置密码最大使用时间<90"
        })
    } else {
        results.push({
            desc: "密码最大使用时间>=90, 当前设置为" + raw.PASS_MAX_DAYS,
            effect: "长期使用相同密码具有安全隐患",
            solution: "设置密码最大使用时间<90",
            name: "密码最大使用时间是否>=90检查",
            level: "正常",
            id: "linux.etclogindefs1",
            category: "系统合规检查",
            actual:raw.PASS_MAX_DAYS,
            expected:"设置密码最大使用时间<90"
        })
    }

    if (raw.PASS_MIN_DAYS < 8) {
        results.push({
            desc: "两次修改密码之间允许的最短天数为" + raw.PASS_MIN_DAYS,
            effect: "两次修改密码之间允许的最短天数过短存在安全隐患",
            solution: "两次修改密码之间允许的最短天数>8",
            name: "两次修改密码之间允许的最短天数>=8检查",
            level: "中风险",
            id: "linux.etclogindefs2",
            category: "系统合规检查",
            actual:raw.PASS_MIN_DAYS,
            expected:"两次修改密码之间允许的最短天数>8"
        })

    } else {
        results.push({
            desc: "两次修改密码之间允许的最短天数为" + raw.PASS_MIN_DAYS,
            effect: "两次修改密码之间允许的最短天数过短存在安全隐患",
            solution: "两次修改密码之间允许的最短天数>8",
            name: "两次修改密码之间允许的最短天数>=8检查",
            level: "正常",
            category: "系统合规检查",
            id: "linux.etclogindefs2",
            actual:raw.PASS_MIN_DAYS,
            expected:"两次修改密码之间允许的最短天数>8"
        })
    }

    if (raw.PASS_WARN_AGE < 7) {
        results.push({
            desc: "当前密码过期前警告为" + raw.PASS_WARN_AGE,
            effect: "无影响，尽早提示以预留修改时间",
            solution: "设置密码过期前警告>7",
            name: "密码过期前警告>=7检查",
            level: "中风险",
            category: "系统合规检查",
            id: "linux.etclogindefs3",
            actual:raw.PASS_WARN_AGE,
            expected:"设置密码过期前警告>7"
        })

    } else {
        results.push({
            desc: "当前密码过期前警告为" + raw.PASS_WARN_AGE,
            effect: "无影响，尽早提示以预留修改时间",
            solution: "设置密码过期前警告>7",
            name: "密码过期前警告>=7检查",
            level: "正常",
            category: "系统合规检查",
            id: "linux.etclogindefs3",
            actual:raw.PASS_WARN_AGE,
            expected:"设置密码过期前警告>7"
        })
    }

    return { results: results }
})(input)
