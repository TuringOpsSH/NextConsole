import {reactive, ref} from "vue";
import {get_all_company, get_dashboard_index} from "@/api/dashboard";
import gsap from 'gsap'
import {format, parseISO} from "date-fns";
import * as echarts from "echarts";
import {Company} from "@/types/contacts";
export const selectedTimeRange = ref('month');
export const refreshRate = ref(600000);
export const refreshInterval = ref(null);
export const targetCompany = ref('')
export const user_company_list = ref<Company[]>([])
export const index_begin_time = ref()





export async function search_all_company_option(){
    let params = {}
    let res = await get_all_company(params)
    if (!res.error_status){
        user_company_list.value = res.result
    }
}
export function transTimeRange(){
    //根据selectedTimeRange计算index_begin_time，end_begin_time
    if (!selectedTimeRange.value){
        index_begin_time.value = null
        return
    }
    const start = new Date()
    if (selectedTimeRange.value==='today'){
        start.setHours(0, 0, 0, 0);
    }
    else if (selectedTimeRange.value==='week'){
        start.setTime(start.getTime() - 3600 * 1000 * 24 * 7 )
    }
    else if (selectedTimeRange.value==='month'){
        start.setTime(start.getTime() - 3600 * 1000 * 24 * 31)
    }
    else if (selectedTimeRange.value==='quarter'){
        start.setTime(start.getTime() - 3600 * 1000 * 24 * 7 * 31 * 4)
    }
    else if (selectedTimeRange.value==='year'){
        start.setTime(start.getTime() - 3600 * 1000 * 24 * 7 * 365)
    }

    index_begin_time.value = format(parseISO(start.toISOString()), 'yyyy-MM-dd HH:mm:ss')
}
export async function changeRefreshRate(){
    if (refreshInterval.value) {
        clearInterval(refreshInterval.value);
    }
    if (refreshRate.value !== 0) {
        refreshInterval.value = setInterval(async () => {
            await get_all_data();
        }, refreshRate.value);
    }
}

export async function get_all_data(){
    transTimeRange()
    get_dnu()
    get_dnu_sd()
    get_all_cvr()
    get_new_cvr()
    get_uv_cnt_data()
    get_d1_retention()
    get_all_retention()


    get_uv_hour_data()
    get_uv_day_data()
    get_avg_qa_retention()
    get_qa_cnt_data()
    get_qa_hour_data()
    get_qa_day_data()

    get_avg_session_retention()
    get_session_cnt_data()
    get_session_hour_data()
    get_session_day_data()


    // 资源库
    get_doc_read_count_data()
    get_doc_view_top_data()
    get_user_view_resource_top_data()
    get_doc_download_count_data()
    get_doc_download_top_data()
    get_user_download_top_data()

}



export const uv_count = ref(0)
export const uv_count_tweened = reactive({number: 0})
export async function get_uv_cnt_data() {
    let params = {
        index_name : "uv",
        begin_time :index_begin_time.value,
        top:'',
        company_id:targetCompany.value
    }
    let res = await get_dashboard_index(params)
    if (!res.error_status){
        uv_count.value = res.result.uv
    }
    gsap.to(uv_count_tweened, { duration: 0.5, number: uv_count.value })
};


export const uv_hour_x = ref([])
export const uv_hour_series = ref([])
export const uv_hour_option = ref({
    title: {
        text: "每小时问答用户数"
    },
    tooltip: {
        trigger: "axis"
    },
    xAxis: {
        type: "category",
        data: uv_hour_x.value,
        axisLabel: {
            formatter: function (value) {
                return value.substring(0, 13); // 显示到小时
            },
            rotate: 45,  // 标签旋转45度以防止重叠

        },
    },
    yAxis: {
        type: "value"
    },
    series: [
        {
            data: uv_hour_series.value,
            type: 'line',
            smooth: true
        }
    ],
    toolbox: {
        show: true,
        feature: {
            dataView: { readOnly: false },
            magicType: { type: ['line', 'bar'] },
            
            saveAsImage: {}
        }
    },
})
let uv_hour_chart = null;
export async function get_uv_hour_data(){
    let params = {
        index_name : "uv_hour",
        begin_time : index_begin_time.value,
        top:'',
        company_id:targetCompany.value
    }
    let res = await get_dashboard_index(params)
    if (!res.error_status){
        uv_hour_x.value.length=0
        uv_hour_series.value.length=0
        for (let item of res.result.uv_hour) {
            uv_hour_x.value.push (item.hour)
            uv_hour_series.value.push(item.unique_user_count)
        }
        if (!uv_hour_chart && document.getElementById('uv_hour')){
            uv_hour_chart = echarts.init(
                document.getElementById('uv_hour'), null, {width: 600, height: 400}
            )
        }
        uv_hour_chart?.setOption(uv_hour_option.value)
    }

}


export const uv_day_x = ref([])
export const uv_day_series = ref([])
export const uv_day_option = ref({
    title: {
        text: "每天问答用户数"
    },
    tooltip: {
        trigger: "axis"
    },
    xAxis: {
        type: "category",
        data: uv_day_x.value,
        axisLabel: {
            formatter: function (value) {
                return value.substring(0, 10); // 显示到小时
            },
            rotate: 45,  // 标签旋转45度以防止重叠

        },
    },
    yAxis: {
        type: "value"
    },
    series: [
        {
            data: uv_day_series.value,
            type: 'line',
            smooth: true
        }
    ],
    toolbox: {
        show: true,
        feature: {
            dataView: { readOnly: false },
            magicType: { type: ['line', 'bar'] },
            
            saveAsImage: {}
        }
    },
})
let uv_day_chart = null;
export async function get_uv_day_data(){
    
    let params = {
        index_name : "uv_day",
        begin_time : index_begin_time.value,
        top:'',
        company_id:targetCompany.value
    }
    let res = await get_dashboard_index(params)
    if (!res.error_status){

        uv_day_x.value.length=0
        uv_day_series.value.length=0
        for (let item of res.result.uv_day) {
            uv_day_x.value.push (item.day)
            uv_day_series.value.push(item.unique_user_count)
        }
        if (!uv_day_chart && document.getElementById('uv_day')){
            uv_day_chart = echarts.init(document.getElementById('uv_day'), null,
                {width: 600, height: 400})
        }
        uv_day_chart?.setOption(uv_day_option.value)
    }
}

