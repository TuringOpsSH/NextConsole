; (function (input) {
    var results = []
    var result = {
        desc: "死锁平均每天发生次数仅供参考",
        effect: "性能下降、数据不一致、用户体验差、资源浪费和未知错误",
        solution: "缩短事务、适当锁粒度、保持资源顺序、及时释放锁、使用锁超时、READ COMMITTED隔离级别和定期分析死锁日志",
        level: "正常",
        id: "sqlserver.deadlock",
        name: "死锁检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "死锁检查正常",
        category: "",
        family: "any"
    }

    // 非空且元素是字符串认定为执行遇到异常
    try {
        if (Array.isArray(input) && input.length > 0) {
            var allStrings = input.every(function (item) {
                return typeof item === 'string';
            });
            if (allStrings) {
                return { results: [result] };
            }
        }
    } catch (error) {
        return { results: [result] }
    }

    try {
        raw = input
        result.raw = $.copy(input)
    } catch (err) {
        $.print(err.message)
        return { results: [result] }
    }

    if (!raw) {
        return { results: [result] }
    }

    for (i = 0; i < raw.length; i++) {
        mixlevel = "正常"
        fields = {}
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["the_total_number_of_occurrences_of_deadlocks"] //string
        // fields["average_number_of_occurrences_per_day"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    results.push(result)
    return { results: results }

})(input)