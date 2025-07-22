;(function (params) {
    // $.print(params[0])
    var results = []
    for (var i = 0; i < params[0].length; i++) {
        if (params[0][i]["id"] == "pgversion" || params[0][i]["id"] == "cluster_info" || params[0][i]["id"] == "table_sizes") {
            results.push(params[0][i])
        }
    }
    // $.print(results)
    m = new Map
    var objs = []
    for (var i2 = 0; i2 < results.length; i2++) {
        if (!m.has(results[i2]["_name"])) {
            objs.push(results[i2]["_name"])
        }
    }
    // $.print(objs)
    var res = {}
    for (var i3 = 0; i3 < objs.length; i3++) {
        var obj = []
        for (var i4 = 0; i4 < results.length; i4++) {
            if (results[i4]["_name"] == objs[i3]) {
                obj.push(results[i4])
            }
        }
        res[objs[i3]] = obj
    }
    // $.print(res)
    return res
})(input)