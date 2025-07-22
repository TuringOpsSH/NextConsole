; (function (input) {
    results = []
    result = {
        desc: "",
        id: "linux.test",
        mixraw: [],
        raw: "test",
        actual: "",
        effect: "",
        solution: "",
        level: "",
        name: "",
        expected: "",
        category: "",
        family: ""
    }

    try {
        result.raw = "select * from V$DEADLOCK_HISTORY;"
    } catch (err) {
        $.print(err.message)
        result.actual = "无数据"
    }

    results.push(result)
    return { results: results }
})(input)
