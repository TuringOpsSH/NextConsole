import {ref} from "vue";
import {msg_item} from "@/types/next_console";
import {get_msg_rag_trace, get_msg_workflow_trace} from "@/api/feedback_center";

export const showMsgTrace = ref(false);
export const CurrentMsg = ref<msg_item>()
export const CurrentMsgTab = ref(1)
export const CurrentMsgRagTrace = ref ()
export const CurrentMsgWorkFlowTrace = ref()
export async function showMsgTraceDialog(msg:msg_item){
    showMsgTrace.value=true;
    CurrentMsg.value=msg;
    await showMsgRagTrace();
}

export async function showMsgRagTrace(){
    CurrentMsgTab.value = 1
    let params = {
        msg_id: CurrentMsg.value.msg_id
    }
    let res =  await get_msg_rag_trace(params)
    if (!res.error_status){
        CurrentMsgRagTrace.value=res.result
    }
}
export function showMsgQaTrace(){
    CurrentMsgTab.value  = 2
}

export async function showMsgWorkFlowTrace(){
    CurrentMsgTab.value = 3
    let params = {
        msg_id: CurrentMsg.value.msg_id
    }
    let res =  await get_msg_workflow_trace(params)
    if (!res.error_status){
        CurrentMsgWorkFlowTrace.value=res.result
    }
}