export const qa_count = ref(0)
export const qa_count_tweened = reactive({ number: 0})
export async function get_qa_cnt_data() {
    let params = {
        index_name : "qa",
        begin_time :index_begin_time.value,
        top:'',
        company_id:targetCompany.value
    }
    let res = await get_dashboard_index(params)
    if (!res.error_status){
        qa_count.value = res.result.qa
    }
    gsap.to(qa_count_tweened, { duration: 0.5, number: qa_count.value })
}

export const qa_hour_x = ref([])
export const qa_hour_series = ref([])
export const qa_hour_option = ref({
    title: {
        text: "每小时新增提问数"
    },
    tooltip: {
        trigger: "axis"
    },
    xAxis: {
        type: "category",
        data: qa_hour_x.value,
        axisLabel: {
            formatter: function (value) {
                return value.substring(0, 13); // 显示到小时
            },
            rotate: 45,  // 标签旋转45度以防止重叠

        },
    },
    yAxis: {
        type: "value"
    },
    series: [
        {
            data: qa_hour_series.value,
            type: 'line',
            smooth: true
        }
    ],
    toolbox: {
        show: true,
        feature: {
            dataView: { readOnly: false },
            magicType: { type: ['line', 'bar'] },
            
            saveAsImage: {}
        }
    },
})
let qa_hour_chart = null;
export async function get_qa_hour_data(){
    let params = {
        index_name : "qa_hour",
        begin_time : index_begin_time.value,
        top:'',
        company_id:targetCompany.value
    }
    let res = await get_dashboard_index(params)
    if (!res.error_status){
        qa_hour_x.value.length=0
        qa_hour_series.value.length=0
        for (let item of res.result.qa_hour) {
            qa_hour_x.value.push (item.hour)
            qa_hour_series.value.push(item.unique_qa_count)
        }
        if (!qa_hour_chart && document.getElementById('qa_hour')){
            qa_hour_chart = echarts.init(document.getElementById('qa_hour'), null,
                {width: 600, height: 400})
        }
        qa_hour_chart?.setOption(qa_hour_option.value)
    }

}

export const qa_day_x = ref([])
export const qa_day_series = ref([])
export const qa_day_option = ref({
    title: {
        text: "每天新增提问数"
    },
    tooltip: {
        trigger: "axis"
    },
    xAxis: {
        type: "category",
        data: qa_day_x.value,
        axisLabel: {
            formatter: function (value) {
                return value.substring(0, 10); // 显示到小时
            },
            rotate: 45,  // 标签旋转45度以防止重叠

        },
    },
    yAxis: {
        type: "value"
    },
    series: [
        {
            data: qa_day_series.value,
            type: 'line',
            smooth: true
        }
    ],
    toolbox: {
        show: true,
        feature: {
            dataView: { readOnly: false },
            magicType: { type: ['line', 'bar'] },
            
            saveAsImage: {}
        }
    },
})
let qa_day_chart = null;
export async function get_qa_day_data(){
    
    let params = {
        index_name : "qa_day",
        begin_time : index_begin_time.value,
        top:'',
        company_id:targetCompany.value
    }
    let res = await get_dashboard_index(params)
    if (!res.error_status){
        qa_day_x.value.length=0
        qa_day_series.value.length=0
        for (let item of res.result.qa_day) {
            qa_day_x.value.push (item.day)
            qa_day_series.value.push(item.unique_qa_count)
        }
        if (!qa_day_chart && document.getElementById('qa_day')){
            qa_day_chart = echarts.init(document.getElementById('qa_day'), null,
                {width: 600, height: 400})
        }
        qa_day_chart?.setOption(qa_day_option.value)
    }
}

export const session_count = ref(0)
export const session_count_tweened = reactive({number: 0})
export async function get_session_cnt_data() {
    let params = {
        index_name : "session",
        begin_time :index_begin_time.value,
        top:'',
        company_id:targetCompany.value
    }
    let res = await get_dashboard_index(params)
    if (!res.error_status){
        session_count.value = res.result.session
    }
    gsap.to(session_count_tweened, { duration: 0.5, number: session_count.value })
};

export const session_hour_x = ref([])
export const session_hour_series = ref([])
export const session_hour_option = ref({
    title: {
        text: "每小时新增会话数"
    },
    tooltip: {
        trigger: "axis"
    },
    xAxis: {
        type: "category",
        data: session_hour_x.value,
        axisLabel: {
            formatter: function (value) {
                return value.substring(0, 13); // 显示到小时
            },
            rotate: 45,  // 标签旋转45度以防止重叠

        },
    },
    yAxis: {
        type: "value"
    },
    series: [
        {
            data: session_hour_series.value,
            type: 'line',
            smooth: true
        }
    ],
    toolbox: {
        show: true,
        feature: {
            dataView: { readOnly: false },
            magicType: { type: ['line', 'bar'] },
            
            saveAsImage: {}
        }
    },
})
let session_hour_chart = null;
export async function get_session_hour_data(){
    let params = {
        index_name : "session_hour",
        begin_time : index_begin_time.value,
        top:'',
        company_id:targetCompany.value
    }
    let res = await get_dashboard_index(params)
    if (!res.error_status){
        session_hour_x.value.length=0
        session_hour_series.value.length=0
        for (let item of res.result.session_hour) {
            session_hour_x.value.push (item.hour)
            session_hour_series.value.push(item.unique_session_count)
        }
        if (!session_hour_chart && document.getElementById('session_hour')){
            session_hour_chart = echarts.init(
                document.getElementById('session_hour'), null, {width: 600, height: 400})
        }
        session_hour_chart?.setOption(session_hour_option.value)

    }

}

