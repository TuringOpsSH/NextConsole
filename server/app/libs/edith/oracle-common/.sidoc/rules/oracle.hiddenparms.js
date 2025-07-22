; (function (input) {
    var results = []
    var result = {
        desc: "",
        effect: "",
        solution: "仅作为调优或问题排查时的参考",
        level: "正常",
        id: "oracle.hiddenparms",
        name: "最佳实践参数设置检查",
        mixraw: [],
        raw: [],
        actual: "",
        expected : "参数设置符合最佳实践",
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

    var reg = new RegExp('\\|', "g")
    for (i = 0; i < raw.length; i++) {
        mixlevel = ""
        iseq = ""
        fields = raw[i]
        fields["ksppstvl"] = fields["ksppstvl"].replace(reg, ", ") 
        // Check fields, reset mixlevel and result.level here:

        // fields["ksppinm"] //string
        // fields["ksppstvl"] //string

        if (fields["ksppinm"] == '_gc_policy_time') {
            fields["expected"]  = '0'
            if (fields["ksppstvl"] != fields["expected"] ) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }

        else if (fields["ksppinm"] == '_optimizer_adaptive_cursor_sharing') {
            fields["expected"]  = 'TRUE'
            if (fields["ksppstvl"] != fields["expected"] ) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }


        else if (fields["ksppinm"] == '_abort_on_mrp_crash') {
            fields["expected"]  = 'FALSE'
            if (fields["ksppstvl"] != fields["expected"] ) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }


        else if (fields["ksppinm"] == '_optimizer_extended_cursor_sharing_rel') {
            fields["expected"]  = 'NONE'
            if (fields["ksppstvl"] != fields["expected"] ) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }


        else if (fields["ksppinm"] == '_optimizer_extended_cursor_sharing') {
            fields["expected"]  = 'NONE'
            if (fields["ksppstvl"] != fields["expected"] ) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }


        else if (fields["ksppinm"] == '_optimizer_use_feedback') {
            fields["expected"]  = 'FALSE'
            if (fields["ksppstvl"] != fields["expected"] ) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }

        else if (fields["ksppinm"] == '_serial_direct_read') {
            fields["expected"]  = 'NEVER'
            if (fields["ksppstvl"] != fields["expected"] ) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }


        else if (fields["ksppinm"] == '_partition_large_extents') {
            fields["expected"]  = 'FALSE'
            if (fields["ksppstvl"] != fields["expected"] ) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }


        else if (fields["ksppinm"] == '_gc_defer_time') {
            fields["expected"]  = '3'
            if (fields["ksppstvl"] != fields["expected"] ) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }
        

        else if (fields["ksppinm"] == '_gc_read_mostly_locking') {
            fields["expected"]  = 'FALSE'
            if (fields["ksppstvl"] != fields["expected"] ) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }


        else if (fields["ksppinm"] == '_cursor_obsolete_threshold') {
            fields["expected"]  = '400'
            if (fields["ksppstvl"] != fields["expected"] ) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }

        else if (fields["ksppinm"] == '_use_single_log_writer') {
            fields["expected"]  = 'TRUE'
            if (fields["ksppstvl"] != fields["expected"] ) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }


        else if (fields["ksppinm"] == '_use_adaptive_log_file_sync') {
            fields["expected"]  = 'FALSE'
            if (fields["ksppstvl"] != fields["expected"] ) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }


        else if (fields["ksppinm"] == '_px_use_large_pool') {
            fields["expected"]  = 'TRUE'
            if (fields["ksppstvl"] != fields["expected"] ) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }

        else if (fields["ksppinm"] == '_undo_autotune') {
            fields["expected"]  = 'FALSE'
            if (fields["ksppstvl"] != fields["expected"] ) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }


        else if (fields["ksppinm"] == '_trace_files_public') {
            fields["expected"]  = 'TRUE'
            if (fields["ksppstvl"] != fields["expected"] ) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }

        else if (fields["ksppinm"] == '_datafile_write_errors_crash_instance') {
            fields["expected"]  = 'FALSE'
            if (fields["ksppstvl"] != fields["expected"] ) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }

        else if (fields["ksppinm"] == '_ktb_debug_flags') {
            fields["expected"]  = '8'
            if (fields["ksppstvl"] != fields["expected"] ) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }


        else if (fields["ksppinm"] == '_gc_bypass_readers') {
            fields["expected"]  = 'FALSE'
            if (fields["ksppstvl"] != fields["expected"] ) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }


        else if (fields["ksppinm"] == '_gc_override_force_cr') {
            fields["expected"]  = 'FALSE'
            if (fields["ksppstvl"] != fields["expected"] ) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }

        else if (fields["ksppinm"] == '_gc_read_mostly_locking') {
            fields["expected"]  = 'FALSE'
            if (fields["ksppstvl"] != fields["expected"] ) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }

        else if (fields["ksppinm"] == '_lm_tickets') {
            fields["expected"]  = '5000'
            if (fields["ksppstvl"] != fields["expected"] ) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }

        else if (fields["ksppinm"] == '_gc_undo_affinity') {
            fields["expected"]  = 'FALSE'
            if (fields["ksppstvl"] != fields["expected"] ) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }

        else if (fields["ksppinm"] == '_log_segment_dump_patch') {
            fields["expected"]  = 'FALSE'
            if (fields["ksppstvl"] != fields["expected"] ) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }


        else if (fields["ksppinm"] == '_ash_enable') {
            fields["expected"]  = 'TRUE'
            if (fields["ksppstvl"] != fields["expected"] ) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }


        else if (fields["ksppinm"] == '_ash_size') {
            fields["expected"]  = '254M'
            if (fields["ksppstvl"] != fields["expected"] ) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }

        else if (fields["ksppinm"] == '_cleanup_rollback_entries') {
            fields["expected"]  = '10000'
            if (Number(fields["ksppstvl"]) < 10000) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为>" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }

        else if (fields["ksppinm"] == '_clusterwide_global_transactions') {
            fields["expected"]  = 'FALSE'
            if (fields["ksppstvl"] != fields["expected"] ) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }

        else if (fields["ksppinm"] == '_cursor_obsolete_threshold') {
            fields["expected"]  = '1000' // TODO
            if (Number(fields["ksppstvl"]) >= 1000) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为<1000, 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }

        else if (fields["ksppinm"] == '_rollback_segment_count') {
            fields["expected"]  = '1000' // TODO
            if (Number(fields["ksppstvl"]) == 0) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }

        else if (fields["ksppinm"] == '_adg_parselock_timeout') {
            fields["expected"]  = '500'
            if (Number(fields["ksppstvl"]) < 500) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为 >" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }

        else if (fields["ksppinm"] == '_index_partition_large_extents') {
            fields["expected"]  = 'FALSE'
            if (fields["ksppstvl"] != fields["expected"] ) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }

        else if (fields["ksppinm"] == '_index_partition_large_extents') {
            fields["expected"]  = 'FALSE'
            if (fields["ksppstvl"] != fields["expected"] ) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }

        else if (fields["ksppinm"] == '_lm_sync_timeout' && fields["ksppstvl"] != 'nan') {
            fields["expected"]  = '1200'
            if (fields["ksppstvl"] != fields["expected"] ) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }

        else if (fields["ksppinm"] == '_optim_peek_user_binds') {
            fields["expected"]  = 'FALSE'
            if (fields["ksppstvl"] != fields["expected"] ) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }



        else if (fields["ksppinm"] == '_enable_automatic_sqltune') {
            fields["expected"]  = 'FALSE'
            if (fields["ksppstvl"] != fields["expected"] ) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }




        else if (fields["ksppinm"] == '_enable_shared_pool_durations') {
            fields["expected"]  = 'FALSE'
            if (fields["ksppstvl"] != fields["expected"] ) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }




        else if (fields["ksppinm"] == 'fast_index_maintenance') {
            fields["expected"]  = 'FALSE'
            if (fields["ksppstvl"] != fields["expected"] ) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }



        else if (fields["ksppinm"] == '_dlm_stats_collect') {
            fields["expected"]  = '0'
            if (fields["ksppstvl"] != fields["expected"] ) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }



        else if (fields["ksppinm"] == '_enable_NUMA_support') {
            fields["expected"]  = 'FALSE'
            if (fields["ksppstvl"] != fields["expected"] ) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }



        else if (fields["ksppinm"] == '_fast_index_maintenance') {
            fields["expected"]  = 'FALSE'
            if (fields["ksppstvl"] != fields["expected"] ) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }



        else if (fields["ksppinm"] == '_memory_imm_mode_without_autosga') {
            fields["expected"]  = 'FALSE'
            if (fields["ksppstvl"] != fields["expected"] ) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }



        // else if (fields["ksppinm"] == '_memory_imm_mode_without_autosga') {
        //     fields["expected"]  = 'TRUE'
        //     if (fields["ksppstvl"] != fields["expected"] ) {
        //         iseq = "不一致"
        //         result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
        //     } else {
        //         // mixlevel = "正常"
        //     }
        // }


        // else if (fields["ksppinm"] == '_olap_dimension_corehash_size') {
        //     fields["expected"]  = 'TRUE'
        //     if (fields["ksppstvl"] != fields["expected"] ) {
        //         iseq = "不一致"
        //         result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
        //     } else {
        //         // mixlevel = "正常"
        //     }
        // }



        else if (fields["ksppinm"] == '_resource_manager_always_off') {
            fields["expected"]  = 'TRUE'
            if (fields["ksppstvl"] != fields["expected"] ) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }



        else if (fields["ksppinm"] == '_report_capture_cycle_time') {
            fields["expected"]  = '0'
            if (fields["ksppstvl"] != fields["expected"] ) {
                iseq = "不一致"
                result.actual += fields["ksppinm"] + "预期为" + fields["expected"]  + ", 实际为" + fields["ksppstvl"]  + "; "
            } else {
                // mixlevel = "正常"
            }
        }


        fields["iseq"] = iseq
        fields["mixlevel"] = mixlevel
        result.mixraw.push(fields)
    }
    
    if (result.actual != ""){
        //result.level = "中风险"
    }

    results.push(result)
    return { results: results }

})(input)

