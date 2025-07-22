; (function (input, params) {
    var results = []
    var result = {
        _sid: "",
        desc: "当前数据库实例的所有数据库及其容量大小",
        solution: "关注使用情况，及时清理不必要的数据",
        effect: "返回当前数据库实例的所有数据库及其容量大小的信息，帮助用户了解数据库使用情况",
        level: "正常",
        id: "mysql.all_databases_of_the_current_database_instance_and_their_capacity",
        name: "所有数据库的信息",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "返回当前数据库实例的所有数据库及其容量大小的信息",
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