export const session_day_x = ref([])
export const session_day_series = ref([])
export const session_day_option = ref({
    title: {
        text: "每天新增会话数"
    },
    tooltip: {
        trigger: "axis"
    },
    xAxis: {
        type: "category",
        data: session_day_x.value,
        axisLabel: {
            formatter: function (value) {
                return value.substring(0, 10); // 显示到小时
            },
            rotate: 45,  // 标签旋转45度以防止重叠

        },
    },
    yAxis: {
        type: "value"
    },
    series: [
        {
            data: session_day_series.value,
            type: 'line',
            smooth: true
        }
    ],
    toolbox: {
        show: true,
        feature: {
            dataView: { readOnly: false },
            magicType: { type: ['line', 'bar'] },
            
            saveAsImage: {}
        }
    },
})
let session_day_chart = null;
export async function get_session_day_data(){
    
    let params = {
        index_name : "session_day",
        begin_time : index_begin_time.value,
        top:'',
        company_id:targetCompany.value
    }
    let res = await get_dashboard_index(params)
    if (!res.error_status){
        session_day_x.value.length=0
        session_day_series.value.length=0
        for (let item of res.result.session_day) {
            session_day_x.value.push (item.day)
            session_day_series.value.push(item.unique_session_count)
        }
        if (!session_day_chart && document.getElementById('session_day')){
            session_day_chart = echarts.init(
                document.getElementById('session_day'), null, {width: 600, height: 400})
        }
        session_day_chart?.setOption(session_day_option.value)

    }

}


export const doc_read_count = ref(0)
export const doc_read_count_tweened = reactive({number: 0})
export async function  get_doc_read_count_data(){
    let params = {
        index_name : "doc_read_count",
        begin_time :index_begin_time.value,
        top:'',
        company_id:targetCompany.value
    }
    let res = await get_dashboard_index(params)
    if (!res.error_status){
        doc_read_count.value = res.result.doc_read_count
    }
    gsap.to(doc_read_count_tweened, { duration: 0.5, number: doc_read_count.value })
}



export const doc_download_count = ref(0)
export const doc_download_count_tweened = reactive({number: 0})
export async function  get_doc_download_count_data(){
    let params = {
        index_name : "doc_download_count",
        begin_time :index_begin_time.value,
        top:'',
        company_id:targetCompany.value
    }
    let res = await get_dashboard_index(params)
    if (!res.error_status){
        doc_download_count.value = res.result.doc_download_count
    }
    gsap.to(doc_download_count_tweened, { duration: 0.5, number: doc_download_count.value })
}

