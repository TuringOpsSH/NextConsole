import {ref} from 'vue';
import {appDetail, initAppSession} from "@/api/app-center";
import {splitMarkdown} from "@/components/next_console/messages_flow/message_flow";
import router from "@/router";
import {
  msg_queue_item,
  qa_item,
  recommend_question_item,
  reference_map,
  session_item,
  workflow_task_map
} from "@/types/next_console";
import {
  create_qa,
  get_workflow_progress_batch,
  search_messages,
  search_qa,
  search_reference,
  update_recommend_question
} from "@/api/next_console";
import {ElMessage} from "element-plus";
import {askAgentQuestion, consoleInput} from "@/components/app_center/ts/agent_console";
import {assistant} from "@/types/assistant";
import {IAppMeta} from "@/types/app";
import {running_questions} from "@/components/next_console/messages_flow/console_input";

export const CurrentAgentApp = ref<IAppMeta>({ app_code :'' }) // 当前应用
export const CurrentAgentAppSession = ref<session_item>({id: 0}) // 当前应用会话
export const CurrentAgentAppQas = ref<qa_item[]>([]) // 当前应用问答
export const LoadingStatus = ref( false) // 加载状态
export const AgentAppMsgFlow = ref<msg_queue_item[]>([])
export const QAWorkFlowMap =  ref<workflow_task_map>({})
export const CurrentAgentReference = ref<reference_map>({})
export const FlowIsScrolling = ref(false)
export const agentFlowBoxRef = ref<HTMLDivElement>()
export const AgentFlowScrollbarRef = ref()
export const AgentScrollButtonTimeout = ref(null)
export const scrollTimer =ref ()
export const scrollToFlag = ref(false)
export const CurrentAgent = ref<assistant>({ id : 0,})
export const sessionAttachData = ref(null)
export const currentGraphConfigs = ref({})
export async function getAgentApp(code:string) {
  // 获取当前应用
  const result = await appDetail({
    app_code: code
  })
  if (!result.error_status){
    CurrentAgentApp.value = result.result
  }
}

export async function getAgentAppSession(app_code: string, session_code: string) {
  if (!app_code){
    return
  }
  const result = await initAppSession({
    app_code: app_code,
    session_code: session_code
  })
  if (!result.error_status){
    CurrentAgentAppSession.value = result.result
    router.replace({
      params: {
        app_code: app_code,
        session_code: CurrentAgentAppSession.value.session_code
      }
    })
  }
}

export async function initAgentAppQas(app_code: string, session: string) {
  if (!CurrentAgentAppSession.value.id){
    return
  }
  const result = await search_qa({
    session_id: [CurrentAgentAppSession.value.id]
  })
  if (!result.error_status){
    CurrentAgentAppQas.value = result.result
  }
}
export async function addAgentAppQa() {
  let data = await create_qa({
    session_id: CurrentAgentAppSession.value.id,
    qa_topic: consoleInput.value
  })
  CurrentAgentAppQas.value.unshift(data.result)
  return data.result
}
export async function initAgentAppMsg(app_code: string, session: string) {
  // 更新问答
  if (!CurrentAgentAppQas.value?.length){
    return
  }
  const result = await search_messages({
    qa_id: CurrentAgentAppQas.value.map(item => item.qa_id)
  })
  if (!result.error_status) {
    AgentAppMsgFlow.value = result.result
    for (let i = 0; i < AgentAppMsgFlow.value.length; i++) {
      let item = AgentAppMsgFlow.value[i]
      splitMarkdown(item)
      item.qa_finished = true
    }
    if (AgentAppMsgFlow.value?.length) {
      initAgentWorkflow()
      initAgentReference()
    }
  }
}

