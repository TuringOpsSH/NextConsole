;(function (input) {
    var results = []
    var result = {
        desc: "配置文件修改信息",
        effect: "",
        solution: "",
        level: "正常",
        id: "altersettings",
        name: "配置文件修改信息",
        mixraw: [],
        raw: {},
        actual: "",
        expected: "",
        category: "",
        family: "conf"
    }

    if (!input) {
        result.actual = "查询结果为空"
        return {results: [result]}
    }
    try {
        // raw = {}
        var res = {
            count: "",
            examples: "",
            sourcefile: ""
        }
        var defaults = {
            count: "",
            examples: "",
            sourcefile: ""
        }
        var totalRes = {
            res,
            defaults
        }
        resObj = input["changes"][0]
        var examples = ""
        for (var i1 = 0; i1 < resObj["examples"].length; i1++) {
            if (i1 == resObj["examples"].length - 1) {
                examples += resObj["examples"][i1]
            } else {
                examples += resObj["examples"][i1] + ","
            }
        }
        res.count = resObj["count"]
        res.examples = examples
        res.sourcefile = resObj["sourcefile"]

        defaultsObj=input["changes"][1]
        defaults.count=defaultsObj["count"]
        defaults.examples=defaults["examples"]
        if (defaults["sourcefile"]==null||defaults["sourcefile"]==""){
            defaults.sourcefile="default"
        }else {
            defaults.sourcefile=defaults["sourcefile"]
        }
        // getOb = $.copy(input)
        // $.print(getOb)
        result.raw = totalRes
    } catch (err) {
        $.print(err.message)
        result.level = "低风险"
        result.actual = "原始数据异常"
        result.solution = ""
    }
    results.push(result)
    return {results: results}

})(input)
