import {
    assistant_get,
    assistant_metric,
    assistant_update,
    list_shop_assistants,
    off_list_shop_assistants
} from "@/api/assistant-center";
import {
    assistant_choose,
    upload_avatar
} from "@/components/assistant/assistant_manage/assistant_manage";
import {ElMessage} from "element-plus";
import {nextTick, ref} from "vue";
import * as echarts from "echarts";

export const assistant_avg_time_Ref = ref(null)
export const assistant_cost_Ref = ref(null)
export const assistant_qa_Ref = ref(null)
export const assistant_user_Ref = ref(null)
export const assistant_speed_Ref = ref(null)
export const assistant_remark_Ref = ref(null)
export const assistant_metric_msg = ref(null)
export const assistant_metric_user = ref(null)
export const assistant_metric_response_time = ref(null)
export const assistant_metric_token_speed = ref(null)
export const assistant_metric_user_remark = ref(null)
export const assistant_metric_cost = ref(null)
export const monitor_time_range = ref(7)
export const current_publish_way = ref("NextConsole")

export async function reset_current_assistant() {
    let res = await assistant_get({
        "id": assistant_choose.id
    })
    if (!res.error_status) {
        Object.assign(assistant_choose, res.result);
        ElMessage.success({
            message: '重置成功!',
            type: 'success',
            duration: 600
        })
    }
}
export async function update_assistant_detail(){
    let res1 = await assistant_update(assistant_choose)
    await upload_avatar.value!.submit()
    if (!res1.error_status) {
        ElMessage.success({
            message: '保存成功!',
            type: 'success',
            duration: 600
        })
        let new_res = await assistant_get({
            "id": assistant_choose.id
        })
        Object.assign(assistant_choose, new_res.result);

    }
}

export async function publish_assistant(){
    let params = {
        "assistant_id": assistant_choose.id,
    }
    let res = await list_shop_assistants(params)
    if (!res.error_status) {
        assistant_choose.assistant_publish_shop_id = res.result.id
        ElMessage.success({
            message: '发布成功！',
            type: 'success',
            duration: 600
        })
    }
    await nextTick()
}

export async function unpublished_assistant(){
    let params = {
        "shop_assistant_id": assistant_choose.assistant_publish_shop_id,
    }
    let res = await off_list_shop_assistants(params)
    if (!res.error_status) {
        assistant_choose.assistant_publish_shop_id = null
        ElMessage.success({
            message: '下架成功！',
            type: 'success',
            duration: 600
        })
    }
    await nextTick()
}



export async function change_publish_way(way: string){
    current_publish_way.value = way
    if (way === 'NextConsole') {

    }
}
function formatter_time (time_str: number){
    let formatter = new Intl.DateTimeFormat('en-GB', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false, // 指定使用24小时制
        timeZone: 'Asia/Shanghai' // 设置时区为北京时区
    });
    return formatter.format(time_str).replace(/(\d{2})\/(\d{2})\/(\d{4}), /, '$3-$2-$1 ')
}
export async function get_assistant_metric_qa_accum() {
    if (!assistant_choose.id) {
        return
    }
    // 获取并更新数据

    let end_time = Date.now()
    let start_time = end_time - monitor_time_range.value * 24 * 60 * 60 * 1000
    let params = {
        "assistant_id": assistant_choose.id,
        "metric_name": "qa_counts",
        "end_time": formatter_time(end_time),
        "start_time": formatter_time(start_time),
    }
    let res = await assistant_metric(params)
    if (!res.error_status) {
        // 更新数据
        assistant_metric_msg.value = res.result.map(item => {
            return {
                date: new Date(item.value[0]),
                value: item.value
            };
        })

    }

}

export async function get_assistant_metric_user() {
    if (!assistant_choose.id) {
        return
    }
    let end_time = Date.now()
    let start_time = end_time - monitor_time_range.value * 24 * 60 * 60 * 1000
    let params = {
        "assistant_id": assistant_choose.id,
        "metric_name": "user_counts",
        "end_time": formatter_time(end_time),
        "start_time": formatter_time(start_time),
    }
    let res = await assistant_metric(params)
    let data = res.result.map(item => {
        return {
            date: new Date(item.value[0]),
            value: item.value
        };
    });
    if (!res.error_status) {
        // 更新数据
        assistant_metric_user.value = data
    }

}

