<script setup lang="ts">
import {useRoute} from "vue-router";
import {onMounted, ref} from "vue";
import {
  CurrentSessionAssistantList,
  CurrentSessionLogList,
  CurrentSessionPageNum,
  CurrentSessionPageSize, CurrentSessionSource,
  CurrentSessionTotal,
  downCheckTargetSession,
  favoriteHistorySession,
  getSessionLog,
  handleCurrentChange,
  handleSizeChange,
  SessionTimeRangeShortCuts,
  showSessionHistoryMsg,
  showSessionMsg,
  splitTags,
  targetAssistantName,
  targetSession,
  targetSessionFavorite,
  targetSessionRemark,
  targetSessionTag,
  targetSessionTimeRange,
  targetSessionTopic, targetSessionUser,
  upCheckTargetSession
} from "@/components/feedback_center/session_log";
import {Search} from "@element-plus/icons-vue";
import Session_history_msg from "@/components/feedback_center/session_history_msg.vue";
import Prompt_test from "@/components/feedback_center/prompt_test.vue";
import {checkUserPermission} from "@/components/user_center/user";

const route = useRoute();
const current_index = route.path
const filteredComponents = ref([
  {
    name: "检索模式",
    url: "/feedback/search_model"
  }
  ,{
    name: "终端模式",
    url: "/feedback/terminal_model"
  },{
    name: "会话模式",
    url: "/feedback/qa_model"
  },
])
onMounted(async () => {
  CurrentSessionSource.value = "next_console"
  await getSessionLog();
})
const up_session_icon_hover = ref(false)
const down_session_icon_hover = ref(false)
async function handle_session_drawer_up(){
  await upCheckTargetSession()
}
async function handle_session_drawer_down(){
  await downCheckTargetSession()
}
function handle_session_drawer_open(){
  window.addEventListener('keydown', function(e) {
    if (e.key === 'ArrowUp') {
      handle_session_drawer_up()
    }
    else if (e.key === 'ArrowDown') {
      handle_session_drawer_down()
    }
  });
}
function handle_session_drawer_close(){
  window.removeEventListener('keydown', function(e) {
    if (e.key === 'ArrowUp') {
      handle_session_drawer_up()
    }
    else if(e.key === 'ArrowDown') {
      handle_session_drawer_down()
    }
  });
}
onMounted(async ()=>{
  await checkUserPermission()
})

</script>