export async function initAgentWorkflow(){
  const res = await get_workflow_progress_batch({
    qa_ids: CurrentAgentAppQas.value.map(item => item.qa_id)
  })
  if (!res.error_status){
      QAWorkFlowMap.value = res.result
  }
  // 填充 currentGraphConfigs
    for (let key of Object.keys(QAWorkFlowMap.value)){
      const workflowList = QAWorkFlowMap.value[key]
        for (let i = 0; i < workflowList.length; i++) {
            const workflowItem = workflowList[i]
          if (!currentGraphConfigs.value[workflowItem.msg_id]){
            currentGraphConfigs.value[workflowItem.msg_id] = {}
          }
            if (workflowItem.task_type == 'SQL查询') {
              let resultJson = {
                sql: undefined,
                data: undefined,
                columns: undefined,
              }
              try {
                 resultJson = JSON.parse(workflowItem.task_result)
                  currentGraphConfigs.value[workflowItem.msg_id].sql = resultJson.sql
                  currentGraphConfigs.value[workflowItem.msg_id].raw_data = resultJson.data
                  currentGraphConfigs.value[workflowItem.msg_id].columns = resultJson.columns
              } catch (e) {}


            }
            if (workflowItem.task_type == '图表生成') {
              // console.log(workflowItem.task_result)
              try {
                currentGraphConfigs.value[workflowItem.msg_id].options = JSON.parse(workflowItem.task_result).options
                currentGraphConfigs.value[workflowItem.msg_id].pane = 'graph'
              } catch (e) {}
            }
        }
    }
}
export async function initAgentReference(){
  let params = { msg_id_list: []}
  for (let i = 0; i < AgentAppMsgFlow.value.length; i++) {
      for (let j = 0; j < AgentAppMsgFlow.value[i].qa_value.question.length; j++) {
          params.msg_id_list.push(AgentAppMsgFlow.value[i].qa_value.question[j].msg_id)
      }
  }
  let res = await search_reference(params)
  if (!res.error_status){
    CurrentAgentReference.value = res.result
    if (CurrentAgentReference.value){
      for (let msg_item of AgentAppMsgFlow.value) {
        for (let question of msg_item.qa_value.question) {
          if (CurrentAgentReference.value?.[question.msg_id]){
            // 生成参考文献链接，并添加至msg_content 后
            let reference_markdown_text = ''
            let reference_list = CurrentAgentReference.value[question.msg_id]
            for (let i = 0; i < reference_list.length; i++) {
              let base_url = window.location.origin
              if (reference_list[i].source_type == "resource") {
                reference_markdown_text += `\n\n [${i+1}]: ${base_url}/#/next_console/resources/resource_viewer/${reference_list[i].resource_id} `
              }
              else if (reference_list[i].source_type == "webpage") {
                reference_markdown_text += `\n\n [${i+1}]: ${reference_list[i].resource_source_url} `
              }
            }
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

}
export async function getTargetAgentReference(msgId: number){
// 为完成的消息获取参考文献
  let params = {
    msg_id_list: [msgId],
  }
  let res = await search_reference(params)
  if (!res.error_status) {
    if (!CurrentAgentReference.value?.[msgId]){
      CurrentAgentReference.value[msgId] = res.result[msgId]
    }
    if (!res.result[msgId]?.length){
      return
    }
    let reference_markdown_text = ''
    for (let i = 0; i < res.result[msgId].length; i++) {
      let base_url = window.location.origin
      if (res.result[msgId][i].source_type == "resource") {
        reference_markdown_text += `\n\n [${i+1}]: ${base_url}/#/next_console/resources/resource_viewer/${res.result[msgId][i].resource_id} `
      }
      else if (res.result[msgId][i].source_type == "webpage") {
        reference_markdown_text += `\n\n [${i+1}]: ${res.result[msgId][i].resource_source_url} `
      }

    }
    // 等待问题加载完成
    await checkQuestionStatus(msgId,100)
    for (let msg_item of AgentAppMsgFlow.value) {
      for (let question of msg_item.qa_value.question) {
        if (question.msg_id == msgId){
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
export async function checkQuestionStatus(msg_id:number, delay:number){
// 周期性检查图片附件上传情况
  return new Promise((resolve) => {
    let intervalId = setInterval(() => {
      // 这里添加你的检查逻辑
      let check_condition = true

      for (let i of running_questions.value){

        if (AgentAppMsgFlow.value[i.qa_item_idx].qa_value.question[0]?.msg_id == msg_id ){
          if (!AgentAppMsgFlow.value[i.qa_item_idx]?.qa_finished) {
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
export function scrollToBottom(){
  // 正在滚动中
  if (FlowIsScrolling.value) {
    return
  }
  if (!agentFlowBoxRef.value) {
    // console.log('AgentFlowScrollbarRef 不存在')
    return
  }
  let scrollMax = agentFlowBoxRef.value.clientHeight

  clearTimeout(AgentScrollButtonTimeout.value);
  FlowIsScrolling.value = true
  AgentFlowScrollbarRef.value.scrollTo({top: scrollMax, behavior: 'smooth'})
  AgentScrollButtonTimeout.value = setTimeout(() => {
    FlowIsScrolling.value = false
  }, 500)
}
export function scrollToTop(){
  // 正在滚动中
  if (FlowIsScrolling.value) {
    return
  }
  clearTimeout(AgentScrollButtonTimeout.value);
  if(!Math.ceil(AgentFlowScrollbarRef.value.wrapRef.scrollTop)){
    ElMessage({
      message: '已经到顶啦！',
      type: 'success',
      duration: 2000
    })
    return;
  }


  FlowIsScrolling.value = true

  AgentFlowScrollbarRef.value.scrollTo({top: 0, behavior: 'smooth'})

  AgentScrollButtonTimeout.value = setTimeout(() => {
    FlowIsScrolling.value = false
  }, 500)
}
export function scrollToQA(step :number){
  // 正在滚动中
  if (FlowIsScrolling.value) {
    return
  }
  if (!agentFlowBoxRef.value) {
    return
  }
  clearTimeout(AgentScrollButtonTimeout.value);
  AgentScrollButtonTimeout.value = setTimeout(() => {
    // 为了保证精度，全部转为int
    FlowIsScrolling.value = true
    // 第i个回答的下沿

    // 获取当前页面上方隐藏高度
    let currentHeight = Math.ceil(AgentFlowScrollbarRef.value.wrapRef.scrollTop)
    // 获取视窗高度
    let viewHeight = Math.ceil(AgentFlowScrollbarRef.value.wrapRef.clientHeight)
    let viewBottom = currentHeight + viewHeight
    let targetHeight = 0
    if (step > 0) {
      // 向下滚动到下step个问题,
      for (let i = 0; i < agentFlowBoxRef.value.children.length; i++) {
        targetHeight +=  Math.floor(agentFlowBoxRef.value.children[i].clientHeight)
        if ( targetHeight > currentHeight) {
          break
        }
      }
    }
    else {
      // 向上滚动到上step个问题
      let index = 0
      for (let i = 0; i < agentFlowBoxRef.value.children.length; i++) {
        targetHeight +=  Math.floor(agentFlowBoxRef.value.children[i].clientHeight)
        if ( targetHeight > currentHeight) {
          index = i
          break
        }
      }
      // index 为下一个问题，targetHeight 为下一个问题的上沿
      // 减去两个问题即可
      targetHeight -= agentFlowBoxRef.value.children[index]?.clientHeight
      if (targetHeight >= currentHeight ) {
        targetHeight -= agentFlowBoxRef.value.children[index -1]?.clientHeight
      }


    }
    AgentFlowScrollbarRef.value.scrollTo({top: targetHeight, behavior: 'smooth'})
    if (!targetHeight){
      ElMessage({
        message: '已经到顶啦！',
        type: 'success',
        duration: 2000
      })
    }

    setTimeout(() => {
      FlowIsScrolling.value = false
    }, 500)
  }, 200);
}
export function handleScroll() {
  if (scrollTimer.value) {
    clearTimeout(scrollTimer.value)
  }
  scrollToFlag.value = true
  scrollTimer.value = setTimeout(() => {
    scrollToFlag.value = false
  }, 6000)

}
export async function clickRecommendQuestion(recommend_question: recommend_question_item){
  // 点击推荐问题,直接提问并更新点击
  consoleInput.value = recommend_question.recommend_question
  if (recommend_question.id) {

    update_recommend_question({"recommend_question_id": recommend_question.id })
  }
  // 追加提问
  await askAgentQuestion()
}
export function sendMessageToParent(data) {
  window.parent.postMessage(data, '*'); // '*' 表示不限制目标域名
}