export async function get_assistant_metric_response_time() {

    let end_time = Date.now()
    let start_time = end_time - monitor_time_range.value * 24 * 60 * 60 * 1000
    let params = {
        "assistant_id": assistant_choose.id,
        "metric_name": "avg_time",
        "end_time": formatter_time(end_time),
        "start_time": formatter_time(start_time),
    }
    let res = await assistant_metric(params)
    let data = res.result.map(item => {
        return {
            date: new Date(item.value[0]),
            value: item.value
        };
    });
    if (!res.error_status) {
        // 更新数据
        assistant_metric_response_time.value = data
    }

}

export async function get_assistant_metric_token_speed() {
    let end_time = Date.now()
    let start_time = end_time - monitor_time_range.value * 24 * 60 * 60 * 1000
    let params = {
        "assistant_id": assistant_choose.id,
        "metric_name": "token_speed",
        "end_time": formatter_time(end_time),
        "start_time": formatter_time(start_time),
    }
    let res = await assistant_metric(params)
    let data = res.result.map(item => {
        return {
            date: new Date(item.value[0]),
            value: item.value
        };
    });
    if (!res.error_status) {
        // 更新数据
        assistant_metric_token_speed.value = data
    }


}

export async function get_assistant_metric_user_remark() {

    let end_time = Date.now()
    let start_time = end_time - monitor_time_range.value * 24 * 60 * 60 * 1000
    let params = {
        "assistant_id": assistant_choose.id,
        "metric_name": "like_rate",
        "end_time": formatter_time(end_time),
        "start_time": formatter_time(start_time),
    }
    let res = await assistant_metric(params)

    if (!res.error_status) {
        // 更新数据
        assistant_metric_user_remark.value = res.result
    }

}

export async function get_assistant_metric_cost() {

    if (!assistant_choose.id) {
        return
    }
    // 获取并更新数据

    let end_time = Date.now()
    let start_time = end_time - monitor_time_range.value * 24 * 60 * 60 * 1000
    let params = {
        "assistant_id": assistant_choose.id,
        "metric_name": "cost",
        "end_time": formatter_time(end_time),
        "start_time": formatter_time(start_time),
    }
    let res = await assistant_metric(params)
    if (!res.error_status) {
        // 更新数据
        assistant_metric_cost.value = res.result.map(item => {
            return {
                date: new Date(item.value[0]),
                value: item.value
            };
        })

    }

}

export async function init_qa_chart(){
    await get_assistant_metric_qa_accum();
    const myChart = echarts.init(assistant_qa_Ref.value);
    const option = {
        title: {
            text: '累计问答数量',
            left: 'center'
        },
        xAxis: {
            type: 'time',
            splitLine: {
                show: true
            }
        },
        yAxis: {
            type: 'value',
            boundaryGap: [0, '100%'],
            splitLine: {
                show: false
            }
        },
        series: [{
            type: 'line',
            showSymbol: false,
            smooth: true,
            areaStyle: {},
            data: assistant_metric_msg.value
        }],
        tooltip: {
            trigger: 'axis',
            formatter: function (params) {
                let date = new Date(params[0].value[0]);
                const dateString = `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()} ${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`;
                return `${dateString}<br />问答数量: ${params[0].value[1]}`;

            },
            axisPointer: {
                animation: false
            }
        },
    };

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);

    assistant_qa_Ref.value = myChart;
}

export async function init_user_chart(){
    await get_assistant_metric_user();
    const myChart = echarts.init(assistant_user_Ref.value);
    const option = {
        title: {
            text: '每小时活跃用户数'
        },
        tooltip: {
            trigger: 'axis',
            formatter: function (params) {
                params = params[0];
                const date = new Date(params.value[0]);
                const dateString = `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()} ${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`;
                return `${dateString} : ${params.value[1]} 用户`;
            }
        },
        xAxis: {
            type: 'time',
            splitLine: {
                show: false
            }
        },
        yAxis: {
            type: 'value',
            splitLine: {
                show: false
            }
        },
        series: [{
            data: assistant_metric_user.value,
            type: 'line',
            areaStyle: {}
        }]
    };
    myChart.setOption(option);
    assistant_user_Ref.value = myChart;
}