<template>
  <el-container style="height: 100vh">
    <el-header height="61px">
      <div class="next-console-admin-header">

        <div class="component-box">
          <el-menu
              :default-active="current_index"
              class="el-menu-demo"
              mode="horizontal"
              router
              :ellipsis="false"

          >
            <el-menu-item v-for="component in filteredComponents"

                          :index=component.url
                          class="menu-header-item"
            >

                {{ component.name }}


            </el-menu-item>
          </el-menu>
        </div>



      </div>
    </el-header>
    <el-main>

      <div style="height: calc(100vh - 170px)">
        <el-scrollbar>
        <div style="display: flex;flex-direction: row;width: 100%; justify-content: space-between">
          <div style="width: 120px;display: flex;align-content: center">
            <el-text class="next-console-font-bold" style="width: 60px;">
              会话日志
            </el-text>
          </div>
          <div style="display: flex;flex-direction: row;width: 100%; justify-content: flex-end; gap: 8px">
            <div style="width: 120px">
              <el-input v-model="targetSessionUser" placeholder="目标用户id"
                        clearable
                        @change="getSessionLog">

              </el-input>
            </div>
            <div style="width: 120px">
              <el-select v-model="targetAssistantName" placeholder="切换助手"
                         clearable
                         @change="getSessionLog">
                <el-option :value="name" v-for="(name,_) in CurrentSessionAssistantList"/>
              </el-select>
            </div>
            <div style="width: 120px">
              <el-select v-model="targetSessionRemark" placeholder="会话评价"
                         @change="getSessionLog" clearable>
                <el-option :value="-1" label="点踩"/>
                <el-option :value="0" label="未评价"/>
                <el-option :value="1" label="点赞"/>
              </el-select>
            </div>
            <div style="width: 120px">
              <el-select v-model="targetSessionFavorite" placeholder="会话收藏"
                         @change="getSessionLog"
                         clearable>
                <el-option :value="0" label="未收藏"/>
                <el-option :value="1" label="收藏"/>
              </el-select>
            </div>
            <div style="width: 380px">
              <el-date-picker
                  style="width: 350px"
                  @change="getSessionLog"
                  v-model="targetSessionTimeRange"
                  type="datetimerange"
                  :shortcuts="SessionTimeRangeShortCuts"
                  range-separator="至"
                  start-placeholder="开始时间"
                  end-placeholder="截止时间"
              />
            </div>
            <div style="width: 180px">
              <el-input
                  v-model="targetSessionTopic"
                  placeholder="搜索会话标题"
                  :prefix-icon="Search"
                  @change="getSessionLog"
                  clearable
              />
            </div>
            <div style="width: 180px">
              <el-input
                  v-model="targetSessionTag"
                  placeholder="搜索会话标签"
                  @change="getSessionLog"
                  clearable
                  :prefix-icon="Search"
              />
            </div>
          </div>
        </div>
        <div>
          <el-table
              :data="CurrentSessionLogList"
              style="width: 100%"
              show-overflow-tooltip
              stripe>
            <el-table-column type="selection" width="55" />
            <el-table-column prop="session_id" label="会话id" width="80" sortable/>
            <el-table-column prop="user_id" label="用户id" width="80" sortable />
            <el-table-column prop="assistant_name" label="助手"  />
            <el-table-column prop="session_topic" label="会话标题"  />
            <el-table-column prop="qa_cnt" label="QA数" width="60" sortable />
            <el-table-column prop="msg_token_used" label="消耗Token数" width="120" sortable />
            <el-table-column prop="session_end_time" label="更新时间"  width="180" sortable />
            <el-table-column prop="tag_name" label="标记标签" width="200" :show-overflow-tooltip="true">
              <template #default="{row}">
                <div style="display:flex; align-content: center;flex-direction: row;gap: 6px;flex-wrap: wrap">
                  <el-tag v-for="tag in splitTags(row.tag_name)" :key="tag" effect="light">
                    {{ tag }}
                  </el-tag>
                </div>

              </template>
            </el-table-column>
            <el-table-column prop="session_remark" label="用户反馈">
              <template #default="{row}">
                 <el-tag v-if="row.session_remark ==-1" type="danger" round>
                   点踩
                 </el-tag>
                <el-tag v-if="row.session_remark ==0" type="info" round>
                  未评价
                </el-tag>
                <el-tag v-if="row.session_remark ==1" type="success" round>
                  点赞
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="admin_session_remark" label="管理员反馈">
              <template #default="{row}">
                <el-tag v-if="row.admin_session_remark ==-1" type="danger" round>
                  点踩
                </el-tag>
                <el-tag v-if="row.admin_session_remark ==0" type="info" round>
                  未评价
                </el-tag>
                <el-tag v-if="row.admin_session_remark ==1" type="success" round>
                  点赞
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="session_favorite" label="用户收藏">
              <template #default="{row}">
                <el-image v-if="row.session_favorite == 1"
                        style="width: 24px;height: 24px;"
                        src="images/star_icon_yellow.svg"
                />

                <el-image v-else-if="row.session_favorite == 0"
                          style="width: 24px;height: 24px;"
                          src="images/star_icon_grey.svg"
                />
              </template>
            </el-table-column>
            <el-table-column prop="session_favorite" label="管理员收藏">
              <template #default="{row}">
                <el-image v-if="row.admin_session_favorite == 1"
                          style="width: 24px;height: 24px;"
                          src="images/star_icon_yellow.svg"
                />

                <el-image v-else-if="row.admin_session_favorite == 0"
                          style="width: 24px;height: 24px;"
                          src="images/star_icon_grey.svg"
                />
              </template>
            </el-table-column>
            <el-table-column label="操作" fixed='right'>
              <template #default="{row}">
                <div style="cursor: pointer" @click="showSessionMsg(row)">
                  <el-image style="width: 20px;height: 20px"
                            src="images/icon_circle_grey.svg"
                  />

                </div>

              </template>
            </el-table-column>

          </el-table>


        </div>
        </el-scrollbar>
      </div>
      <el-drawer v-model="showSessionHistoryMsg" size="80%"
                 @open="handle_session_drawer_open"
                 @closed="handle_session_drawer_close">
        <template #header>
          <div v-if="targetSession"
               style="width: 100%;display: flex;flex-direction: row;justify-content: space-between;align-content: center">
            <div class="next-console-div" >
              <div>
                <el-text class="next-console-font-bold">{{ targetSession.session_topic }}</el-text>
              </div>
              <div>
                <div style="cursor: pointer" @click="favoriteHistorySession()">
                  <el-image v-if="targetSession.admin_session_favorite ==1"
                            src="images/star_icon_yellow.svg"
                            style="width: 24px;height: 24px;"
                  />
                  <el-image v-else
                            src="images/star_icon_grey.svg"
                            style="width: 24px;height: 24px;"
                  />
                </div>
              </div>

            </div>
            <div class="next-console-div">
              <div class="next-console-div"
                   @mouseenter="up_session_icon_hover=true"
                   @mouseleave="up_session_icon_hover=false" @click="upCheckTargetSession">
                <el-image v-if="up_session_icon_hover"
                          src="images/arrow_up_blue.svg"
                          style="width: 14px;height: 14px;cursor: pointer"/>

                <el-image v-else src="images/arrow_up_grey.svg" style="width: 14px;height: 14px;cursor: pointer"/>
              </div>
              <div class="next-console-div" @mouseenter="down_session_icon_hover=true"
                   @mouseleave="down_session_icon_hover=false" @click="downCheckTargetSession">
                <el-image v-if="down_session_icon_hover"
                          src="images/arrow_down_blue.svg"
                          style="width: 14px;height: 14px;cursor: pointer"/>
                <el-image v-else src="images/arrow_down_grey.svg" style="width: 14px;height: 14px;cursor: pointer"/>
              </div>

            </div>
          </div>

        </template>
        <session_history_msg/>
      </el-drawer>
      <prompt_test/>
    </el-main>
    <el-footer >
      <div class="kg-pagination" >
        <el-pagination
            :small="true"
            layout=" total, sizes, prev, pager, next"
            :total="CurrentSessionTotal"
            :page-sizes="[100,200,500,1000]"
            :page-size="CurrentSessionPageSize"
            :current-page="CurrentSessionPageNum"
            @update:page-size="handleSizeChange"
            @update:current-page="handleCurrentChange"
        />
      </div>
    </el-footer>
  </el-container>
</template>

<style scoped>
.el-header {
  --el-header-padding : 0 !important;
}
.kg-pagination{
  display: flex;
  justify-content: center;
  align-content: center;
  width: 100%;
  height: 100%;
}

</style>