export const doc_view_top_y = ref([])
export const doc_view_top_series = ref([])
export const doc_view_top_option = ref({
    title: {
        text: "文档阅读排行"
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis: {
        type: 'value',
        boundaryGap: [0, 0.01]
    },
    yAxis: {
        type: 'category',
        data:  doc_view_top_y.value

    },
    series: [
        {
            data: doc_view_top_series.value,
            type: 'bar'
        }
    ],
    toolbox: {
        show: true,
        feature: {
            dataView: { readOnly: false },
            magicType: { type: ['line', 'bar'] },
            
            saveAsImage: {}
        }
    },
})
let doc_view_top_chart = null;
export async function  get_doc_view_top_data(){


    let params = {
        index_name : "doc_view_top",
        begin_time : index_begin_time.value,
        top:'',
        company_id:targetCompany.value
    }
    let res = await get_dashboard_index(params)
    if (!res.error_status){
        doc_view_top_y.value.length=0
        doc_view_top_series.value.length=0
        for (let item of res.result.doc_view_top) {
            doc_view_top_y.value.push (item.resource_name)
            doc_view_top_series.value.push( item.view_count)
        }
        if (!doc_view_top_chart && document.getElementById('doc_view_top')){
            doc_view_top_chart = echarts.init(
                document.getElementById('doc_view_top'), null, {width: 600, height: 400})
        }
        doc_view_top_chart?.setOption(doc_view_top_option.value)

    }
}


export const doc_download_top_y = ref([])
export const doc_download_top_series = ref([])
export const doc_download_top_option = ref({
    title: {
        text: "文档下载排行"
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis: {
        type: 'value',
        boundaryGap: [0, 0.01]
    },
    yAxis: {
        type: 'category',
        data:  doc_download_top_y.value

    },
    series: [
        {
            data: doc_download_top_series.value,
            type: 'bar'
        }
    ],
    toolbox: {
        show: true,
        feature: {
            dataView: { readOnly: false },
            magicType: { type: ['line', 'bar'] },
            
            saveAsImage: {}
        }
    },
})
let doc_download_top_chart = null;
export async function  get_doc_download_top_data(){


    let params = {
        index_name : "doc_download_top",
        begin_time : index_begin_time.value,
        top:'',
        company_id:targetCompany.value
    }
    let res = await get_dashboard_index(params)
    if (!res.error_status){
        doc_download_top_y.value.length=0
        doc_download_top_series.value.length=0
        for (let item of res.result.doc_download_top) {
            doc_download_top_y.value.push (item.resource_name)
            doc_download_top_series.value.push( item.download_count)
        }
        if (!doc_download_top_chart && document.getElementById('doc_download_top')){
            doc_download_top_chart = echarts.init(
                document.getElementById('doc_download_top'), null, {width: 600, height: 400})
        }
        doc_download_top_chart?.setOption(doc_download_top_option.value)

    }
}

export const user_view_resource_top_y = ref([])
export const user_view_resource_series = ref([])
export const user_view_resource_option = ref({
    title: {
        text: "用户阅读排行"
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis: {
        type: 'value',
        boundaryGap: [0, 0.01]
    },
    yAxis: {
        type: 'category',
        data:  user_view_resource_top_y.value

    },
    series: [
        {
            data: user_view_resource_series.value,
            type: 'bar'
        }
    ],
    toolbox: {
        show: true,
        feature: {
            dataView: { readOnly: false },
            magicType: { type: ['line', 'bar'] },
            
            saveAsImage: {}
        }
    },
})
let user_view_resource_chart = null;

export async function  get_user_view_resource_top_data(){


    let params = {
        index_name : "user_view_resource_top",
        begin_time : index_begin_time.value,
        top:'',
        company_id:targetCompany.value
    }
    let res = await get_dashboard_index(params)
    if (!res.error_status){
        user_view_resource_top_y.value.length=0
        user_view_resource_series.value.length=0
        for (let item of res.result.user_view_resource_top) {
            user_view_resource_top_y.value.push (item.user_id + ":" + item.user_name)
            user_view_resource_series.value.push( item.view_count)
        }
        if (!user_view_resource_chart && document.getElementById('user_view_resource_top')){
            user_view_resource_chart = echarts.init(
                document.getElementById('user_view_resource_top'), null, {width: 600, height: 400})
        }
        user_view_resource_chart?.setOption(user_view_resource_option.value)

    }
}



export const user_download_top_y = ref([])
export const user_download_top_series = ref([])
export const user_download_top_option = ref({
    title: {
        text: "用户下载排行"
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis: {
        type: 'value',
        boundaryGap: [0, 0.01]
    },
    yAxis: {
        type: 'category',
        data:  user_download_top_y.value

    },
    series: [
        {
            data: user_download_top_series.value,
            type: 'bar'
        }
    ],
    toolbox: {
        show: true,
        feature: {
            dataView: { readOnly: false },
            magicType: { type: ['line', 'bar'] },
            
            saveAsImage: {}
        }
    },
})
let user_download_top_chart = null;

export async function  get_user_download_top_data(){


    let params = {
        index_name : "user_download_top",
        begin_time : index_begin_time.value,
        top:'',
        company_id:targetCompany.value
    }
    let res = await get_dashboard_index(params)
    if (!res.error_status){
        user_download_top_y.value.length=0
        user_download_top_series.value.length=0
        for (let item of res.result.user_download_top) {
            user_download_top_y.value.push (item.user_id + ":" + item.user_name)
            user_download_top_series.value.push( item.download_count)
        }
        if (!user_download_top_chart && document.getElementById('user_download_top')){
            user_download_top_chart = echarts.init(
                document.getElementById('user_download_top'), null, {width: 600, height: 400})
        }
        user_download_top_chart?.setOption(user_download_top_option.value)

    }
}

// 新增报表
export const dnu_x = ref([])
export const dnu_series = ref([])
export const dnu_option = ref({
    title: {
        text: "每日新增注册用户数"
    },
    tooltip: {
        trigger: "axis"
    },
    xAxis: {
        type: "category",
        data: dnu_x.value,
        axisLabel: {
            formatter: function (value) {
                return value.substring(0, 10); // 显示到小时
            },
            rotate: 45,  // 标签旋转45度以防止重叠

        },
    },
    yAxis: {
        type: "value"
    },
    series: [
        {
            data: dnu_series.value,
            type: 'line',
            smooth: true,
            name: '新增用户数'
        }
    ],
    toolbox: {
        show: true,
        feature: {
            dataView: { readOnly: false },
            magicType: { type: ['line', 'bar'] },
            
            saveAsImage: {}
        }
    },
})
let dnu_chart = null;
export async function get_dnu(){
    let params = {
        index_name : "dnu",
        begin_time : index_begin_time.value,
        top:'',
        company_id:targetCompany.value
    }
    let res = await get_dashboard_index(params)
    if (!res.error_status){
        dnu_x.value.length=0
        dnu_series.value.length=0
        for (let item of res.result.dnu) {
            dnu_x.value.push (item.day)
            dnu_series.value.push(item.dnu)
        }
        if (!dnu_chart && document.getElementById('dnu')){
            dnu_chart = echarts.init(
                document.getElementById('dnu'), null, {width: 600, height: 400})
        }
        dnu_chart?.setOption(dnu_option.value)

    }
}

let dnu_sd_chart = null
export const dnu_sd_option = ref({
    title: {
        text: "每日新增用户来源渠道"
    },
    tooltip: {
        trigger: "axis",
        showContent: false
    },
    legend:{
        data: [ '营销推荐' , '官网注册', '用户推荐', '未知渠道']
    },
    dataset: {
        source: []
    },
    xAxis: { type: 'category',axisLabel: {
            formatter: function (value) {
                return value.substring(0, 10); // 显示到小时
            },
            rotate: 45,  // 标签旋转45度以防止重叠

        }, },
    yAxis: { gridIndex: 0 },
    grid: { top: '55%' },
    series: [
        {
            name: '营销推荐',
            type: 'line',
            smooth: true,
            seriesLayoutBy: 'row',
            emphasis: { focus: 'series' }
        },
        {
            name: '官网注册',
            type: 'line',
            smooth: true,
            seriesLayoutBy: 'row',
            emphasis: { focus: 'series' }
        },
        {
            name: '用户推荐',
            type: 'line',
            smooth: true,
            seriesLayoutBy: 'row',
            emphasis: { focus: 'series' }
        },
        {
            name: '未知渠道',
            type: 'line',
            smooth: true,
            seriesLayoutBy: 'row',
            emphasis: { focus: 'series' }
        },
        {
            type: 'pie',
            id: 'pie',
            radius: '30%',
            center: ['50%', '25%'],
            emphasis: {
                focus: 'self'
            },
            label: {
                formatter: '{b}: {@[1]} ({d}%)'
            },
            encode: {
                itemName: 'source_channel',
                value: '1',
                tooltip: '1'
            }
        }
    ],

})
export async function get_dnu_sd(){
    let params = {
        index_name : "dnu_sd",
        begin_time : index_begin_time.value,
        top:'',
        company_id:targetCompany.value
    }
    let res = await get_dashboard_index(params)
    if (!res.error_status){
        dnu_sd_option.value.dataset.source = res.result.dnu_sd
    }
    if( !dnu_sd_chart && document.getElementById('dnu_sd')){
        dnu_sd_chart = echarts.init(
            document.getElementById('dnu_sd'), null,
            {width: 800, height:600}
        );
    }

    dnu_sd_chart?.on('updateAxisPointer', function (event:any) {
        const xAxisInfo = event.axesInfo[0];
        if (xAxisInfo) {
            const dimension = xAxisInfo.value + 1;
            dnu_sd_chart?.setOption({
                series: {
                    id: 'pie',
                    label: {
                        formatter: '{b}: {@[' + dimension + ']} ({d}%)'
                    },

                    encode: {
                        value: dimension,
                        tooltip: dimension
                    }
                }
            });
        }
    });
    dnu_sd_chart?.setOption(dnu_sd_option.value);
}

let all_cvr_chart = null;
export const all_cvr_option = ref({
    title: {
        text: "整体转化率"
    },
    tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b} : {c}%'
    },
    toolbox: {
        feature: {
            dataView: { readOnly: false },
            
            saveAsImage: {}
        }
    },
    legend: {
        data: ['所有注册用户', 'AI工作台', '帮助工单', '在线支持', '资源库', '全部使用']
    },
    series: [
        {
            name: '用户转化率',
            type: 'funnel',
            left: '10%',
            top: 60,
            bottom: 60,
            width: '80%',
            min: 0,
            max: 100,
            minSize: '0%',
            maxSize: '100%',
            sort: 'descending',
            gap: 2,
            label: {
                show: true,
                position: 'inside'
            },
            labelLine: {
                length: 10,
                lineStyle: {
                    width: 1,
                    type: 'solid'
                }
            },
            itemStyle: {
                borderColor: '#fff',
                borderWidth: 1
            },
            emphasis: {
                label: {
                    fontSize: 20
                }
            },
            data: [
                { value: 60, name: '所有注册用户' },
                { value: 40, name: 'AI工作台' },
                { value: 20, name: '帮助工单' },
                { value: 80, name: '在线支持' },
                { value: 100, name: '资源库' },
                { value: 100, name: '全部使用' },
            ]
        }
    ],

})
export async function get_all_cvr(){
    let params = {
        index_name : "all_cvr",
        begin_time : index_begin_time.value,
        top:'',
        company_id:targetCompany.value,
    }
    let res = await get_dashboard_index(params)
    if (!res.error_status){
        all_cvr_option.value.series[0].data = res.result.all_cvr
    }
    if( !all_cvr_chart && document.getElementById('all_cvr')){
        all_cvr_chart = echarts.init(
            document.getElementById('all_cvr'), null,
            {width: 800, height:400}
        );
    }
    all_cvr_chart?.setOption(all_cvr_option.value);
}

let new_cvr_chart = null;
export const new_cvr_option = ref({
    title: {
        text: "新增转化率"
    },
    tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b} : {c}%'
    },
    toolbox: {
        feature: {
            dataView: { readOnly: false },
            
            saveAsImage: {}
        }
    },
    legend: {
        data: ['所有注册用户', 'AI工作台', '帮助工单', '在线支持', '资源库', '全部使用']
    },
    series: [
        {
            name: '用户转化率',
            type: 'funnel',
            left: '10%',
            top: 60,
            bottom: 60,
            width: '80%',
            min: 0,
            max: 100,
            minSize: '0%',
            maxSize: '100%',
            sort: 'descending',
            gap: 2,
            label: {
                show: true,
                position: 'inside'
            },
            labelLine: {
                length: 10,
                lineStyle: {
                    width: 1,
                    type: 'solid'
                }
            },
            itemStyle: {
                borderColor: '#fff',
                borderWidth: 1
            },
            emphasis: {
                label: {
                    fontSize: 20
                }
            },
            data: [
                { value: 60, name: '所有注册用户' },
                { value: 40, name: 'AI工作台' },
                { value: 20, name: '帮助工单' },
                { value: 80, name: '在线支持' },
                { value: 100, name: '资源库' },
                { value: 100, name: '全部使用' },
            ]
        }
    ],
})
export async function get_new_cvr(){
    let params = {
        index_name : "new_cvr",
        begin_time : index_begin_time.value,
        top:'',
        company_id:targetCompany.value,
    }
    let res = await get_dashboard_index(params)
    if (!res.error_status){
        new_cvr_option.value.series[0].data = res.result.new_cvr
    }
    if( !new_cvr_chart && document.getElementById('new_cvr')){
        new_cvr_chart = echarts.init(
            document.getElementById('new_cvr'), null,
            {width: 800, height:400}
        );
    }
    new_cvr_chart?.setOption(new_cvr_option.value);
}

