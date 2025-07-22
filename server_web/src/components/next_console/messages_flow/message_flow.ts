import {nextTick, ref} from "vue";
import {
    get_workflow_progress_batch,
    search_reference,
    update_messages,
    update_recommend_question
} from "@/api/next_console";
import {
    msg_queue_item,
    recommend_question_item,
    recommend_question_map,
    reference_item,
    reference_map,
    workflow_task_map
} from "@/types/next_console";
import MarkdownIt from "markdown-it";
import hljs from "highlight.js";
import markdownItKatex from '@vscode/markdown-it-katex';
import markdownItMermaid from 'markdown-it-mermaid-plugin';
import '@/styles/katex.min.css';
import Clipboard from "clipboard";
import {ElMessage} from "element-plus";
import {ask_question, running_questions, user_input} from "@/components/next_console/messages_flow/console_input";
import mermaid from "mermaid";

export const msgFlowRef = ref(null);
export const msg_recommend_question = ref<recommend_question_map>({});
export const msg_flow = ref<msg_queue_item[]>([]);
export const msg_flow_box_Ref =ref<HTMLDivElement>()
export const msg_flow_scrollbar_Ref = ref();
export const scrollTimer = ref();
export const scrollToFlag = ref(false);
export const isScrolling = ref(false);
export const scroll_button_timeout = ref(null);
export const msg_flow_reference = ref<reference_map>({});
export const show_sup_detail = ref(false);
export const tooltipStyle = ref({});
export const current_sup_detail = ref<reference_item>();
export const qa_workflow_map = ref<workflow_task_map>({});
export const userStopScroll = ref(false);
export async function click_recommend_question(recommend_question: recommend_question_item){
    // 点击推荐问题,直接提问并更新点击
    user_input.value = recommend_question.recommend_question
    update_recommend_question({"recommend_question_id": recommend_question.id })
    // 追加提问
    await ask_question()
}

export async function get_target_reference(msg_id: number,){
    // 为完成的消息获取参考文献
    let params = {
        msg_id_list: [msg_id],
    }
    let res = await search_reference(params)
    if (!res.error_status) {
        if (!msg_flow_reference.value?.[msg_id]){
            msg_flow_reference.value[msg_id] = res.result[msg_id]
        }
        if (!res.result[msg_id]?.length){
            return
        }
        let reference_markdown_text = ''
        for (let i = 0; i < res.result[msg_id].length; i++) {
            let base_url = window.location.origin
            if (res.result[msg_id][i].source_type == "resource") {
                reference_markdown_text += `\n\n [${i+1}]: ${base_url}/#/next_console/resources/resource_viewer/${res.result[msg_id][i].resource_id} `
            }
            else if (res.result[msg_id][i].source_type == "webpage") {
                reference_markdown_text += `\n\n [${i+1}]: ${res.result[msg_id][i].resource_source_url} `
            }

        }
        // 等待问题加载完成
        await check_question_status(msg_id,100)
        for (let msg_item of msg_flow.value) {
            for (let question of msg_item.qa_value.question) {
                if (question.msg_id == msg_id){
                    if (!msg_item.qa_value.answer[question.msg_id][0]?.msg_reference_finish){
                        msg_item.qa_value.answer[question.msg_id][0].msg_content += reference_markdown_text
                        splitMarkdown(msg_item)
                        msg_item.qa_value.answer[question.msg_id][0].msg_reference_finish = true
                    }
                }
            }
        }
    }
}
export async function check_question_status(msg_id:number, delay:number){
// 周期性检查图片附件上传情况
    return new Promise((resolve) => {
        let intervalId = setInterval(() => {
            // 这里添加你的检查逻辑
            let check_condition = true

            for (let i of running_questions.value){

                if (msg_flow.value[i.qa_item_idx].qa_value.question[0]?.msg_id == msg_id ){
                    if (!msg_flow.value[i.qa_item_idx]?.qa_finished) {
                        check_condition = false
                    }

                }
            }
            if (check_condition) {
                clearInterval(intervalId);
                resolve(true);
            }
        }, delay);
    });
}
export function add_copy_button_event() {
    let copy_button_list = document.getElementsByClassName("answer-code-copy")
    for (let i = 0; i < copy_button_list.length; i++) {
        let button = copy_button_list[i] as HTMLElement;
        if (button.dataset.clickListener === 'true') {
            continue;
        }
        copy_button_list[i].addEventListener('click', function () {
            let code = (this.parentNode.nextElementSibling && this.parentNode.nextElementSibling.innerText) || '';
            Clipboard.copy(code.trim())
            ElMessage({
                message: '复制成功',
                type: 'success',
                duration: 2000
            })
        })
        button.dataset.clickListener = 'true';
    }
    try {
        // 获取页面上所有的 <sup> 标签
        let supTags = document.querySelectorAll('sup');

        // 遍历每个 <sup> 标签
        supTags.forEach(function(supTag) {
            // 获取 <sup> 标签下的所有 <a> 标签
            let aTags = supTag.querySelectorAll('a');

            // 遍历每个 <a> 标签
            aTags.forEach(function(aTag) {

                // 为 <a> 标签添加 target="_blank" 属性
                aTag.setAttribute('target', '_blank');


            });
        });
    } catch (error) {
        console.error('An error occurred:', error);
    }
    render_mermaid()

}
export function copy_question(item: msg_queue_item){
    let content = item?.qa_value?.question?.[0]?.msg_content
    if (!content) {
        return
    }
    Clipboard.copy(content.trim())
    ElMessage({
        message: '复制成功',
        type: 'success',
        duration: 2000
    })
}
export function copy_answer(item: msg_queue_item){
    let msg_parent_id = item?.qa_value?.question?.[0]?.msg_id
    if (!msg_parent_id){
        // @ts-ignore
        msg_parent_id = 'null'
    }
    let content = item?.qa_value?.answer?.[msg_parent_id]?.[0]?.msg_content
    if (!content) {
        return
    }
    // 去除 <sup> 标签及其内容
    const cleanedData = content.replace(/<sup>.*?<\/sup>/g, '');

    // 去除参考索引，如 [1]: https://www.turingops.com.cn/dev/
    const finalData = cleanedData.replace(/\[.*?]:\s*\S+/g, '');
    Clipboard.copy(finalData.trim())
    ElMessage({
        message: '复制成功',
        type: 'success',
        duration: 2000
    })

}