export async function init_response_time_chart(){
    await get_assistant_metric_response_time();
    const myChart = echarts.init(assistant_avg_time_Ref.value);
    // 指定图表的配置项和数据
    const option = {
        title: {
            text: '平均响应时间'
        },
        tooltip: {
            trigger: 'item',
            axisPointer: {
                type: 'cross'
            },
            formatter: function (params) {
                const date = new Date(params.value[0]);
                const dateStr = `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()} ${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`;
                return `${dateStr} : ${params.value[1]} 秒`;
            }
        },
        xAxis: {
            type: 'time',
            splitLine: {
                show: false
            }
        },
        yAxis: {
            type: 'value',
            splitLine: {
                show: false
            },
            scale: true,
            name: '响应时间(秒)'
        },
        series: [{
            type: 'scatter',
            symbolSize: 10,
            data: assistant_metric_response_time.value
        }]
    };

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
    assistant_avg_time_Ref.value = myChart;
}

export async function init_speed_chart(){
    await get_assistant_metric_token_speed();
    const myChart = echarts.init(assistant_speed_Ref.value);
    // 指定图表的配置项和数据
    // 指定图表的配置项和数据
    const option = {
        title: {
            text: 'Token输出速度'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            },
            formatter: function (params) {
                const date = new Date(params[0].value[0]);
                const dateStr = `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()} ${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`;
                return `${dateStr} : ${params[0].value[1]} 个Token`;
            }
        },
        xAxis: {
            type: 'time',

            axisLabel: {
                interval: 0,
                rotate: 45 // 如果标签过多，可以选择旋转标签以改善显示效果
            }
        },
        yAxis: {
            type: 'value'
        },
        series: [{
            data: assistant_metric_token_speed.value,
            type: 'bar'
        }]
    };
    myChart.setOption(option);
    assistant_speed_Ref.value = myChart;
}

export async function init_remark_chart(){
    await get_assistant_metric_user_remark();
    const myChart = echarts.init(assistant_remark_Ref.value);
    // 指定图表的配置项和数据
    const option = {
        title: {
            text: '用户满意度',
            left: 'center'
        },
        tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        legend: {
            orient: 'vertical',
            left: 'left',
            data: ['用户点赞', '用户点踩', '用户未评论']
        },
        series: [
            {
                name: '满意度',
                type: 'pie',
                radius: '55%',
                center: ['50%', '60%'],
                data: assistant_metric_user_remark.value,
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    };

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
    assistant_remark_Ref.value = myChart;
}

export async function init_cost_chart(){
    await get_assistant_metric_cost();
    const myChart = echarts.init(assistant_cost_Ref.value);
    // 指定图表的配置项和数据
    const option = {
        title: {
            text: '费用消耗',
            left: 'center'
        },
        tooltip: {
            trigger: 'axis',
            formatter: function (params) {
                let date = new Date(params[0].value[0]);
                const dateString = `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()} ${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`;
                return `${dateString}<br />费用: ${params[0].value[1]}元`;
            },
            axisPointer: {
                animation: false
            }
        },
        xAxis: {
            type: 'time',
            splitLine: {
                show: false
            }
        },
        yAxis: {
            type: 'value',
            boundaryGap: [0, '100%'],
            splitLine: {
                show: false
            }
        },
        series: [{
            type: 'line',
            showSymbol: false,
            smooth: true,
            areaStyle: {},
            data: assistant_metric_cost.value
        }]
    };

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);

    assistant_cost_Ref.value = myChart;
}


export async function init_metric_chart(){
    init_qa_chart();
    init_user_chart();
    init_response_time_chart();
    init_speed_chart();
    init_remark_chart();
    init_cost_chart();
}