let d1_retention_chart = null;
export const d1_retention_series = ref([])
export const d1_new_users_series = ref([])
export const d1_retention_option = ref({
    title: {
        text: "新增用户一日留存"
    },
    tooltip: {
        trigger: "axis"
    },
    legend:{
        data:['一日后留存用户','当日新增用户',]
    },
    xAxis: {
        type: "category",
        data: dnu_x.value,
        axisLabel: {
            formatter: function (value) {
                return value.substring(0, 10); // 显示到小时
            },
            rotate: 45,  // 标签旋转45度以防止重叠

        },
    },
    yAxis: {
        type: "value"
    },
    series: [
        {
            data: d1_retention_series.value,
            type: 'line',
            smooth: true,
            name: '一日后留存用户'
        },
        {
            data: d1_new_users_series.value,
            type: 'line',
            smooth: true,
            name: '当日新增用户'
        },

    ],
    toolbox: {
        show: true,
        feature: {
            dataView: { readOnly: false },
            magicType: { type: ['line', 'bar'] },
            
            saveAsImage: {}
        }
    },
})
export async function get_d1_retention(){
    let params = {
        index_name : "d1_retention",
        begin_time : index_begin_time.value,
        top:'',
        company_id:targetCompany.value,
    }
    let res = await get_dashboard_index(params)
    if (!res.error_status){
        d1_retention_series.value.length=0
        d1_new_users_series.value.length=0
        for (let item of res.result.d1_retention) {
            d1_retention_series.value.push(item.d1_retention)
            d1_new_users_series.value.push(item.user_cnt)
        }
    }
    if( !d1_retention_chart && document.getElementById('d1_retention')){
        d1_retention_chart = echarts.init(
            document.getElementById('d1_retention'), null,
            {width: 800, height:400}
        );
    }
    d1_retention_chart?.setOption(d1_retention_option.value);
}

