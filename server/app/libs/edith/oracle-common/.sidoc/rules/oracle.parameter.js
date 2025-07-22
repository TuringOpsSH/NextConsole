; (function (input, params) {
    try {
        if (Number(params[3].Value) >= 12) {
            return
        }
    } catch { }

    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "仅作为调优或问题排查时的参考",
        level: "正常",
        id: "oracle.parameter",
        name: "数据库系统参数检查",
        mixraw: [],
        raw: [],
        actuals: [],
        actual: "",
        expected: "各参数设置符合预期值",
        category: "数据库组件及参数设置",
        family: "conf"
    }

    if (!input) {
        return { results: [result] }
    }

    if (result.family == "status") {
        raw = input[0]["metric"]
    } else {
        raw = input
    }

    if (!raw) {
        return { results: [result] }
    }

    cpu_count = 1
    for (i = 0; i < raw.length; i++) {
        mixlevel = ""
        fields = raw[i]

        // Check fields, reset mixlevel and result.level here:

        // fields["inst_id"] //int
        // fields["name"] //string
        // fields["value"] //string
        if (fields["name"] == "cpu_count") {
            cpu_count = Number(fields["value"])
        }

        else if (fields["name"] == "cursor_sharing") {
            if (fields["value"] != "EXACT") {
                // mixlevel = "中风险"
                result.actuals.push("cursor_sharing预期为EXACT, 实际为" + fields["value"])
            } else {
                // mixlevel = "正常"
            }
        }

        else if (fields["name"] == "deferred_segment_creation") {
            if (fields["value"] == "TRUE") {
                // mixlevel = "中风险"
                result.actuals.push("deferred_segment_creation预期为!=TRUE, 实际为" + fields["value"])
            } else {
                // mixlevel = "正常"
            }
        }

        else if (fields["name"] == "aq_tm_processes") {
            if (fields["value"] == "0") {
                // mixlevel = "中风险"
                result.actuals.push("aq_tm_processes预期为!=0, 实际为" + fields["value"])
            } else {
                // mixlevel = "正常"
            }
        }

        else if (fields["name"] == "max_dump_file_size") {
            if (fields["value"] == "unlimited") {
                // mixlevel = "中风险"
                result.actuals.push("max_dump_file_size预期为!=unlimited, 实际为" + fields["value"])
            } else {
                // mixlevel = "正常"
            }
        }

        else if (fields["name"] == "optimizer_mode") {
            if (fields["value"] != "ALL_ROWS") {
                // mixlevel = "中风险"
                result.actuals.push("optimizer_mode预期为ALL_ROWS, 实际为" + fields["value"])
            } else {
                // mixlevel = "正常"
            }
        }

        else if (fields["name"] == "result_cache_max_size") {
            if (fields["value"] != "0") {
                // mixlevel = "中风险"
                result.actuals.push("result_cache_max_size预期为0, 实际为" + fields["value"])
            } else {
                // mixlevel = "正常"
            }
        }

        else if (fields["name"] == "standby_file_management") {
            if (fields["value"] == "MANUAL") {
                // mixlevel = "中风险"
                result.actuals.push("standby_file_management预期为!=MANUAL, 实际为" + fields["value"])
            } else {
                // mixlevel = "正常"
            }
        }

        else if (fields["name"] == "recovery_parallelism") {
            if (fields["value"] == "0") {
                // mixlevel = "中风险"
                result.actuals.push("recovery_parallelism预期为!=0, 实际为" + fields["value"])
            } else {
                // mixlevel = "正常"
            }
        }

        else if (fields["name"] == "parallel_max_servers") {
            if (Number(fields["value"]) > cpu_count / 2) {
                // mixlevel = "中风险"
                result.actuals.push("parallel_max_servers预期为 <= cpu_count / 2, 实际为" + fields["value"])
            } else {
                // mixlevel = "正常"
            }
        }

        else if (fields["name"] == "log_archive_dest_2") {
            if (fields["value"].toUpperCase().match("ASYNC")) {
                // mixlevel = "中风险"
                result.actuals.push("log_archive_dest_2预期为!ASYNC, 实际为" + fields["value"])
            } else if (fields["value"] != "" && fields["value"] != "NOT-CONFIGURE") {
                // mixlevel = "中风险"
                result.actuals.push("log_archive_dest_2预期为NOT-CONFIGURE, 实际为" + fields["value"])
            } else {
                // mixlevel = "正常"
            }
        }

        else if (fields["name"] == "control_file_record_keep_time") {
            if (Number(fields["value"]) < 30) {
                // mixlevel = "中风险"
                result.actuals.push("control_file_record_keep_time预期为>=30, 实际为" + fields["value"])
            } else {
                // mixlevel = "正常"
            }
        }

        else if (fields["name"] == "control_management_pack_access") {
            if (fields["value"] != "DIAGNOSTIC+TUNING") {
                // mixlevel = "中风险"
                result.actuals.push("control_management_pack_access预期为DIAGNOSTIC+TUNING, 实际为" + fields["value"])
            } else {
                // mixlevel = "正常"
            }
        }

        else if (fields["name"] == "job_queue_processes") {
            if (Number(fields["value"]) == 0) {
                mixlevel = "高风险"
                result.actuals.push("job_queue_processes预期为!=0, 实际为" + fields["value"])
                result.effect += "job_queue_processes 为 0 会导致后台进程无法启动, 导致大部分后台任务无法运行"
            } else {
                mixlevel = "正常"
            }
        }

        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }

    for (i = 0; i < result.mixraw.length; i++) {
        if (result.mixraw[i]["mixlevel"] == "高风险") {
            result.level = "高风险"
        }
    }

    
    if (result.actuals.length == 0) {
        result.actuals = ["符合预期"]
    }

    result.actual = result.actuals.join("; ")

    results.push(result)
    return { results: results }

})(input, params)

