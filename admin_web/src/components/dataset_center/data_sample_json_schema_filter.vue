<script setup lang="ts">
import {Search} from '@element-plus/icons-vue'
import {
  current_result_json_schema,
  current_sample_key_work,
  current_tags_filter,
  get_data_set_sample_list
} from "@/components/dataset_center/data_samples";
</script>

<template>
  <el-scrollbar>
    <div id="dataset-sample-button-group">
      <div>
        <el-input v-model="current_sample_key_work" :prefix-icon="Search" placeholder="搜索问题..."
                  @change="get_data_set_sample_list"/>
      </div>
      <div v-for="(sub_params,key) in current_result_json_schema?.properties" class="json-filter-box">
        <el-select v-if="sub_params.type==='string' && sub_params.enum" style="width: 100%"
                   multiple :placeholder="sub_params.title + '-真实'"
                   @change="get_data_set_sample_list"
                   v-model="current_tags_filter[key].tag_value_correct">
          <el-option v-for="item in sub_params.enum" :key="item" :label="item" :value="item"/>
        </el-select>
        <el-select v-else-if="sub_params.type==='boolean'"
                   multiple
                   :placeholder="sub_params.title + '-真实'" style="width: 100%"
                   @change="get_data_set_sample_list"
                   v-model="current_tags_filter[key].tag_value_correct">
          <el-option label="是" :value="true"/>
          <el-option label="否" :value="false"/>
        </el-select>
        <el-select v-if="sub_params.type==='string' && sub_params.enum" style="width: 100%"
                   multiple :placeholder="sub_params.title + '-预测'"
                   @change="get_data_set_sample_list"
                   v-model="current_tags_filter[key].tag_value_history">
          <el-option v-for="item in sub_params.enum" :key="item" :label="item" :value="item"/>
        </el-select>
        <el-select v-else-if="sub_params.type==='boolean'"
                   :placeholder="sub_params.title + '-预测'" style="width: 100%"
                   multiple
                   @change="get_data_set_sample_list"
                   v-model="current_tags_filter[key].tag_value_history">
          <el-option label="是" :value="true"/>
          <el-option label="否" :value="false"/>
        </el-select>
        <el-select :placeholder="sub_params.title + '-结果' " multiple style="width: 100%"
                   @change="get_data_set_sample_list"
                   v-model="current_tags_filter[key].tag_result">
          <el-option label="正确" :value="true"/>
          <el-option label="错误" :value="false"/>
        </el-select>
      </div>
    </div>
  </el-scrollbar>
</template>

<style scoped>
#dataset-sample-button-group{
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 6px;
  padding: 6px 8px;
  width: calc(100% - 16px);
}
.json-filter-box{
  max-width: 280px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
}
</style>