let total_retention_chart = null;
export const total_retention_x = ref([])
export const active_user_series = ref([])
export const d7_retention_series = ref([])
export const d15_retention_series = ref([])
export const d30_retention_series = ref([])
export const all_retention_option = ref(
    {
        title: {
            text: "新增用户留存"
        },
        tooltip: {
            trigger: "axis"
        },
        legend:{
            data:['当日活跃用户','7日留存用户','15日留存用户','30日留存用户']
        },
        xAxis: {
            type: "category",
            data: total_retention_x.value,
            axisLabel: {
                formatter: function (value) {
                    return value.substring(0, 13);
                },
                rotate: 45,
            },
        },
        yAxis: {
            type: "value"
        },
        series: [
            {
                data: active_user_series.value,
                type: 'line',
                smooth: true,
                name: '当日活跃用户'
            },
            {
                data: d7_retention_series.value,
                type: 'line',
                smooth: true,
                name: '7日留存用户'
            },
            {
                data: d15_retention_series.value,
                type: 'line',
                smooth: true,
                name: '15日留存用户'
            },
            {
                data: d30_retention_series.value,
                type: 'line',
                smooth: true,
                name: '30日留存用户'
            }

        ],
        toolbox: {
            show: true,
            feature: {
                dataView: { readOnly: false },
                magicType: { type: ['line', 'bar'] },
                
                saveAsImage: {}
            }
        },
    }
)
export async function get_all_retention(){
    let params = {
        index_name : "all_retention",
        begin_time : index_begin_time.value,
        top:'',
        company_id:targetCompany.value,
    }
    let res = await get_dashboard_index(params)
    if (!res.error_status){
        total_retention_x.value.length=0
        active_user_series.value.length=0
        for (let item of res.result.all_retention.active_user_series) {
            total_retention_x.value.push(item.day)
            active_user_series.value.push(item.active_user_count)
        }
        d7_retention_series.value.length=0
        for (let item of res.result.all_retention.retention_7) {
            d7_retention_series.value.push(item)
        }
        d15_retention_series.value.length=0
        for (let item of res.result.all_retention.retention_15) {
            d15_retention_series.value.push(item)
        }
        d30_retention_series.value.length=0
        for (let item of res.result.all_retention.retention_30) {
            d30_retention_series.value.push(item)
        }
    }
    if( !total_retention_chart && document.getElementById('all_retention')){
        total_retention_chart = echarts.init(
            document.getElementById('all_retention'), null,
            {width: 800, height:400}
        );
    }
    total_retention_chart?.setOption(all_retention_option.value);
}

let avg_qa_retention_chart = null;
export const avg_qa_retention_x = ref([])
export const avg_qa_retention_series = ref([])
export const d1_avg_qa_retention_series = ref([])
export const d7_avg_qa_retention_series = ref([])
export const d15_avg_qa_retention_series = ref([])
export const d30_avg_qa_retention_series = ref([])
export const uv_qa_retention_option = ref({
        title: {
            text: "用户平均问答数"
        },
        tooltip: {
            trigger: "axis"
        },
        legend:{
            data:['当日所有用户', '第1日留存用户','第7日留存用户','第15日留存用户','第30日留存用户']
        },
        xAxis: {
            type: "category",
            data: avg_qa_retention_x.value,
            axisLabel: {
                formatter: function (value) {
                    return value.substring(0, 13);
                },
                rotate: 45,
            },
        },
        yAxis: {
            type: "value"
        },
        series: [
            {
                data: avg_qa_retention_series.value,
                type: 'line',
                smooth: true,
                name: '当日所有用户'
            },
            {
                data: d1_avg_qa_retention_series.value,
                type: 'line',
                smooth: true,
                name: '第1日留存用户'
            },
            {
                data: d7_avg_qa_retention_series.value,
                type: 'line',
                smooth: true,
                name: '第7日留存用户'
            },
            {
                data: d15_avg_qa_retention_series.value,
                type: 'line',
                smooth: true,
                name: '第15日留存用户'
            },
            {
                data: d30_avg_qa_retention_series.value,
                type: 'line',
                smooth: true,
                name: '第30日留存用户'
            }
        ],
        toolbox: {
            show: true,
            feature: {
                dataView: { readOnly: false },
                magicType: { type: ['line', 'bar'] },
                
                saveAsImage: {}
            }
        },
    })
export async function get_avg_qa_retention(){
    let params = {
        index_name : "avg_qa_retention",
        begin_time : index_begin_time.value,
        top:'',
        company_id:targetCompany.value,
    }
    let res = await get_dashboard_index(params)
    if (!res.error_status){
        avg_qa_retention_x.value.length=0
        avg_qa_retention_series.value.length=0
        for (let item of res.result.avg_qa_retention.avg_qa_retention_series) {
            avg_qa_retention_x.value.push(item.day)
            avg_qa_retention_series.value.push(item.avg_qa_count)
        }
        d1_avg_qa_retention_series.value.length=0
        for (let item of res.result.avg_qa_retention.retention_1) {
            d1_avg_qa_retention_series.value.push(item)
        }
        d7_avg_qa_retention_series.value.length=0
        for (let item of res.result.avg_qa_retention.retention_7) {
            d7_avg_qa_retention_series.value.push(item)
        }
        d15_avg_qa_retention_series.value.length=0
        for (let item of res.result.avg_qa_retention.retention_15) {
            d15_avg_qa_retention_series.value.push(item)
        }
        d30_avg_qa_retention_series.value.length=0
        for (let item of res.result.avg_qa_retention.retention_30) {
            d30_avg_qa_retention_series.value.push(item)
        }
    }
    if( !avg_qa_retention_chart && document.getElementById('avg_qa_retention')){
        avg_qa_retention_chart = echarts.init(
            document.getElementById('avg_qa_retention'), null,
            {width: 1000, height:400}
        );
    }
    avg_qa_retention_chart?.setOption(uv_qa_retention_option.value);
}

