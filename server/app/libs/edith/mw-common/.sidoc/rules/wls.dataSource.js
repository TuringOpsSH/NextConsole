; (function (input) {

    var problemId = "wls.dataSource"
    var okResult = {
        level: "None",
        id: problemId
    }

    var errResult = {
        desc: "未设置连接池大小",
        effect: "连接池过小，无法承载较大的压力",
        solution: "连接池的初始值设置为10，最大值最少设置为10",
        level: "low",
        id: problemId,
        name: "需要设置数据库连接池的最大最小值",
    }

    if (input["connectionPool"]["min"] == "" || input["connectionPool"]["max"] == "") {
        return { results: [errResult] }
    }

    if (input["connectionPool"]["min"] < 10 || input["connectionPool"]["max"] < 10) {
        // log(100000)
        errResult.desc = "设置的最大最小值过小（" + input["connectionPool"]["min"] + "," + input["connectionPool"]["max"] + "）"
        return { results: [errResult] }
    }


    return {
        exports: {},
        results: [
            errResult
        ]
    }


})(input)