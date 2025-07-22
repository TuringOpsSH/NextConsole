<script setup lang="ts">

import {CurrentKg} from "@/components/kg/kg_process";
import {
  current_script_tags,
  current_script_tags_form,
  current_script_tags_valid_status
} from "@/components/kg/code_kg/code_script_process";
import {c} from "vite/dist/node/types.d-aGj9QkWt";
function check_required(key){
  return !!CurrentKg.value?.kg_json_schema?.required.includes(key);


}
</script>

<template>
  <el-form require-asterisk-position="right" label-position="top" style="width: 100%"
           v-model="current_script_tags"
           v-if="CurrentKg.kg_json_schema && current_script_tags" ref="current_script_tags_form">
    <el-form-item v-for="(item,name) in CurrentKg.kg_json_schema.properties"
                  :label="item?.description"

                  :required="check_required(name)"

    >
      <el-input-number v-if="item.type==='integer' " style="width: 100%"
                       v-model="current_script_tags[name]"
                       :min="item?.minimum" :max="item?.maximum"/>
      <el-input-number v-else-if="item.type==='number' " :precision="2" style="width: 100%"
                       v-model="current_script_tags[name]"/>
      <el-input v-else-if="item.type==='string' && !item.enum" v-model="current_script_tags[name]"
                :maxlength="item?.maximum" :minlength="item?.minimum"
                style="width: 100%"
      />
      <el-input v-else-if="item.type==='object' " v-model="current_script_tags[name]"
                type="textarea" :rows="5" resize="none"
                style="width: 100%"
      />
      <el-select v-else-if="item.type==='string' && item.enum" style="width: 100%"
                 v-model="current_script_tags[name]">
        <el-option v-for="item_label in item.enum" :key="item_label" :label="item_label" :value="item_label"/>
      </el-select>
      <el-switch v-else-if="item.type==='boolean' " style="width: 100%"
                 v-model="current_script_tags[name]"
                 inline-prompt
                 active-text="是"
                 inactive-text="否"
      />
    </el-form-item>
  </el-form>
</template>

<style scoped>

</style>
