<script setup lang="ts">

import {
  current_model,
  search_new_friends_list,
  current_friend,
  current_friend_list,
  current_search_friends,
  enter_add_model,
  exit_add_model,
  exit_search_model,
  friend_loading,
  friend_search_keyword,
  init_current_friend_list,
  new_friend_search_keyword,
  search_friend_list,
  search_new_friends,
  set_current_friend,
  auto_exit_search_model,
  show_delete_confirm_flag,
  confirm_delete_friend,
  auto_handle_search_blur,
  auto_handle_add_blur,
  set_current_new_friend,
  current_new_friend,
  send_add_friend_request,
  enter_history_model,
  history_friends, handle_accept, handle_reject, friends_width, back_friends_list
} from "@/components/contacts/friends/friends";
import {onMounted} from "vue";
import { Search ,CirclePlus} from '@element-plus/icons-vue'
import {user_info} from "@/components/user_center/user";
onMounted(async ()=>{
  init_current_friend_list()
})
const phone_view = window.innerWidth < 768
const dialog_width = phone_view ? '90vw' : '600px'
</script>

<template>
  <el-container>
    <el-header style="padding: 0 !important;">
      <div id="friend_area">
        <el-text id="friend_area_title">
          外部联系人
        </el-text>
      </div>
    </el-header>
    <el-container style="margin-top: 4px" v-loading="friend_loading">
      <el-aside style="border-right: 1px solid #E9EBF0;" :width="friends_width">
        <el-scrollbar>
          <div id="friend_list_area">
            <div id="friend_search_area" v-show="current_model != 'add' ">
                <div class="std-middle-box">
                  <el-input placeholder="搜索好友" clearable v-model="friend_search_keyword"
                            @focus="current_model='search'" @clear="exit_search_model"
                            @change="auto_exit_search_model" @blur="auto_handle_search_blur()"
                            @keydown.enter="search_friend_list()"
                             >
                    <template #prefix>
                      <el-icon style="cursor: pointer;" @click="search_friend_list">
                        <Search/>
                      </el-icon>
                    </template>
                  </el-input>

                </div>

               <el-tooltip effect="light" placement="right" content="添加好友">
                 <div class="std-middle-box" style="cursor: pointer" @click="enter_add_model()">
                   <el-image src="images/add_friend.svg" style="width: 20px; height: 20px"/>
                 </div>
               </el-tooltip>

            </div>
            <div id="friend_search_area" v-show="current_model == 'add' ">
              <div class="std-middle-box">
                <el-input placeholder="搜索新的朋友 by 邮箱" clearable v-model="new_friend_search_keyword"
                          @focus="current_model='add'" @blur="auto_handle_add_blur()"
                          @keydown.enter="search_new_friends_list()"
                          style="width: 100%" >
                  <template #prefix>
                    <el-icon style="cursor: pointer;" @click="search_new_friends_list">
                      <CirclePlus/>
                    </el-icon>
                  </template>
                </el-input>
              </div>
              <div class="std-middle-box" style="cursor: pointer"   @click="exit_add_model()">
                <el-text style="width: 30px"> 取消</el-text>
              </div>
            </div>
            <div id="new_friend" @click="enter_history_model()">
              <div class="std-middle-box" style="background-color: orange;padding: 6px;">
                <el-image src="images/new_friend.svg" style="width: 32px;height: 32px;"/>
              </div>
              <div>
                <el-text>新的朋友</el-text>
              </div>

            </div>

            <div class="friend-type-box" v-for="(item,idx) in current_friend_list"
                 @click="set_current_friend(item)"
                 v-show="current_model == 'list' || current_model == 'history'"
                 :class="{'friend-type-box-active': current_friend?.user_id == item.user_id}">
              <div class="std-middle-box">
                <el-avatar :src="item?.user_avatar" style="background-color: white" v-if="item?.user_avatar"/>
                <el-avatar  style="background-color: #D1E9FF" v-else>
                  <el-text style="font-weight: 600;color: #1570ef">{{item?.user_nick_name_py}}</el-text>
                </el-avatar>
              </div>
              <div class="std-middle-box">
                <el-text>
                  {{item?.user_nick_name}}
                </el-text>
              </div>

            </div>
            <div class="friend-type-box" v-for="(item,idx) in current_search_friends"
                 @click="set_current_friend(item)"
                  v-show='current_model == "search" '
                 :class="{'friend-type-box-active': current_friend?.user_id == item.user_id}">
              <div class="std-middle-box">
                <el-avatar :src="item?.user_avatar" style="background-color: white" v-if="item?.user_avatar"/>
                <el-avatar  style="background-color: #D1E9FF" v-else>
                  <el-text style="font-weight: 600;color: #1570ef">{{item?.user_nick_name_py}}</el-text>
                </el-avatar>
              </div>
              <div class="std-middle-box">
                <el-text>
                  {{item?.user_nick_name}}
                </el-text>
              </div>
            </div>
            <div class="friend-type-box" v-for="(item,idx) in search_new_friends"
                 @click="set_current_new_friend(item)"
                 v-show='current_model == "add" '
                 :class="{'friend-type-box-active': current_friend?.user_id == item?.user_id}">
              <div class="std-middle-box">
                <el-avatar :src="item?.user_avatar" style="background-color: white" v-if="item?.user_avatar"/>
                <el-avatar  style="background-color: #D1E9FF" v-else>
                  <el-text style="font-weight: 600;color: #1570ef">{{item?.user_nick_name_py}}</el-text>
                </el-avatar>
              </div>
              <div class="std-middle-box">
                <el-text>
                  {{item?.user_nick_name}}
                </el-text>
              </div>
            </div>
            <div v-show="!current_friend_list?.length && current_model== 'list'" class="empty-box">
              <el-empty description="暂无好友，赶快去添加吧~"/>
            </div>
            <div v-show="!current_search_friends?.length && current_model== 'search'" class="empty-box"  >
              <el-empty description="暂无搜索结果"/>
            </div>
            <div v-show="!search_new_friends?.length && current_model== 'add'" class="empty-box">
              <el-empty description="暂无搜索结果"/>
            </div>
          </div>
        </el-scrollbar>


      </el-aside>
      <el-main style="height: calc(100vh - 100px); padding: 0 !important;">
        <div id="back-friends" v-if="phone_view" style="margin-left: 30px">
          <el-button type="text" @click="back_friends_list" v-if="phone_view">
            返回
          </el-button>
        </div>
        <div id="show-info-area" v-show="current_model!='history'">
          <div id="show-info-box" v-if="current_friend?.user_id">
            <div id="show-info-head">
              <div id="show-info-head-left">
                <div class="std-middle-box" style="gap: 6px">
                  <div class="std-middle-box">
                    <el-text style="font-size: 18px">
                      {{ current_friend?.user_nick_name }}
                    </el-text>
                  </div>
                  <div class="std-middle-box">
                    <el-image src="images/male.svg" style="width: 16px;height: 16px;"
                              v-show="current_friend?.user_gender=='男'"/>
                    <el-image src="images/female.svg" style="width: 16px;height: 16px;"
                              v-show="current_friend?.user_gender=='女'"/>
                  </div>
                </div>
                <div class="std-middle-box" style="justify-content: flex-start">
                  <el-text>{{ current_friend?.user_position }}</el-text>
                </div>


              </div>
              <div class="std-middle-box">
                <el-avatar :src="current_friend?.user_avatar" style="width: 60px; height: 60px;background-color: white"/>
              </div>

            </div>
            <div id="show-info-body">
              <div class="show-info-meta-item">
                <div>
                  <el-text>部门</el-text>
                </div>
                <div>
                  <el-text>{{current_friend?.user_department}}</el-text>
                </div>
              </div>
              <div class="show-info-meta-item">
                <div>
                  <el-text>企业</el-text>
                </div>
                <div class="std-middle-box" style="gap: 6px">
                  <el-text>{{current_friend?.user_company}}</el-text>
                  <el-image src="images/certification.svg"
                            v-show="current_friend?.user_account_type=='企业账号'"
                            style="width: 20px; height: 20px"/>
                </div>

              </div>
              <div class="show-info-meta-item">
                <div>
                  <el-text>邮箱</el-text>
                </div>
                <div class="std-middle-box" style="gap: 6px">
                  <el-text>{{current_friend?.user_email}}</el-text>

                </div>

              </div>
            </div>
            <div id="show-info-foot">
              <div class="std-middle-box">
                <el-button type="primary" disabled>
                  发消息
                </el-button>
              </div>

              <div class="std-middle-box">
                <el-button type="danger" @click="show_delete_confirm_flag=true">
                  删除
                </el-button>
              </div>
            </div>
          </div>
          <div id="show-info-box" v-else-if="current_new_friend?.user_id">
            <div id="show-info-head">
              <div id="show-info-head-left">
                <div class="std-middle-box" style="gap: 6px">
                  <div class="std-middle-box">
                    <el-text style="font-size: 18px">
                      {{ current_new_friend?.user_nick_name }}
                    </el-text>
                  </div>
                  <div class="std-middle-box">
                    <el-image src="images/male.svg" style="width: 16px;height: 16px;"
                              v-show="current_new_friend?.user_gender=='男'"/>
                    <el-image src="images/female.svg" style="width: 16px;height: 16px;"
                              v-show="current_new_friend?.user_gender=='女'"/>
                  </div>
                </div>
                <div class="std-middle-box" style="justify-content: flex-start">
                  <el-text>{{ current_new_friend?.user_position }}</el-text>
                </div>


              </div>
              <div class="std-middle-box">
                <el-avatar :src="current_new_friend?.user_avatar" style="width: 60px; height: 60px;background-color: white"/>
              </div>

            </div>
            <div id="show-info-body">
              <div class="show-info-meta-item">
                <div>
                  <el-text>部门</el-text>
                </div>
                <div>
                  <el-text>{{current_new_friend?.user_department}}</el-text>
                </div>
              </div>
              <div class="show-info-meta-item">
                <div>
                  <el-text>企业</el-text>
                </div>
                <div class="std-middle-box" style="gap: 6px">
                  <el-text>{{current_new_friend?.user_company}}</el-text>
                  <el-image src="images/certification.svg"
                            v-show="current_new_friend?.user_account_type=='企业账号'"
                            style="width: 20px; height: 20px"/>
                </div>

              </div>
              <div class="show-info-meta-item">
                <div>
                  <el-text>邮箱</el-text>
                </div>
                <div class="std-middle-box" style="gap: 6px">
                  <el-text>{{current_new_friend?.user_email}}</el-text>

                </div>

              </div>
            </div>
            <div id="show-info-foot">
              <div class="std-middle-box" v-show="!current_new_friend?.rel_status
              || (current_new_friend?.rel_status?.rel_status >=2) ">
                <el-button type="primary" @click="send_add_friend_request()">
                  添加好友
                </el-button>
              </div>
              <div class="std-middle-box" v-show="current_new_friend?.rel_status?.rel_status == 1">
                <el-button type="primary">
                  发送信息
                </el-button>
              </div>
              <div class="std-middle-box" v-show="current_new_friend?.rel_status?.rel_status == -1
              && current_new_friend?.rel_status?.friend_id == user_info?.user_id">
                <el-button disabled type="info">
                  已拒绝
                </el-button>
              </div>
              <div class="std-middle-box" v-show="current_new_friend?.rel_status?.rel_status == -1
              && current_new_friend?.rel_status?.user_id == user_info?.user_id">
                <el-button disabled type="danger">
                  被拒绝
                </el-button>
              </div>
              <div class="std-middle-box" v-show="current_new_friend?.rel_status?.rel_status == 0">
                <el-button disabled type="info">
                  申请中
                </el-button>
              </div>
            </div>
          </div>
          <div id="show-info-box" v-else>
            <el-text>
              请选择一个好友查看详细信息
            </el-text>
          </div>

        </div>
        <div id="show-history-area" v-show="current_model=='history'">
          <el-scrollbar>
            <div id="show-history-box">
              <div v-for="(record,idx) in history_friends" class="history-record-box">
                <div class="std-middle-box">
                  <el-avatar :src="record?.user_avatar" style="width: 40px;height: 40px;background-color: white"/>
                </div>
                <div class="std-middle-box" style="width: 100%;justify-content: flex-start">
                  <el-text>{{record?.user_nick_name}}</el-text>
                </div>
                <div class="std-middle-box" style="min-width: 60px">
                  <el-text v-show="record.rel_status?.rel_status == 1">
                    已添加
                  </el-text>
                  <el-text v-show="record.rel_status?.rel_status == -1">
                    已拒绝
                  </el-text>
                  <el-button v-show="record.rel_status?.rel_status == 0
                  && record.rel_status?.friend_id == user_info.user_id"
                             @click="handle_accept(record.rel_status)" type="success">
                    接受
                  </el-button>
                  <el-button v-show="record.rel_status?.rel_status == 0
                  && record.rel_status?.friend_id == user_info.user_id"
                             @click="handle_reject(record.rel_status)" type="warning">
                    拒绝
                  </el-button>
                  <el-text v-show="record.rel_status?.rel_status == 0
                  && record.rel_status?.user_id == user_info.user_id"  >
                    申请中
                  </el-text>
                  <el-text v-show="record.rel_status?.rel_status > 1">
                    已删除
                  </el-text>
                </div>

              </div>

            </div>
          </el-scrollbar>

        </div>
      </el-main>

    </el-container>
    <el-dialog v-model="show_delete_confirm_flag" title="删除好友" :width="dialog_width">
      <el-result icon="warning" title="确定删除好友吗？"
                 :sub-title="`将清除所有历史记录并不再接受到${current_friend?.user_nick_name}发送的任何消息`"/>
      <div style="display: flex;flex-direction: row;align-items: center;justify-content: center;gap: 12px">
        <el-button type="primary" @click="show_delete_confirm_flag=false">取消</el-button>
        <el-button type="danger" @click="confirm_delete_friend()">删除</el-button>
      </div>
    </el-dialog>
  </el-container>