export let md_answer = new MarkdownIt(
    {
        html: true,
        linkify: true,
        typographer: true,
        breaks: true,
        highlight: function (str, lang) {
            let language = lang ? lang : 'plaintext';
            let language_text = '<span style="">' +
                language +
                '</span>'
            let copy_button = '<img src="images/copy.svg" alt="复制" class="answer-code-copy" style="width: 20px;height: 20px;cursor: pointer"/>'
            let header =  '<div style="display: flex;justify-content: space-between;border-bottom: 1px solid #D0D5DD;padding: 8px">'
                + language_text + copy_button +
                '</div>'

            if (hljs.getLanguage(language)) {
                try {

                    return '<pre class="hljs" style="white-space: pre-wrap; overflow: auto ; position: relative;' +
                        'border-bottom: 1px solid #D0D5DD;padding: 16px">'
                        +header + '<code class="hljs-code" >' + '<br>' +

                        hljs.highlight(str, {language: language, ignoreIllegals: true}).value + '<br>' +
                        '</code></pre>'
                } catch (__) {

                }
            }

            return '<pre class="hljs" style="white-space: pre-wrap; overflow: auto ; position: relative;' +
                'border-bottom: 1px solid #D0D5DD;padding: 16px">'
                +header + '<code class="hljs-code" >' + '<br>' +
                hljs.highlight(str, {language: 'plaintext', ignoreIllegals: true}).value + '<br>' +
                '</code></pre>';
        }
    }
);
// 添加数学公式支持
md_answer.use(markdownItKatex, {
    throwOnError: false,
    errorColor: ' #cc0000',
    strict: false,  // 允许非标准语法


});
// 添加mermaid支持
// 使用 mermaid 插件
md_answer.use(markdownItMermaid);
// 自定义表格渲染
const defaultTableRule = md_answer.renderer.rules.table_open || function (tokens, idx, options, env, self) {
    return self.renderToken(tokens, idx, options);
};
md_answer.renderer.rules.table_open = function (tokens, idx, options, env, self) {
    tokens[idx].attrPush(['class', 'custom-table']);
    return defaultTableRule(tokens, idx, options, env, self);
};
const customTableStyle = `
    <style>
    .custom-table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 1rem;
    }
    .custom-table th, .custom-table td {
        border: 1px solid #D0D5DD;
        padding: 8px;
        text-align: left;
    }
    .custom-table th {
        background-color: #f2f2f2;
    }
    </style>
`;
document.head.insertAdjacentHTML('beforeend', customTableStyle);

