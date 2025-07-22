<script setup lang="ts">

import {current_assistant_instruction, current_dry_run_params} from "@/components/feedback_center/prompt_test";
</script>

<template>
  <div style="width: 100%">
    <el-form label-position="top" >
    <el-form-item v-for="(sub_params,key) in current_assistant_instruction?.instruction_params_json_schema?.properties"
                  :label="sub_params.title"
    >
      <el-input-number v-if="sub_params.type==='integer' " style="width: 100%"
                       v-model="current_dry_run_params[key]" :min="sub_params?.minimum" :max="sub_params?.maximum"/>
      <el-input-number v-else-if="sub_params.type==='number' " :precision="2" style="width: 100%"
                       v-model="current_dry_run_params[key]"/>
      <el-input v-else-if="sub_params.type==='string' && !sub_params.enum" v-model="current_dry_run_params[key]"
                style="width: 100%"
      />
      <el-select v-else-if="sub_params.type==='string' && sub_params.enum" style="width: 100%"
                 v-model="current_dry_run_params[key]">
        <el-option v-for="item in sub_params.enum" :key="item" :label="item" :value="item"/>
      </el-select>
      <el-switch v-else-if="sub_params.type==='boolean' " style="width: 100%"
          v-model="current_dry_run_params[key]"
          inline-prompt
          active-text="是"
          inactive-text="否"
      />
    </el-form-item>
  </el-form>
  </div>
</template>

<style scoped>

</style>