</template>

<style scoped>
.std-middle-box{
  display: flex;
  justify-content: center;
  align-items: center;
}
#friend_area{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  width: 100%;
  height: 56px;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, .1);
}
#friend_area_title{
  font-size: 20px;
  font-weight: 600;
  color: #333333;
  margin-left: 24px;
  cursor: default;
}
#friend_list_area{
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  width: 100%;
  height: calc(100vh - 200px);
}
.friend-type-box{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 6px;
  padding: 12px;
  cursor: pointer;
  border-radius: 8px;
  width: calc(100% - 24px);
}
.friend-type-box:hover{
  background-color: #F5F7FA;
}
.friend-type-box-active{
  background-color: #E9EBF0;
}
#show-info-area{
  display: flex;
  flex-direction: row;
  width: calc(100% - 32px);
  height: calc(100% - 32px);
  align-items: center;
  justify-content: center;
  padding: 16px;
}
#show-info-box{
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  max-width: 400px;
  align-items: center;
  justify-content: center;
}
#show-info-foot{
  display: flex;
  flex-direction: row;
  gap: 12px;
  align-items: center;
  justify-content: space-around;
  width: 100%;
  height: 60px;
}
#show-info-head{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  width: calc(100% - 32px);
  padding: 12px 16px;
}
#show-info-head-left{
  display: flex;
  flex-direction: column;
  gap: 6px;

}
#show-info-body{
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 12px 16px;
  border-top: 1px solid #E9EBF0;
  width: calc(100% - 32px);
}
.show-info-meta-item{
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  width: 100%;
  gap: 24px;
  align-items: center;
}
#friend_search_area{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding: 4px 12px;
  width: calc(100% - 24px);
}
#new_friend{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  padding: 12px;
  width: calc(100% - 24px);
  gap: 6px;
  cursor: pointer;
  border-radius: 8px;
}
#new_friend:hover{
  background-color: #F5F7FA;
}
.new_friend-active{
  background-color: #E9EBF0;
}
.empty-box{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  width: 100%;
}
#show-history-area{
  display: flex;
  flex-direction: row;
  width: calc(100% - 32px);
  height: calc(100% - 32px);
  align-items: center;
  justify-content: center;
  padding: 16px;
}
#show-history-box{
  display: flex;
  flex-direction: column;
  gap: 6px;
  width: calc(100vw - 900px);
  height: calc(100vh - 200px);
}
.history-record-box{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding: 6px 24px;
  gap: 12px;
  border-bottom: 1px solid #E9EBF0;
}
@media (width < 768px) {
  #friend_area_title{
    font-size: 16px;
    font-weight: 600;
    margin-left: 30px;

  }
  #show-history-box{
    display: flex;
    flex-direction: column;
    gap: 6px;
    width: calc(100vw - 90px);
    height: calc(100vh - 200px);
  }
  .history-record-box{
    padding: 6px 12px;
  }
}
</style>