// 自定义图片样式
md_answer.renderer.rules.image = function (tokens, idx, options, env, self) {
    const token = tokens[idx];
    const src = token.attrGet('src');
    const alt = token.content;
    const title = token.attrGet('title');
    const is_last = env.is_last;
    const imgHtml = `<img src="${src}" alt="${alt}" title="${title}" style="max-width: 100%">`;

    if (is_last) {
        return ` <div style="text-align: center;">${src}</div> `;
    }

    return ` <div style="text-align: center;">${imgHtml}</div> `;
};

// 自定义链接样式
md_answer.renderer.rules.link_open = function (tokens, idx, options, env, self) {
    const aIndex = tokens[idx].attrIndex('target');

    if (aIndex < 0) {
        tokens[idx].attrPush(['target', '_blank']); // 添加 target="_blank"
    } else {
        tokens[idx].attrs[aIndex][1] = '_blank';    // 替换现有的 target 属性
    }

    return self.renderToken(tokens, idx, options);
};
// 自定义引用样式
md_answer.renderer.rules.blockquote_open = function (tokens, idx, options, env, self) {
    tokens[idx].attrSet('class', 'my-custom-quote');
    return self.renderToken(tokens, idx, options);
};
// 自定义角标样式
export function splitMarkdown(item: msg_queue_item  ) {
    // 找到最小粒度的tokens，分别转换为html，然后与存量html比对，不同则替换
    let msg_parent_id =item.qa_value.question?.[0]?.msg_id
    if (!msg_parent_id){
        // @ts-ignore
        msg_parent_id = 'null'
    }
    let msg_content = item.qa_value.answer[msg_parent_id]?.[0]?.msg_content
    if (!msg_content){
        return
    }
    let tokens = md_answer.parse(msg_content, {})
    let finish_queue = []
    let queue = []
    // 遍历tokens 将完成的token匹配好存入finish_queue
    tokens.forEach((token, index) => {
        queue.push(token)
        if (token.type.includes('_close')){
            let open_token_name = token.type.replace('_close', '_open')
            if (queue[0].type === open_token_name) {
                let finish_flag = true
                queue.forEach((token, index) => {
                    if (index >0 && token.type == open_token_name){
                        finish_flag = false
                    }
                })
                if (finish_flag){
                    finish_queue.push(queue)
                    queue = []
                }
            }
        }
        else if (!token.type.includes('_open')){
            if (queue.length == 1) {
                finish_queue.push(queue)
                queue = []
            }
        }
    })
    if (!item.qa_value.answer[msg_parent_id][0].msg_content_finish_html){
        item.qa_value.answer[msg_parent_id][0].msg_content_finish_html = []
    }
    finish_queue.forEach((sub_queue, index) => {

        let html = md_answer.renderer.render(
            sub_queue,
            md_answer.options,
            {
                is_last: index == finish_queue.length - 1  && running_questions.value.length > 0
            }
        )
        // 两者比对，不同则替换
        if (item.qa_value.answer[msg_parent_id][0].msg_content_finish_html[index] !== html){
            item.qa_value.answer[msg_parent_id][0].msg_content_finish_html[index] = html
        }
    })
    // 如果完成的html比存量html多，截取，可能原因是搜索时，搜索到的内容比原有的内容多
    if (finish_queue.length < item.qa_value.answer[msg_parent_id][0].msg_content_finish_html.length){
        item.qa_value.answer[msg_parent_id][0].msg_content_finish_html = item.qa_value.answer[msg_parent_id][0].msg_content_finish_html.slice(0, finish_queue.length)
    }
    //如果还剩下没有匹配上的，直接推入
    if (queue.length) {
        let html = md_answer.renderer.render(
            queue,
            md_answer.options,
            {}
        )
        item.qa_value.answer[msg_parent_id][0].msg_content_finish_html.push(html)
    }
    render_mermaid()

}
export function get_msg_item_answer_create_time(item: msg_queue_item){
    try {
        let msg_parent_id = item?.qa_value?.question?.[0].msg_id
        return item?.qa_value?.answer?.[msg_parent_id]?.[0].create_time
    } catch (e) {
        return ''
    }

}
export function switch_answer_length(item: msg_queue_item){

    item.short_answer = !item.short_answer

}
export function scroll_to_bottom() {
  // 正在滚动中
  if (isScrolling.value) {
    return;
  }
  if (userStopScroll.value) {
    return;
  }
  if (!msg_flow_box_Ref.value) {
    return;
  }
  const scrollMax = msg_flow_box_Ref.value.clientHeight;
  clearTimeout(scroll_button_timeout.value);
  isScrolling.value = true;
  msg_flow_scrollbar_Ref.value.scrollTo({ top: scrollMax, behavior: 'smooth'})
  scroll_button_timeout.value = setTimeout(() => {
    isScrolling.value = false;
  }, 500);
}
export async function add_like(item:msg_queue_item){
    let question_id = item.qa_value.question[0]?.msg_id
    if (!question_id){
        // @ts-ignore
        question_id = 'null'
    }
    let answer_id = item.qa_value.answer[question_id][0]?.msg_id
    if (!answer_id) {
        ElMessage.info(
            {
                message: "请过会儿点击，感谢您的支持！",
                "duration": 1000

            })

        return false
    }
    if (item.qa_value.answer[question_id][0].msg_remark == 1) {
        await update_messages(
            {
                "msg_id": answer_id,
                "msg_remark": 0
            }
        )
        item.qa_value.answer[question_id][0].msg_remark = 0
        ElMessage.success(
            {
                message: "取消收藏！",

            }
        )
        return
    }
    await update_messages(
        {
            "msg_id": answer_id,
            "msg_remark": 1
        }
    )
    item.qa_value.answer[question_id][0].msg_remark = 1
    ElMessage.success(
        {
            message: "收藏成功！",

        }
    )
}
export async function add_dislike(item:msg_queue_item){
    let question_id = item.qa_value.question[0]?.msg_id
    if (!question_id){
        // @ts-ignore
        question_id = 'null'
    }
    let answer_id = item.qa_value.answer[question_id][0]?.msg_id
    if (!answer_id) {
        ElMessage.info(
            {
                message: "请过会儿点击，感谢您的支持！",
                "duration": 1000

            })

        return false
    }
    if (item.qa_value.answer[question_id][0].msg_remark == -1) {
        await update_messages(
            {
                "msg_id": answer_id,
                "msg_remark": 0
            }
        )
        item.qa_value.answer[question_id][0].msg_remark = 0
        ElMessage.success(
            {
                message: "取消点踩成功！",

            }
        )
        return
    }
    await update_messages(
        {
            msg_id: item.qa_value.answer[question_id][0].msg_id,
            msg_remark: -1
        }
    )
    item.qa_value.answer[question_id][0].msg_remark = -1
    ElMessage.success(
        {
            message: "感谢您的反馈！我们会尽快改进！",

        }
    )
}
export async function show_sup_detail_fn(item: msg_queue_item, event){
    if (event.target.tagName.toLowerCase() === 'sup'||
        (event.target.tagName.toLowerCase() === 'a' && event.target.parentElement.tagName.toLowerCase() === 'sup')) {
        show_sup_detail.value = true
        const targetRect = event.target.getBoundingClientRect();
        const mouseX = event.clientX;
        const mouseY = event.clientY;
        tooltipStyle.value = {
            position: 'absolute',
            top: `${window.scrollY + mouseY}px`, // 鼠标的Y轴位置
            left: `${window.scrollX + mouseX}px`, // 鼠标的X轴位置
        };
        let question_id = item.qa_value.question[0].msg_id
        let reference_list = msg_flow_reference.value?.[question_id]// 获取 <sup> 的内容
        if (reference_list?.length){
            current_sup_detail.value = null
            for (let i = 0; i <= reference_list.length; i++) {
                if (i == event.target.textContent) {

                    current_sup_detail.value = reference_list[i-1]
                }
            }
        }
    }
    else {
        show_sup_detail.value = false
    }
}
export async function get_lasted_workflow(){
    // 获取最新的工作流
    let params = {
        "qa_ids": [],
    }
    for (let i = 0; i < msg_flow.value.length; i++) {
        params.qa_ids.push(msg_flow.value[i].qa_id)
    }
    let res = await get_workflow_progress_batch(params)
    if (!res.error_status){
        qa_workflow_map.value = res.result
    }
}
mermaid.initialize({
    startOnLoad: false,
    securityLevel: 'loose',
    gantt: {
        axisFormat: '%Y-%m-%d',
    }
});
export async function render_mermaid(){
    await nextTick()
    const nodes = document.querySelectorAll(".mermaid");

    // 提前验证至挑选合法的语法进行渲染
    const nodes_valid = []
    for (let node of nodes) {
        let mermaid_text = node.textContent

        if (mermaid_text) {
            // gantt 最后渲染
            try {
                await mermaid.parse(mermaid_text)
                nodes_valid.push(node)
            } catch (e) {
            }
        }
    }

    await mermaid.run({
        // @ts-ignore
        nodes: Array.from(nodes_valid),
        suppressErrors: true,
    });


}
