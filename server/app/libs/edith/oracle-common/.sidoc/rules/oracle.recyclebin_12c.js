; (function (input, params) {
    try {
        if (Number(params[3].Value) < 12) {
            return
        }
    } catch { }

    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "及时清理回收站",
        level: "正常",
        id: "oracle.recyclebin_12c",
        name: "回收站使用检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "回收站对象数量不超过2000",
        category: "status",
        family: "status"
    }

    if (!input) {
        result.actual = "未发现回收站使用信息"
        return { results: [result] }
    }

    if (result.family == "status") {
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        result.actual = "未发现回收站使用信息"
        return { results: [result] }
    }

    for (i = 0; i < raw.length; i++) {
        mixlevel = ""
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["pdb_name"] //string
        // fields["tbs_name"] //string
        // fields["cnt"] //string
        if (Number(fields["cnt"]) > 2000) {
            result.actual = "回收站对象过多"
            result.level = "中风险"
            mixlevel = "中风险"
        } else {
            mixlevel = "正常"
        }


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }
    // if (result.desc == "") {
    //     result.actual = "回收站对象数量正常"
    // }

    results.push(result)
    return { results: results }

})(input, params)