let avg_session_retention_chart = null;
export const avg_session_retention_x = ref([])
export const avg_session_retention_series = ref([])
export const d1_avg_session_retention_series = ref([])
export const d7_avg_session_retention_series = ref([])
export const d15_avg_session_retention_series = ref([])
export const d30_avg_session_retention_series = ref([])
export const uv_session_retention_option = ref({
        title: {
            text: "用户平均会话数"
        },
        tooltip: {
            trigger: "axis"
        },
        legend:{
            data:['当日所有用户', '第1日留存用户','第7日留存用户','第15日留存用户','第30日留存用户']
        },
        xAxis: {
            type: "category",
            data: avg_session_retention_x.value,
            axisLabel: {
                formatter: function (value) {
                    return value.substring(0, 13);
                },
                rotate: 45,
            },
        },
        yAxis: {
            type: "value"
        },
        series: [
            {
                data: avg_session_retention_series.value,
                type: 'line',
                smooth: true,
                name: '当日所有用户'
            },
            {
                data: d1_avg_session_retention_series.value,
                type: 'line',
                smooth: true,
                name: '第1日留存用户'
            },
            {
                data: d7_avg_session_retention_series.value,
                type: 'line',
                smooth: true,
                name: '第7日留存用户'
            },
            {
                data: d15_avg_session_retention_series.value,
                type: 'line',
                smooth: true,
                name: '第15日留存用户'
            },
            {
                data: d30_avg_session_retention_series.value,
                type: 'line',
                smooth: true,
                name: '第30日留存用户'
            }
        ],
        toolbox: {
            show: true,
            feature: {
                dataView: { readOnly: false },
                magicType: { type: ['line', 'bar'] },
                
                saveAsImage: {}
            }
        },
    }
)
export async function get_avg_session_retention(){
    let params = {
        index_name : "avg_session_retention",
        begin_time : index_begin_time.value,
        top:'',
        company_id:targetCompany.value,
    }
    let res = await get_dashboard_index(params)
    if (!res.error_status){
        avg_session_retention_x.value.length=0
        avg_session_retention_series.value.length=0
        for (let item of res.result.avg_session_retention.avg_session_retention_series) {
            avg_session_retention_x.value.push(item.day)
            avg_session_retention_series.value.push(item.avg_session_count)
        }
        d1_avg_session_retention_series.value.length=0
        for (let item of res.result.avg_session_retention.retention_1) {
            d1_avg_session_retention_series.value.push(item)
        }
        d7_avg_session_retention_series.value.length=0
        for (let item of res.result.avg_session_retention.retention_7) {
            d7_avg_session_retention_series.value.push(item)
        }
        d15_avg_session_retention_series.value.length=0
        for (let item of res.result.avg_session_retention.retention_15) {
            d15_avg_session_retention_series.value.push(item)
        }
        d30_avg_session_retention_series.value.length=0
        for (let item of res.result.avg_session_retention.retention_30) {
            d30_avg_session_retention_series.value.push(item)
        }
    }
    if( !avg_session_retention_chart && document.getElementById('avg_session_retention')){
        avg_session_retention_chart = echarts.init(
            document.getElementById('avg_session_retention'), null,
            {width: 1000, height:400}
        );
    }
    avg_session_retention_chart?.setOption(uv_session_retention_option.value);
}

// 工单
let ticket_service_type_chart = null;
export const ticket_service_data = ref([])
let ticket_service_type_option = ref({
    title:{
        text: "工单服务类型"
    },
    tooltip: {
        trigger: 'item'
    },
    legend: {
        top: '5%',
        left: 'center'
    },
    series: [
        {
            name: '工单服务类型',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            padAngle: 5,
            itemStyle: {
                borderRadius: 10,
                borderColor: '#fff',
                borderWidth: 2
            },
            label: {
                show: false,
                position: 'center'
            },
            emphasis: {
                label: {
                    show: true,
                    fontSize: 40,
                    fontWeight: 'bold'
                }
            },
            labelLine: {
                show: false
            },
            data: ticket_service_data.value
        }
    ]
})
export async function get_ticket_service_type(){
    let params = {
        index_name : "ticket_service_type",
        begin_time : index_begin_time.value,
        top:'',
        company_id:targetCompany.value,
    }
    let res = await get_dashboard_index(params)
    if (!res.error_status){
        ticket_service_data.value.length=0
        for (let item of res.result.ticket_service_type) {
            ticket_service_data.value.push({value: item.value, name: item.name})
        }
    }
    if( !ticket_service_type_chart && document.getElementById('ticket_service_type')){
        ticket_service_type_chart = echarts.init(
            document.getElementById('ticket_service_type'), null,
            {width: 500, height:400}
        );
    }
    ticket_service_type_chart?.setOption(ticket_service_type_option.value);
}

