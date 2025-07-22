<script setup lang="ts">

import {current_company} from "@/components/contacts/contacts_panel/contacts_panel";
import {
  auto_exit_search_model,
  auto_handle_search_blur,
  back_company_lists,
  company_structure_width,
  current_colleague,
  current_company_structure_data,
  current_company_structure_Ref,
  current_department,
  current_item_type,
  current_model,
  current_search_keyword,
  exit_search_model,
  get_company_structure_tree,
  init_company_structure_tree,
  props,
  search_company_department_and_colleague,
  search_department_colleague_data,
  set_current_item_type
} from "@/components/contacts/company_structure/company_structure";
import {onMounted} from "vue";
import {Search} from "@element-plus/icons-vue";
import router from "@/router";
import {user_info} from "@/components/user_center/user";

onMounted(async ()=>{
  init_company_structure_tree()
})
const phone_view= window.innerWidth < 768
</script>

<template>
  <el-container>
    <el-header style="padding: 0 !important;" v-if="current_company?.id">
      <div id="company_name_area">
        <el-text id="company_name">
          {{current_company?.company_name}}
        </el-text>
      </div>

    </el-header>
    <el-container>

      <el-aside style="border-right: 1px solid #E9EBF0;" v-if="current_company?.id" :width="company_structure_width">
        <el-scrollbar>
          <div style="height: calc(100vh - 200px)">
            <div id="colleague_search_area">
              <div class="std-middle-box" style="width: 100%">
                <el-input placeholder="搜索" v-model="current_search_keyword" clearable
                          @focus="current_model='search'" @clear="exit_search_model"
                          @change="auto_exit_search_model" @blur="auto_handle_search_blur"
                          @keydown.enter.prevent="search_company_department_and_colleague"
                >
                  <template #prefix>
                    <el-icon style="cursor: pointer;" @click="search_company_department_and_colleague">
                      <Search/>
                    </el-icon>
                  </template>
                </el-input>
              </div>
              <el-tooltip effect="light" placement="right" content="发起群聊" v-if="false">
                 <el-button type="primary" disabled text>
                  <el-text   style="font-size: 20px;font-weight: 500">
                    +
                  </el-text>
                 </el-button>
              </el-tooltip>
            </div>
            <el-tree :data="current_company_structure_data" :lazy="true" :load="get_company_structure_tree"
                     :props="props" :expand-on-click-node="true" :highlight-current="true"
                     node-key="structure_id" ref="current_company_structure_Ref"
                     @current-change="" v-show="current_model == 'tree'">
              <template  #default="{ node, data }">
                <div class="tree-button" @click="set_current_item_type(node, data)" >
                  <div class="std-middle-box">
                    <el-avatar :src="data?.user_avatar" style="width: 36px; height: 36px;background-color: white"
                               v-if="data?.structure_type=='colleague' && data?.user_avatar"/>
                    <el-avatar v-else-if="data?.structure_type=='colleague' && !data?.user_avatar" style="background: #D1E9FF">
                      <el-text style="font-weight: 600;color: #1570ef">{{data?.user_nick_name_py}}</el-text>
                    </el-avatar>
                    <el-avatar :src="data?.department_logo" style="width: 36px; height: 36px;background-color: white"
                               v-else-if="data?.structure_type=='department'"/>
                  </div>
                  <div>
                    <el-text>{{ node.data.label }}</el-text>
                  </div>
                </div>
                <div v-if="node.data.roles?.length>0" class="role_list">
                  <el-tag v-for="role in node.data.roles" size="small">
                    {{role.role_desc}}
                  </el-tag>
                </div>
              </template>
            </el-tree>
            <el-tree :data="search_department_colleague_data" :lazy="true" :load="get_company_structure_tree"
                     :props="props" :expand-on-click-node="true" :highlight-current="true"
                     node-key="structure_id" ref="current_company_structure_Ref"
                     @current-change="" v-show="current_model == 'search'">

              <template  #default="{ node, data }">
                <div class="tree-button"
                     @click="set_current_item_type(node, data)" >
                  <div class="std-middle-box">
                    <el-avatar :src="data?.user_avatar" style="width: 36px; height: 36px;background-color: white"
                               v-if="data?.structure_type=='colleague' && data?.user_avatar"/>
                    <el-avatar v-else-if="data?.structure_type=='colleague' && !data?.user_avatar"
                               style="width: 36px; height: 36px;background: #D1E9FF">
                      <el-text style="font-weight: 600;color: #1570ef">{{data?.user_nick_name_py}}</el-text>
                    </el-avatar>
                    <el-avatar :src="data?.department_logo" style="width: 36px; height: 36px;background-color: white"
                               v-show="data?.structure_type=='department'"/>
                  </div>
                  <div>
                    <el-text>{{ node.data.label }}</el-text>
                  </div>
                </div>
              </template>
            </el-tree>
            <div class="std-middle-box" style="width: 100%;margin-top: 12px"
                 v-show="current_model=='tree' && current_company?.user_count">
              <el-text>共{{current_company?.user_count}}人</el-text>
            </div>
          </div>
        </el-scrollbar>
      </el-aside>

      <el-main style="height: calc(100vh - 100px); padding: 0 !important;">
        <div id="back-friends" v-if="phone_view" style="margin-left: 30px">
          <el-button type="text" @click="back_company_lists" v-if="phone_view">
            返回
          </el-button>
        </div>
        <div id="show-info-area" v-if="current_company?.id">

          <div id="show-info-box" v-show="current_item_type=='colleague' && current_colleague?.user_id">
            <div id="show-info-head">
              <div id="show-info-head-left">
                <div class="std-middle-box" style="gap: 6px">
                  <div class="std-middle-box">
                    <el-text style="font-size: 18px">
                      {{ current_colleague?.user_nick_name }}
                    </el-text>
                  </div>
                  <div class="std-middle-box">
                    <el-image src="images/male.svg" style="width: 16px;height: 16px;"
                              v-show="current_colleague?.user_gender=='男'"/>
                    <el-image src="images/female.svg" style="width: 16px;height: 16px;"
                              v-show="current_colleague?.user_gender=='女'"/>
                  </div>
                </div>
                <div class="std-middle-box" style="justify-content: flex-start">
                  <el-text>{{ current_colleague?.user_position }}</el-text>
                </div>


              </div>
              <div class="std-middle-box">
                <el-avatar :src="current_colleague?.user_avatar" style="width: 60px; height: 60px;background-color: white"/>
              </div>

            </div>

            <div id="show-info-body">
              <div class="show-info-meta-item">
                <div>
                  <el-text>姓名</el-text>
                </div>
                <div>
                  <el-text>{{current_colleague?.user_name}}</el-text>
                </div>
              </div>
              <div class="show-info-meta-item">
                <div>
                  <el-text>部门</el-text>
                </div>
                <div>
                  <el-text>{{current_colleague?.user_department}}</el-text>
                </div>
              </div>
              <div class="show-info-meta-item">
                <div>
                  <el-text>企业</el-text>
                </div>
                <div class="std-middle-box" style="gap: 6px">
                  <el-text>{{current_colleague?.user_company}}</el-text>
                  <el-image src="images/certification.svg" style="width: 20px; height: 20px"/>
                </div>

              </div>
              <div class="show-info-meta-item">
                <div>
                  <el-text>邮箱</el-text>
                </div>
                <div class="std-middle-box" style="gap: 6px">
                  <el-text>{{current_colleague?.user_email}}</el-text>

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
                <el-button disabled>
                  写邮件
                </el-button>
              </div>
              <div class="std-middle-box">
                <el-button disabled>
                  语音通话
                </el-button>
              </div>
            </div>

          </div>
          <div id="show-info-box" v-show="current_item_type=='department'">
            <div>
              <el-text>
                {{current_department?.department_name}}
              </el-text>
            </div>
            <div v-show="current_department?.user_count">
              <el-text>
                - {{current_department?.user_count}}人 -
              </el-text>
            </div>

          </div>

        </div>
        <div v-else  id="show-info-area">
             <div id="show-info-box" style="gap: 16px">
               <div>
                 <el-image src="images/empty_company_logo.svg" style="height: 160px; width: 220px"/>
               </div>
               <div>
                  <el-text style="font-size: 24px;font-weight: 600;color: #333333">
                    企业联系人为空
                  </el-text>
               </div>
                <div>
                  <el-text style="font-size: 16px;color: #475467">
                    请联系平台升级为企业用户，尊享更多企业级功能
                  </el-text>
                </div>
             </div>
        </div>
      </el-main>

    </el-container>
  </el-container>

</template>

<style scoped>
#company_name_area{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  width: 100%;
  height: 56px;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, .1);
}
#company_name{
  font-size: 20px;
  font-weight: 600;
  color: #333333;
  margin-left: 24px;
  cursor: default;
}
.std-middle-box{
  display: flex;
  justify-content: center;
  align-items: center;
}
:deep(.el-tree-node__content){
  height: 50px;
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
.tree-button{
  display: flex;
  flex-direction: row;
  gap: 6px;
  align-items: center;
  justify-content: flex-start;
  height: 40px;
  width: 100%;
}
#show-info-foot{
  display: flex;
  flex-direction: row;
  gap: 12px;
  align-items: center;
  justify-content: center;
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
#colleague_search_area{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding: 4px 12px;
  width: calc(100% - 24px);
}
.role_list{
  display: flex;
  flex-direction: row;
  gap: 6px;
  flex-wrap: wrap;
  margin-right: 12px;
}
@media (width < 768px) {
  #company_name{
    font-size: 16px;
    font-weight: 600;
    margin-left: 30px;



  }
}
</style>
