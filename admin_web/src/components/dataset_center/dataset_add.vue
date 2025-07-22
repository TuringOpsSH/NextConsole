<script setup lang="ts">

import {
  cancel_add_new_data_set,
  data_set_add_model, data_set_add_rules,
  data_set_instructions_list,
  data_set_add_form,
  get_all_available_instructions, submit_new_data_set_form
} from "@/components/dataset_center/data_set";
import {onMounted} from "vue";
onMounted(async () => {
  await get_all_available_instructions()
});
</script>

<template>
  <div class="middle-box" style="margin-top: 36px;">
    <el-form :model="data_set_add_model" label-position="top" style="width: 66%"
             :rules="data_set_add_rules"
              ref="data_set_add_form"
    >
      <el-form-item label="数据集名称" required prop="dataset_name">
          <el-input v-model="data_set_add_model.dataset_name"/>
      </el-form-item>
      <el-form-item label="数据集类型" required prop="dataset_type">
        <el-select v-model="data_set_add_model.dataset_type" placeholder="请选择">
          <el-option label="指令" value="指令"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="数据集描述">
        <el-input v-model="data_set_add_model.dataset_desc" type="textarea" :rows="6" show-word-limit maxlength="1024"
                  resize="none"
        />
      </el-form-item>
      <el-form-item label="目标指令" required>
         <el-select v-model="data_set_add_model.instruction_id" placeholder="请选择">
          <el-option v-for="(instruction,index) in data_set_instructions_list"
                     :label="instruction.instruction_desc" :value="instruction.id"/>
        </el-select>

      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submit_new_data_set_form(data_set_add_form)">创建</el-button>
        <el-button @click="cancel_add_new_data_set">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<style scoped>
.middle-box{
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: center;
  justify-content: center;
}
</style>
