; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "检查 DG 配置及归档传输",
        level: "正常",
        id: "oracle.archive_dest_status",
        name: "DG 配置检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected: "日志传输正常",
        category: "系统备份",
        family: "status"
    }
    
    if (!input) {
        result.actual = "未发现配置信息"
        return { results: [result] }
    }

    if (result.family == "status"){
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        result.actual = "未发现配置信息"
        return { results: [result] }
    }

    for (i = 0; i < raw.length; i++) {
        mixlevel = ""
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["dest_id"] //int
        // fields["dest_name"] //string
        // fields["DESTINATION"] //string
        // fields["DB_UNIQUE_NAME"] //string
        // fields["type"] //string
        // fields["DATABASE_MODE"] //string
        // fields["RECOVERY_MODE"] //string
        // fields["status"] //string
        // fields["STANDBY_LOGFILE_COUNT"] //int
        if(fields["status"] != "nan" && fields["status"] != "VALID" && fields["status"] != "INACTIVE" && fields["status"] != "DISABLED"){
            result.actual = "日志传输异常"
            result.level = "高风险"
            mixlevel = "高风险"
        }else{
            mixlevel = "正常"
        }

        // if row_cells[7].text != 'nan' and  row_cells[7].text != 'VALID' and row_cells[7].text != 'INACTIVE':
        // check_result=u'日志传输异常'
        // adjust = u'检查DG 配置及归档传输'

        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }
    if(result.level == "正常"){
        result.actual = result.expected
    }

    results.push(result)
    return { results: results }

})(input)
