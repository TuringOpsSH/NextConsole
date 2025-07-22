; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "集群环境下, 应保持充足的可用 ticket",
        level: "正常",
        id: "oracle.ges_traffic",
        name: "节点间私网流量检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "集群环境下, 应保持充足的可用 ticket",
        category: "集群状态",
        family: "status"
    }
    
    if (!input) {
        result.desc = "未发现节点间私网流量数据"
        result.actual = "未发现节点间私网流量数据"
        return { results: [result] }
    }

    if (result.family == "status"){
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        result.actual = "未发现节点间私网流量数据"
        return { results: [result] }
    }

    for (i = 0; i < raw.length; i++) {
        mixlevel = ""
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["inst_id"] //string
        // fields["local_nid"] //string
        // fields["remote_rid"] //string
        // fields["remote_inc"] //string
        // fields["tckt_avail"] //string
        // fields["tckt_limit"] //string
        // fields["tckt_wait"] //string


        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }
    
    results.push(result)
    return { results: results }

})(input)
