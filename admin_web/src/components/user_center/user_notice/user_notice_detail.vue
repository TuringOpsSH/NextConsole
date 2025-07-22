<script setup lang="ts">
import {onMounted, watch} from 'vue'
import {
  area_company_options,
  area_department_options,
  area_shortcut,
  area_target_companies,
  area_target_departments,
  area_target_users,
  area_user_options,
  check_html_valid,
  current_notice_task,
  current_notice_template_valid,
  delete_current_task,
  handle_notice_area_change,
  handle_notice_company_change,
  handle_notice_department_change,
  handle_notice_user_change,
  init_current_task,
  notice_task_Ref,
  notice_task_rules,
  search_company,
  search_department,
  search_user,
  start_notice_task,
  task_loading,
  loading_text,
  update_current_task,
  refresh_interval,
  refresh_task_detail,
  pause_notice_task,
  resume_notice_task,
  stop_notice_task,
  current_task_instances
} from "@/components/user_center/user_notice/user_notice_detail";
import {onBeforeRouteLeave} from 'vue-router';
import router from "@/router";
import {get_notification_data} from "@/components/user_center/user_notice/user_notification";

const props = defineProps({
  task_id: {
    type: Number,
    require: false,
    default: null,
  },

})

watch (()=>props.task_id, async (new_task_id)=>{

    await init_current_task(new_task_id)
    if (current_notice_task.task_status === '执行中'){
      // 开始刷新任务详情
      if (refresh_interval.value){
        clearInterval(refresh_interval.value)
      }
      refresh_interval.value = setInterval(refresh_task_detail, 2000)
    }

}, {immediate: true})
onBeforeRouteLeave(()=>{
  if (refresh_interval.value){
    clearInterval(refresh_interval.value)}
})
</script>

