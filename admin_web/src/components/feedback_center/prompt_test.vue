<script setup lang="ts">

import {
  assistant_instructions,
  current_assistant_instruction_name, current_data_relate_set,
  current_data_sample,
  current_dry_run_loading,
  current_dry_run_result,
  dry_run_instruction,
  prompt_test_dialog,
  switch_current_assistant_instruction,
  update_data_sample_tags
} from "@/components/feedback_center/prompt_test";
import Json_schema_params_form from "@/components/feedback_center/json_schema_params_form.vue";
import Json_schema_tag_form from "@/components/feedback_center/json_schema_tag_form.vue";
</script>

<template>
  <el-dialog v-model="prompt_test_dialog" width="80%">
    <template #header>
      <span>提示词测试</span>
    </template>
    <div>
      <el-tabs v-model="current_assistant_instruction_name" @tab-change="switch_current_assistant_instruction" >
        <el-tab-pane :label="sub_instruction.instruction_desc" :name="sub_instruction.instruction_name"
                   v-for="(sub_instruction,index) in assistant_instructions" >
        <div id="instruction-test-area">
          <div id="instruction-dry-run">
            <div id="instruction-params">
              <Json_schema_params_form/>
              <div id="instruction-params-button" @click="dry_run_instruction">
                <div class="middle-box">
                  <el-image src="images/play_white.svg" style="width: 15px;height: 15px"/>
                </div>
                <div class="middle-box">
                  <el-text style="font-weight: 600;line-height: 20px;font-size: 14px;color: #FFFFFF">
                    运行
                  </el-text>
                </div>
              </div>
            </div>
            <div id="instruction-output">
              <div>
                <el-text>运行结果</el-text>
              </div>
              <div style="width: 100%">
                <el-input type="textarea" v-model="current_dry_run_result" :rows="3"
                          v-loading="current_dry_run_loading"
                          :readonly="true" resize="none" style="width: 100%"/>
              </div>
            </div>
          </div>

          <div id="instruction-tags">
            <el-divider>
                 <div v-if="!current_data_relate_set?.length" class="middle-divider-box">
                   <div class="middle-box">
                     <el-image src="images/dot_grey.svg" style="width: 8px;height: 8px"></el-image>
                   </div>
                   <div class="middle-box">
                     <el-text>未加入测试集</el-text>
                   </div>
                 </div>
                <div v-else class="middle-divider-box">
                  <div class="middle-box">
                    <el-image src="images/dot_green.svg" style="width: 8px;height: 8px"></el-image>
                  </div>
                  <div class="middle-box">
                    <el-text>已加入测试集</el-text>
                  </div>
                </div>
            </el-divider>
            <Json_schema_tag_form/>
            <div id="instruction-tags" >

              <div id="instruction-params-button" @click="update_data_sample_tags">
                <div class="middle-box">
                  <el-image src="images/play_white.svg" style="width: 15px;height: 15px"/>
                </div>
                <div class="middle-box">
                  <el-text style="font-weight: 600;line-height: 20px;font-size: 14px;color: #FFFFFF">
                    更新样本标签
                  </el-text>
                </div>
              </div>
            </div>
          </div>
        </div>

      </el-tab-pane>

    </el-tabs>
    </div>
  </el-dialog>
</template>

<style scoped>
#instruction-test-area{
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: center;
  justify-content: center;
  width: 100%
}
#instruction-dry-run{
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: center;
  justify-content: center;
  width: 100%
}
#instruction-params{
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: flex-start;
  justify-content: center;
  width: 100%
}
#instruction-params-button{
  display: flex;
  flex-direction: row;
  gap: 8px;
  align-items: center;
  justify-content: center;
  width: calc(100% - 24px);
  background-color: #1570ef;
  border-radius: 8px;
  padding: 6px 12px;
  cursor: pointer;

}
.middle-box{
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: center;
  justify-content: center;
}
#instruction-output{
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: flex-start;
  justify-content: center;
  width: 100%
}
#instruction-tags{
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: flex-start;
  justify-content: center;
  width: 100%
}
.middle-divider-box {
  display: flex;
  flex-direction: row;
  gap: 8px;
  align-items: center;
  justify-content: center;
}
</style>
