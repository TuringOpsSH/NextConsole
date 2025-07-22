; (function (input, params) {
    var results = []
    var result = {
        _sid: "",
        desc: "按照登录用户+数据库+登录服务器查看登录信息",
        effect: "可以查看登录用户、数据库和登录服务器的登录信息",
        solution: "使用该规则查询登录信息",
        level: "正常",
        id: "mysql.view_login_information_according_to_login_user_database_login_server",
        name: "数据库登录统计",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "无 SQL 报错并展示查询结果",
        category: "",
        family: "log"
    }

    result._sid = params[2]["Value"]
    
    if (input == null) {
        result.actual = "查询结果为空"
        return {results: [result]}
    }

    if (typeof input[0] == "string") {
        result.expected = "无 SQL 报错并展示查询结果"
        result.level = "中风险"
        result.actual = input
        result.raw = input
        results.push(result)
        return {results: results}
    }
    result.raw = input


    results.push(result)
    return { results: results }

})(input, params)
