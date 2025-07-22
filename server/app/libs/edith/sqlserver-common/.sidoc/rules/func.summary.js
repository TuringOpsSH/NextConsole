; (function (params) {

    config = {
        date: $.ymd(),
        group: "host",
        debug: "no",

        show_document_version_information: "yes", // 文档版本信息
        show_summary_of_check: "yes", // 巡检结果汇总
        show_important_and_handling_plan: "yes", // 重要告警及处理计划

        show_count_of_risks: "yes", // 告警数量统计
        show_count_of_risks_with_score: "yes", // 在 show_count_of_risks 中显示健康度
        show_count_of_risks_orderby_score: "yes", // 告警数量统计, 健康度从高至低
        show_piechart: "yes", // 告警数量统计饼图

        show_list_of_risks_danger: "yes", // 高风险
        show_list_of_risks_warning: "yes", // 中风险
        show_list_of_risks_green: "yes", // 低风险
        show_list_of_risks_ok: "yes", // 正常

        show_list_of_risks_group_by_category: "no", // 风险及建议（按告警分类）
        show_list_of_risks_group_by_category_order: ["OS 检查", "Docker 检查", "K8s 检查"],

        show_check_item_list: "yes" // 双栏检查项列表
    }

    try {
        return $.summary(params[0], config)
    } catch (err) {
        $.print("Summary err", err.message)
    }

})(input)