<template>
  <el-container>
    <el-header>
      <div id="detail-header-area">
        <div id="detail-header-left">
          <div>
            <el-text class="next-console-font-bold" style="width: 60px;color: #101828"> 任务详情</el-text>
          </div>


        </div>
        <div id="detail-header-right">
          <div>
            <el-button type="primary" @click="router.push({'name':'user_notification_list'});get_notification_data()"
                       round>
              返回
            </el-button>
          </div>
          <div v-if="current_notice_task.task_status =='新建中'">
            <el-button type="primary" @click="update_current_task" round>
              保存
            </el-button>
          </div>
          <div v-if="current_notice_task.task_status =='新建中'">
            <el-button type="success" round @click="start_notice_task" >
              启动
            </el-button>
          </div>
          <div v-else-if="current_notice_task.task_status == '执行中'">
            <el-button type="info" round @click="pause_notice_task" >
              暂停
            </el-button>
          </div>
          <div v-else-if="current_notice_task.task_status == '已暂停'">
            <el-button type="info" round @click="resume_notice_task" >
              恢复
            </el-button>
          </div>
          <div v-if="!['新建中', '已终止', '已完成'].includes(current_notice_task.task_status) ">
            <el-button type="warning" round @click="stop_notice_task" >
              终止
            </el-button>
          </div>
          <div v-if="['新建中', '已终止', '已完成'].includes(current_notice_task.task_status)">
            <el-popconfirm title="删除后不可找回，是否继续？" @confirm="delete_current_task">
              <template #reference>
                <el-button type="danger" round>
                  删除
                </el-button>
              </template>
            </el-popconfirm>

          </div>
        </div>


      </div>
    </el-header>
    <el-main>
      <el-scrollbar style="height: calc(100vh - 200px)">
        <div id="notice-detail-area" v-loading="task_loading" :element-loading-text="loading_text">
          <el-form label-position="top" inline style="max-width: 925px">
            <el-form-item label="编号" prop="id">
              <el-input v-model="current_notice_task.id" readonly/>
            </el-form-item>
            <el-form-item label="创建用户" prop="user_id">
              <el-input v-model="current_notice_task.user_id" readonly/>
            </el-form-item>
            <el-form-item label="状态" prop="task_status">
              <el-input v-model="current_notice_task.task_status" readonly/>
            </el-form-item>
            <el-form-item label="创建时间">
              <el-input v-model="current_notice_task.create_time" readonly/>
            </el-form-item>
            <el-form-item label="更新时间">
              <el-input v-model="current_notice_task.update_time" readonly/>
            </el-form-item>
            <el-form-item label="启动时间">
              <el-input v-model="current_notice_task.begin_time" readonly/>
            </el-form-item>
            <el-form-item label="完成时间">
              <el-input v-model="current_notice_task.finish_time" readonly/>
            </el-form-item>
            <el-form-item label="通知总数">
              <el-input v-model="current_notice_task.task_instance_total" readonly/>
            </el-form-item>
            <el-form-item label="任务进度" style="width: 100%">
              <el-progress :percentage="current_notice_task.task_progress "
                           status="exception"
                           :text-inside="true" :stroke-width="18"
                           v-if="current_notice_task.task_instance_failed" style="width: 100%"
              />
              <el-progress :percentage="current_notice_task.task_progress "
                           status="success"
                           :text-inside="true" :stroke-width="18"
                           v-else-if="current_notice_task.task_status === '已完成'" style="width: 100%"
              />

              <el-progress :percentage="current_notice_task.task_progress "
                           status="warning"
                           :text-inside="true" :stroke-width="18"  style="width: 100%"
                           v-else-if="current_notice_task.task_status === '已暂停'
                           || current_notice_task.task_status === '已终止'"
              />
              <el-progress :percentage="current_notice_task.task_progress "
                           :text-inside="true" :stroke-width="18"  style="width: 100%"
                           v-else-if="current_notice_task.task_status === '执行中'"
              />
              <el-text v-else>
                暂无进度
              </el-text>
            </el-form-item>
          </el-form>
          <el-form :model="current_notice_task" label-position="top" style="max-width: 925px;width: 100%"
                   ref="notice_task_Ref" :rules="notice_task_rules"
          >
            <el-form-item label="通知主题" prop="task_name" required>
              <el-input v-model="current_notice_task.task_name" :disabled="current_notice_task.task_status!='新建中'"/>
            </el-form-item>
            <el-form-item label="描述" required prop="task_desc">
              <el-input v-model="current_notice_task.task_desc" :disabled="current_notice_task.task_status!='新建中'"/>
            </el-form-item>
            <el-form-item label="通知类型" required prop="notice_type">
              <el-select v-model="current_notice_task.notice_type" :disabled="current_notice_task.task_status!='新建中'">
                <el-option value="站内信" label="站内信"></el-option>
                <el-option value="邮件" label="邮件"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="立刻运行" prop="run_now">
              <el-checkbox v-model="current_notice_task.run_now" :disabled="current_notice_task.task_status!='新建中'"/>
            </el-form-item>
            <el-form-item label="计划开始时间" prop="plan_begin_time" v-if="!current_notice_task.run_now">
              <el-date-picker
                  v-model="current_notice_task.plan_begin_time"
                  type="datetime"
                  placeholder="选择日期时间"
                  :disabled="current_notice_task.task_status!='新建中' || current_notice_task.run_now"
                  style="width: 100%"
              />
            </el-form-item>
            <el-form-item label="计划完成时间" prop="plan_finish_time" v-if="!current_notice_task.run_now">
              <el-date-picker
                  v-model="current_notice_task.plan_finish_time"
                  type="datetime"
                  placeholder="选择日期时间"
                  :disabled="current_notice_task.task_status!='新建中' || current_notice_task.run_now"
                  style="width: 100%"
              />
            </el-form-item>
            <el-form-item label="任务事务大小" prop="task_instance_batch_size" >
              <el-input-number v-model="current_notice_task.task_instance_batch_size"
                        :min="1" :max="1000" :step="10"
                        :disabled="current_notice_task.task_status!='新建中'"/>
            </el-form-item>
            <el-form-item label="通知模板(html)" required prop="notice_template">

              <el-row style="width: 100%">
                <el-col :span="10">
                  <div class="std-middle-box">
                    <el-input type="textarea" :rows="12" v-model="current_notice_task.notice_template"
                              :disabled="current_notice_task.task_status!='新建中'" @blur="check_html_valid">
                    </el-input>
                  </div>
                </el-col>
                <el-col :span="4">
                  <div class="std-middle-box">
                    <el-text>
                      <- 预览区域 ->
                    </el-text>
                  </div>
                </el-col>
                <el-col :span="10">
                  <div id="preview-area">
                    <div v-html="current_notice_task.notice_template" v-if="current_notice_template_valid"/>
                    <div v-else>
                      <el-text>模板内容不合法</el-text>
                    </div>
                  </div>
                </el-col>
              </el-row>



            </el-form-item>
            <el-form-item label="通知范围(取并集)" prop="notice_params">
              <div id="notice-area">
                <el-checkbox-group v-model="area_shortcut"
                                   :disabled="current_notice_task.task_status!='新建中'"
                                   @change="handle_notice_area_change"
                >
                  <el-checkbox label="所有用户" value="all_user"></el-checkbox>
                  <el-checkbox label="所有企业用户" value="all_company_user"></el-checkbox>
                  <el-checkbox label="所有个人用户" value="all_person_user"></el-checkbox>
                  <el-checkbox label="所有订阅邮箱" value="all_subscribe_email"
                               v-if="current_notice_task.notice_type=='邮件'"/>
                  <el-checkbox label="指定公司" value="target_company"></el-checkbox>
                  <el-checkbox label="指定部门" value="target_department"></el-checkbox>
                  <el-checkbox label="指定用户" value="target_user"></el-checkbox>
                </el-checkbox-group>

                <el-select multiple v-model="area_target_companies" v-show="area_shortcut.includes('target_company')"
                           placeholder="请搜索后选择公司" :disabled="current_notice_task.task_status!='新建中'"
                           collapse-tags clearable :remote-method="search_company" remote filterable
                           value-key="id" @change="handle_notice_company_change" :max-collapse-tags="3"
                >
                  <el-option  v-for="item in area_company_options"
                              :label="item.company_name" :value="item" :key="item.id"
                  />
                </el-select>
                <el-select multiple v-model="area_target_departments" v-show="area_shortcut.includes('target_department')"
                           placeholder="请搜索后选择部门" :disabled="current_notice_task.task_status!='新建中'"
                           collapse-tags clearable :remote-method="search_department" remote filterable
                           value-key="id" @change="handle_notice_department_change" :max-collapse-tags="3"
                >
                  <el-option  v-for="item in area_department_options"
                              :label="item.department_name" :value="item" :key="item.id"
                  />
                </el-select>
                <el-select multiple v-model="area_target_users" v-show="area_shortcut.includes('target_user')"
                           placeholder="请搜索后选择用户" :disabled="current_notice_task.task_status!='新建中'"
                           collapse-tags clearable :remote-method="search_user" remote filterable
                           @change="handle_notice_user_change" :max-collapse-tags="3" value-key="user_id"
                >
                  <el-option  v-for="item in area_user_options"
                              :label="item.user_nick_name" :value="item" :key="item.user_id"
                  />
                </el-select>
              </div>


            </el-form-item>


          </el-form>
          <el-divider>
            通知实例列表
          </el-divider>
          <el-scrollbar>
            <div style="width: 100%; max-height: 600px">
              <el-table :data="current_task_instances" stripe >
                <el-table-column type="selection" width="55" />
                <el-table-column prop="id" label="通知ID" sortable/>
                <el-table-column prop="receive_user_id" label="用户ID" sortable/>
                <el-table-column prop="task_celery_id" label="celery-ID" sortable min-width="240px"/>
                <el-table-column prop="notice_type" label="通知类型" sortable/>
                <el-table-column prop="notice_status" label="通知状态" sortable>
                  <template #default="{row}">
                    <el-tag v-if="row.notice_status === '新建中'" type="info">新建中</el-tag>
                    <el-tag v-else-if="row.notice_status === '待执行'" type="info">待执行</el-tag>
                    <el-tag v-else-if="row.notice_status === '执行中'" type="primary">执行中</el-tag>
                    <el-tag v-else-if="row.notice_status === '成功'" type="success">成功</el-tag>
                    <el-tag v-else-if="row.notice_status === '已暂停'" type="warning">已暂停</el-tag>
                    <el-tag v-else-if="row.notice_status === '已终止'" type="danger">已终止</el-tag>
                    <el-tag v-else-if="row.notice_status === '异常'" type="danger">异常</el-tag>
                    <el-tag v-else type="primary">
                      {{ row.notice_status }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="create_time" label="通知时间" sortable min-width="200px"/>
                <el-table-column prop="update_time" label="更新时间" sortable min-width="200px"/>
                <el-table-column fixed label="操作" min-width="200px">
                  <template #default="{row}">
                    <el-button v-if="!['已通知','排队中'].includes(row.notice_status)" disabled type="primary">
                      重发
                    </el-button>
                  </template>

                </el-table-column>



              </el-table>
            </div>
          </el-scrollbar>





        </div>
      </el-scrollbar>


    </el-main>
    <el-footer/>
  </el-container>

</template>

<style scoped>
.std-middle-box{
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;

}
#detail-header-area{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  height: 100%;
  width: 100%;
}
#detail-header-left{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 12px;
  height: 100%;
  width: 100%;
}
#detail-header-right{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
  height: 100%;
  width: 100%;
}
#notice-detail-area{
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}
#preview-area{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  border: 1px solid #ddd; /* 边框颜色和宽度 */
  border-radius: 4px; /* 圆角 */

  background-color: #f9f9f9; /* 背景色 */
}
#notice-area{
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
}
</style>
