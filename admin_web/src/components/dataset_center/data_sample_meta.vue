<script setup lang="ts">

import {
  check_next_data_sample,
  current_data_sample,
  current_result_json_schema,
  current_smale_detail_model,
  data_sample_detail_loading,
  show_target_data_sample_drawer
} from "@/components/dataset_center/data_samples";
import {onMounted} from "vue";
import {current_sample_tags, update_current_data_sample_tags} from "@/components/dataset_center/data_sample_tags";
import Data_sample_context from "@/components/dataset_center/data_sample_context.vue";
import {omit_text} from "@/utils/base";

onMounted(async () => {


});



</script>

<template>
   <el-drawer v-model="show_target_data_sample_drawer" v-loading="data_sample_detail_loading"
              element-loading-text="详情加载中..." size="80%" class="data-sample-drawer"
              @keydown.down="check_next_data_sample(1)"
              @keydown.up="check_next_data_sample(-1)"
   >
     <template #header>
       <div id="drawer-header">
         <div class="middle-box" style="gap: 6px;margin-right: 24px">
           <div class="middle-box" style="min-width: 80px">
             <el-text style="font-weight: 600;line-height: 28px;font-size: 18px;color: #101828">
               {{current_data_sample.id}}
             </el-text>
           </div>
           <div class="middle-box">
              <el-text style="font-weight: 600;line-height: 28px;font-size: 18px;color: #101828"
                       v-if="current_data_sample.msg_content?.length< 200"
              >
                {{current_data_sample.msg_content}}
              </el-text>
             <el-popover v-else width="60vw">
               <template #reference>
                 <el-text style="font-weight: 600;line-height: 28px;font-size: 18px;color: #101828">
                   {{omit_text(current_data_sample.msg_content, 200)}}
                 </el-text>
               </template>

               <el-text >
                 {{current_data_sample.msg_content}}
               </el-text>
             </el-popover>
           </div>
         </div>
         <div id="drawer-header-button-box">
           <div class="middle-box" style="cursor: pointer" @click="check_next_data_sample(-1)">
             <el-image src="images/arrow_up_grey.svg" style="width: 14px;height: 14px"/>
           </div>
           <div class="middle-box" style="cursor: pointer" @click="check_next_data_sample(1)">
             <el-image src="images/arrow_down_grey.svg" style="width: 14px;height: 14px"/>
           </div>
         </div>
       </div>

     </template>
     <el-scrollbar>
     <div>

       <el-tabs v-model="current_smale_detail_model" type="border-card" class="sample-tab-pane">
         <el-tab-pane label="样本" name="sample" >

             <div id="sample-correct-result-box">
               <div id="sample-correct-result">
                 <div v-for="(sub_tag,key) in current_result_json_schema?.properties">
                   <el-text>
                     {{ sub_tag.title }}:
                   </el-text>
                   <el-tag v-if="current_data_sample.tags?.[key]?.tag_value_history
                 == current_data_sample.tags?.[key]?.tag_value_correct"
                           type="success" round
                   >
                     正确
                   </el-tag>
                   <el-tag v-else type="danger" round>
                     错误
                   </el-tag>
                 </div>

               </div>
               <div style="padding: 0 12px">
                 <el-divider>
                   <el-text class="divider-text">编辑真实标签</el-text>
                 </el-divider>
               </div>
               <div id="sample-correct-tag" v-if="!data_sample_detail_loading">
                 <el-form label-position="top" style="width: 100%">

                   <el-form-item v-for="(sub_params,key) in current_result_json_schema?.properties"
                                 :label="sub_params.title" style="width: 100%">
                     <el-input-number v-if="sub_params.type==='integer' " style="width: 100%"
                                      v-model="current_sample_tags[key].tag_value_correct"
                                      :min="sub_params?.minimum" :max="sub_params?.maximum"/>
                     <el-input-number v-else-if="sub_params.type==='number' " :precision="2" style="width: 100%"
                                      v-model="current_sample_tags[key].tag_value_correct"/>
                     <el-input v-else-if="sub_params.type==='string' && !sub_params.enum" style="width: 100%"
                               v-model="current_sample_tags[key].tag_value_correct"/>
                     <el-select v-else-if="sub_params.type==='string' && sub_params.enum" style="width: 100%"
                                v-model="current_sample_tags[key].tag_value_correct">
                       <el-option v-for="item in sub_params.enum" :key="item" :label="sub_params['x-apifox'].enumDescriptions[item]"
                                  :value="item"/>
                     </el-select>
                     <el-switch v-else-if="sub_params.type==='boolean' "
                                style="width: 100%"
                                v-model="current_sample_tags[key].tag_value_correct"
                                inline-prompt
                                active-text="是"
                                inactive-text="否"
                     />
                   </el-form-item>

                 </el-form>
               </div>

               <data_sample_context/>

             </div>


         </el-tab-pane>

         <el-tab-pane label="预测信息" name="predict">
           <el-form label-position="top" style="width: 100%" v-if="!data_sample_detail_loading">
             <el-form-item label="预测结果" >
               <el-input v-model="current_data_sample.sample_result" placeholder="预测结果"
                         type="textarea"
                         resize="none"
                         rows="4"
                   readonly
               ></el-input>
             </el-form-item>
             <el-form-item>
               <el-divider>
                 <el-text class="divider-text">编辑预测标签</el-text>
               </el-divider>
             </el-form-item>
             <el-form-item v-for="(sub_params,key) in current_result_json_schema?.properties"
                           :label="sub_params.title" style="width: 100%">
               <el-input-number v-if="sub_params.type==='integer' " style="width: 100%"
                                v-model="current_sample_tags[key].tag_value_history"
                                :min="sub_params?.minimum" :max="sub_params?.maximum"/>
               <el-input-number v-else-if="sub_params.type==='number' " :precision="2" style="width: 100%"
                                v-model="current_sample_tags[key].tag_value_history"/>
               <el-input v-else-if="sub_params.type==='string' && !sub_params.enum" style="width: 100%"
                         v-model="current_sample_tags[key].tag_value_history"/>
               <el-select v-else-if="sub_params.type==='string' && sub_params.enum" style="width: 100%"
                          v-model="current_sample_tags[key].tag_value_history">
                 <el-option v-for="item in sub_params.enum" :key="item"
                            :label="sub_params['x-apifox'].enumDescriptions[item]"
                            :value="item"/>
               </el-select>
               <el-switch v-else-if="sub_params.type==='boolean' "
                          style="width: 100%"
                          v-model="current_sample_tags[key].tag_value_history"
                          inline-prompt
                          active-text="是"
                          inactive-text="否"
               />
             </el-form-item>
           </el-form>

         </el-tab-pane>
       </el-tabs>

     </div>
     </el-scrollbar>
     <template #footer>
       <div class="middle-box">
         <el-button @click="show_target_data_sample_drawer = false">取消</el-button>
         <el-button type="primary" @click="update_current_data_sample_tags()">保存</el-button>
       </div>
     </template>
   </el-drawer>
</template>

<style>
#drawer-header{
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-direction: row;

}
.middle-box{
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: row;
}
#drawer-header-button-box{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 8px;
}
.divider-text{
  font-size: 14px;
  line-height: 20px;
  color: #475467;
  font-weight: 600;
}
#sample-correct-result-box{
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
#sample-correct-result{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: 22px;
  background-color: #F9FAFB;
  padding: 8px 12px;
}
.sample-tab-pane :deep( .el-tabs__content){

    padding: 0 !important;

}
#sample-correct-tag{
  width: calc(100% - 24px);
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 0 12px;
}
.data-sample-drawer   {

  .el-drawer__body{
    padding: 0 !important;
  }
}

</style>