let ticket_status_chart = null;
export const ticket_status_option = ref({
    title: {
        text: "每日提交工单当前状态"
    },
    tooltip: {
        trigger: "axis",
        showContent: false
    },
    dataset: {
        source: []
    },
    legend : {
        data: [
            '新建', '分配中', '处理中', '已解决','自动关闭', '成功关闭',
            '已拒绝', '挂起', '自动关闭',  '已撤销', '已删除'],
        top: '45%', // 图例距离顶部 15%
        left: 'center', // 图例水平居中
        orient: 'horizontal' // 图例水平排列
    },
    xAxis: { type: 'category' ,axisLabel: {
            formatter: function (value) {
                return value.substring(0, 10); // 显示到小时
            },
            rotate: 45,  // 标签旋转45度以防止重叠

        },},
    yAxis: { gridIndex: 0 },
    grid: { top: '55%' },
    series: [
        {
            name: '新建',
            type: 'line',
            smooth: true,
            seriesLayoutBy: 'row',
            emphasis: { focus: 'series' }
        },
        {
            name: '分配中',
            type: 'line',
            smooth: true,
            seriesLayoutBy: 'row',
            emphasis: { focus: 'series' }
        },
        {
            name: '处理中',
            type: 'line',
            smooth: true,
            seriesLayoutBy: 'row',
            emphasis: { focus: 'series' }
        },
        {
            name: '已解决',
            type: 'line',
            smooth: true,
            seriesLayoutBy: 'row',
            emphasis: { focus: 'series' }
        },
        {
            name: '自动关闭',
            type: 'line',
            smooth: true,
            seriesLayoutBy: 'row',
            emphasis: { focus: 'series' }
        },
        {
            name: '成功关闭',
            type: 'line',
            smooth: true,
            seriesLayoutBy: 'row',
            emphasis: { focus: 'series' }
        },
        {
            name: '已拒绝',
            type: 'line',
            smooth: true,
            seriesLayoutBy: 'row',
            emphasis: { focus: 'series' }
        },
        {
            name: '挂起',
            type: 'line',
            smooth: true,
            seriesLayoutBy: 'row',
            emphasis: { focus: 'series' }
        },
        {
            name: '自动关闭',
            type: 'line',
            smooth: true,
            seriesLayoutBy: 'row',
            emphasis: { focus: 'series' }
        },
        {
            name: '已撤销',
            type: 'line',
            smooth: true,
            seriesLayoutBy: 'row',
            emphasis: { focus: 'series' }
        },
        {
            name: '已删除',
            type: 'line',
            smooth: true,
            seriesLayoutBy: 'row',
            emphasis: { focus: 'series' }
        },
        {
            type: 'pie',
            id: 'pie',
            radius: '30%',
            center: ['50%', '25%'],
            emphasis: {
                focus: 'self'
            },
            label: {
                formatter: '{b}: {@[1]} ({d}%)'
            },
            encode: {
                itemName: 'ticket_status',
                value: '1',
                tooltip: '1'
            }
        }
    ],

})
export async function get_ticket_status(){
    let params = {
        index_name : "ticket_status",
        begin_time : index_begin_time.value,
        top:'',
        company_id:targetCompany.value
    }
    let res = await get_dashboard_index(params)
    if (!res.error_status){
        ticket_status_option.value.dataset.source = res.result.ticket_status
    }
    if( !ticket_status_chart && document.getElementById('ticket_status')){
        ticket_status_chart = echarts.init(
            document.getElementById('ticket_status'), null,
            {width: 600, height:600}
        );
    }

    ticket_status_chart?.on('updateAxisPointer', function (event:any) {
        const xAxisInfo = event.axesInfo[0];
        if (xAxisInfo) {
            const dimension = xAxisInfo.value +1 ;
            ticket_status_chart?.setOption({
                series: {
                    id: 'pie',
                    label: {
                        formatter: '{b}: {@[' + dimension + ']} ({d}%)'
                    },
                    encode: {
                        value: dimension,
                        tooltip: dimension
                    }
                }
            });
        }
    });
    ticket_status_chart?.setOption(ticket_status_option.value);
}

let success_ticket_service_type_chart = null;
export const success_ticket_service_option =  ref({
    title: {
        text: "每日成功提交工单服务类型"
    },
    tooltip: {
        trigger: "axis",
        showContent: false
    },
    dataset: {
        source: []
    },
    legend : {
        data: [ '安装部署', '故障解决', '性能优化', '咨询和其他'],
        top: '45%', // 图例距离顶部 15%
        left: 'center', // 图例水平居中
        orient: 'horizontal' // 图例水平排列
    },
    xAxis: { type: 'category' ,axisLabel: {
            formatter: function (value) {
                return value.substring(0, 10); // 显示到小时
            },
            rotate: 45,  // 标签旋转45度以防止重叠

        },},
    yAxis: { gridIndex: 0 },
    grid: { top: '55%' },
    series: [
        {
            name: '安装部署',
            type: 'line',
            smooth: true,
            seriesLayoutBy: 'row',
            emphasis: { focus: 'series' }
        },
        {
            name: '故障解决',
            type: 'line',
            smooth: true,
            seriesLayoutBy: 'row',
            emphasis: { focus: 'series' }
        },
        {
            name: '性能优化',
            type: 'line',
            smooth: true,
            seriesLayoutBy: 'row',
            emphasis: { focus: 'series' }
        },
        {
            name: '咨询和其他',
            type: 'line',
            smooth: true,
            seriesLayoutBy: 'row',
            emphasis: { focus: 'series' }
        },
        {
            type: 'pie',
            id: 'pie',
            radius: '30%',
            center: ['50%', '25%'],
            emphasis: {
                focus: 'self'
            },
            label: {
                formatter: '{b}: {@[1]} ({d}%)'
            },
            encode: {
                itemName: 'success_ticket_service_type',
                value: '1',
                tooltip: '1'
            }
        }
    ],

})
export async function get_success_ticket_service_type(){
    let params = {
        index_name : "success_ticket_service_type",
        begin_time : index_begin_time.value,
        top:'',
        company_id:targetCompany.value
    }
    let res = await get_dashboard_index(params)
    if (!res.error_status){
        success_ticket_service_option.value.dataset.source = res.result.success_ticket_service_type
    }
    if( !success_ticket_service_type_chart && document.getElementById('success_ticket_service_type')){
        success_ticket_service_type_chart = echarts.init(
            document.getElementById('success_ticket_service_type'), null,
            {width: 600, height:500}
        );
    }

    success_ticket_service_type_chart?.on('updateAxisPointer', function (event:any) {
        const xAxisInfo = event.axesInfo[0];
        if (xAxisInfo) {
            const dimension = xAxisInfo.value + 1;
            success_ticket_service_type_chart?.setOption({
                series: {
                    id: 'pie',
                    label: {
                        formatter: '{b}: {@[' + dimension + ']} ({d}%)'
                    },
                    encode: {
                        value: dimension,
                        tooltip: dimension
                    }
                }
            });
        }
    });
    success_ticket_service_type_chart?.setOption(success_ticket_service_option.value);
}
