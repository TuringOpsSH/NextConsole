<script setup lang="ts">

import {
  available_data_set_list,
  current_assistant_instruction, current_data_relate_set, current_dry_run_result_extract_loading,
  current_dry_run_tags, tags_type, update_data_sample_relations,
} from "@/components/feedback_center/prompt_test";
</script>

<template>
  <div style="width: 100%">
    <el-tabs v-model="tags_type"  type="border-card">
      <el-tab-pane label="预测值" name="history" v-loading="current_dry_run_result_extract_loading">
        <el-form label-position="top" >
          <el-form-item v-for="(sub_params,key) in current_assistant_instruction?.instruction_params_json_schema?.properties"
                        :label="sub_params.title"
          >
            <el-input-number v-if="sub_params.type==='integer' " style="width: 100%"
                             v-model="current_dry_run_tags[key].tag_value_history"
                             :min="sub_params?.minimum"
                             :max="sub_params?.maximum"/>
            <el-input-number v-else-if="sub_params.type==='number' " :precision="2" style="width: 100%"
                             v-model="current_dry_run_tags[key].tag_value_history"/>
            <el-input v-else-if="sub_params.type==='string' && !sub_params.enum" v-model="current_dry_run_tags[key].tag_value_correct"
                      style="width: 100%"
            />
            <el-select v-else-if="sub_params.type==='string' && sub_params.enum" style="width: 100%"
                       v-model="current_dry_run_tags[key].tag_value_history">
              <el-option v-for="item in sub_params.enum" :key="item" :label="item" :value="item"/>
            </el-select>
            <el-switch v-else-if="sub_params.type==='boolean' " style="width: 100%"
                       v-model="current_dry_run_tags[key].tag_value_history"
                       inline-prompt
                       active-text="是"
                       inactive-text="否"
            />
          </el-form-item>
          <el-form-item v-for="(sub_params,key) in current_assistant_instruction?.instruction_result_json_schema?.properties"
                        :label="sub_params.title"
          >
            <el-input-number v-if="sub_params.type==='integer' " style="width: 100%"
                             v-model="current_dry_run_tags[key].tag_value_history" :min="sub_params?.minimum" :max="sub_params?.maximum"/>
            <el-input-number v-else-if="sub_params.type==='number' " :precision="2" style="width: 100%"
                             v-model="current_dry_run_tags[key].tag_value_history"/>
            <el-input v-else-if="sub_params.type==='string' && !sub_params.enum" style="width: 100%"
                      v-model="current_dry_run_tags[key].tag_value_history"/>
            <el-select v-else-if="sub_params.type==='string' && sub_params.enum" style="width: 100%"
                       v-model="current_dry_run_tags[key].tag_value_history">
              <el-option v-for="item in sub_params.enum" :key="item" :label="sub_params['x-apifox'].enumDescriptions[item]"
                         :value="item"/>
            </el-select>
            <el-switch v-else-if="sub_params.type==='boolean' "
                       style="width: 100%"
                       v-model="current_dry_run_tags[key].tag_value_history"
                       inline-prompt
                       active-text="是"
                       inactive-text="否"
            />
          </el-form-item>
          <el-form-item label="关联测试数据集" >
            <el-select v-model="current_data_relate_set" style="width: 100%" multiple

                       value-key="id"
                       collapse-tags
                       collapse-tags-tooltip>
              <el-option v-for="item in available_data_set_list" :key="item.id"
                         :label="item.id + '.' + item.dataset_name" :value="item"/>
            </el-select>
          </el-form-item>
        </el-form>
      </el-tab-pane>
      <el-tab-pane label="真实值" name="correct">
        <el-form label-position="top" >
          <el-form-item v-for="(sub_params,key) in current_assistant_instruction?.instruction_params_json_schema?.properties"
                        :label="sub_params.title"
          >
            <el-input-number v-if="sub_params.type==='integer' " style="width: 100%"
                             v-model="current_dry_run_tags[key].tag_value_correct"
                             :min="sub_params?.minimum"
                             :max="sub_params?.maximum"/>
            <el-input-number v-else-if="sub_params.type==='number' " :precision="2" style="width: 100%"
                             v-model="current_dry_run_tags[key].tag_value_correct"/>
            <el-input v-else-if="sub_params.type==='string' && !sub_params.enum" v-model="current_dry_run_tags[key].tag_value_correct"
                      style="width: 100%"
            />
            <el-select v-else-if="sub_params.type==='string' && sub_params.enum" style="width: 100%"
                       v-model="current_dry_run_tags[key].tag_value_correct">
              <el-option v-for="item in sub_params.enum" :key="item" :label="item" :value="item"/>
            </el-select>
            <el-switch v-else-if="sub_params.type==='boolean' " style="width: 100%"
                       v-model="current_dry_run_tags[key].tag_value_correct"
                       inline-prompt
                       active-text="是"
                       inactive-text="否"
            />
          </el-form-item>
          <el-form-item v-for="(sub_params,key) in current_assistant_instruction?.instruction_result_json_schema?.properties"
                        :label="sub_params.title"
          >
            <el-input-number v-if="sub_params.type==='integer' " style="width: 100%"
                             v-model="current_dry_run_tags[key].tag_value_correct" :min="sub_params?.minimum" :max="sub_params?.maximum"/>
            <el-input-number v-else-if="sub_params.type==='number' " :precision="2" style="width: 100%"
                             v-model="current_dry_run_tags[key].tag_value_correct"/>
            <el-input v-else-if="sub_params.type==='string' && !sub_params.enum" style="width: 100%"
                      v-model="current_dry_run_tags[key].tag_value_correct"/>
            <el-select v-else-if="sub_params.type==='string' && sub_params.enum" style="width: 100%"
                       v-model="current_dry_run_tags[key].tag_value_correct">
              <el-option v-for="item in sub_params.enum" :key="item" :label="sub_params['x-apifox'].enumDescriptions[item]"
                         :value="item"/>
            </el-select>
            <el-switch v-else-if="sub_params.type==='boolean' "
                       style="width: 100%"
                       v-model="current_dry_run_tags[key].tag_value_correct"
                       inline-prompt
                       active-text="是"
                       inactive-text="否"
            />
          </el-form-item>
          <el-form-item label="关联测试数据集" >
            <el-select v-model="current_data_relate_set" style="width: 100%" multiple

                       value-key="id"
                       collapse-tags
                       collapse-tags-tooltip>
              <el-option v-for="item in available_data_set_list" :key="item.id"
                         :label="item.id + '.' + item.dataset_name" :value="item"/>
            </el-select>
          </el-form-item>
        </el-form>
      </el-tab-pane>
    </el-tabs>

  </div>
</template>

<style scoped>

</style>
