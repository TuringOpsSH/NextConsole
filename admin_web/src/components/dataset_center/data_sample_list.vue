<script setup lang="ts">

import {
  batch_delete_data_samples, batch_download_data_samples,
  current_data_set_id,
  current_params_json_schema,
  current_result_json_schema,
  current_sample_key_work,
  data_set_sample_list,
  data_set_sample_page_num,
  data_set_sample_page_size,
  data_set_sample_page_total,
  delete_data_set_samples, download_loading, get_all_selected_data_samples,
  get_data_set_sample_list,
  get_data_set_tag_json_schema,
  hand_data_set_page_change,
  hand_data_set_size_change,
  show_data_set_sample_meta
} from "@/components/dataset_center/data_samples";
import {onMounted} from "vue";

import Data_sample_json_schema_filter from "@/components/dataset_center/data_sample_json_schema_filter.vue";
import Data_sample_meta from "@/components/dataset_center/data_sample_meta.vue";
const props = defineProps({
      data_set_id :{
        type: String,
        required: false,
        default: '',
      },
      page_num: {
        type: String,
        required: false,
        default: 1,
      },
      page_size: {
        type: String,
        required: false,
        default: 1000,
      },
    }
);
onMounted(async () => {
  if (props.page_num){
    try{
      let page_num = parseInt(props.page_num);
      if (page_num > 0){
        data_set_sample_page_num.value = page_num;
      }
    }
    catch (e) {
      console.error('props.page_num', e)
    }
  }
  if (props.page_size){
    try{
      let page_size = parseInt(props.page_size);
      if (page_size > 0){
        data_set_sample_page_size.value = page_size;
      }
    }
    catch (e) {
      console.error('props.page_size', e)
    }
  }
  if (props.data_set_id){
    try {
      let data_set_id = parseInt(props.data_set_id);
      if (data_set_id > 0){
        current_data_set_id.value = data_set_id;
      }
    } catch (e) {
      console.error('props.data_set_id', e)

    }
  }
  await get_data_set_tag_json_schema();
  await get_data_set_sample_list();

});

</script>

<template>
  <el-container v-loading="download_loading" element-loading-text="样本下载中">
    <el-header style="padding: 0 !important;" height="120px">
      <div id="dataset-sample-header">
        <div class="middle-box" style="min-width: 80px">
          <el-text style="font-size: 16px;line-height: 24px;font-weight: 600;color: #101828">数据样本</el-text>
        </div>
        <div id="dataset-sample-header-right">
          <data_sample_json_schema_filter/>
          <el-dropdown style="width: 120px;display: flex;flex-direction: row;gap: 6px">
            <div id="sample-batch-op">
              <div class="middle-box">
                <el-text style="font-size: 14px;font-weight: 600;line-height: 20px;color: #175CD3">
                  批量操作
                </el-text>
                <el-image src="images/dots_horizontal_blue.svg" style="width: 20px;height: 20px;margin-left: 6px;"/>
              </div>

            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="batch_download_data_samples()">
                  下载
                </el-dropdown-item>
                <el-dropdown-item @click="batch_delete_data_samples()">
                  删除
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>

          <div id="prompt-manage">

          </div>
        </div>

      </div>
    </el-header>
    <el-main style="height: calc(100vh - 260px)">
      <el-scrollbar>
        <el-table :data="data_set_sample_list" stripe style="width: 100%" :highlight-current-row="true"
                  show-overflow-tooltip height="calc(100vh - 300px)"
                  @selection-change="get_all_selected_data_samples"
        >
          <el-table-column type="selection" width="55" />
          <el-table-column prop="id" label="样本编号" width="60" :sortable="true"/>
          <el-table-column prop="session_id" label="会话编号" width="60" :sortable="true"/>
          <el-table-column prop="user_name" label="作者名称" width="120" :sortable="true"/>
          <el-table-column prop="msg_content" label="样本问题" :sortable="true" width="360"/>
          <el-table-column prop="instruction_desc" label="指令名称" :sortable="true" width="100"/>
          <el-table-column prop="create_time" label="创建时间" :sortable="true" width="180" />
          <el-table-column prop="update_time" label="更新时间" :sortable="true" width="180"/>
          <el-table-column v-for="(sub_tag,key) in current_params_json_schema?.properties"
                           :label="'真实-' + sub_tag.title"
                           :sortable="true"
                           width="120"
                                    >

            <template #default="{row}">
              <el-text>{{row?.tags[key]?.tag_value_correct }}</el-text>
            </template>
          </el-table-column>
          <el-table-column v-for="(sub_tag,key) in current_params_json_schema?.properties"
                           :label="'预测-' + sub_tag.title"
                           :sortable="true"
                           width="120"
          >
            <template #default="{row}">
              <el-text>{{row?.tags[key]?.tag_value_history }}</el-text>
            </template>
          </el-table-column>
          <el-table-column v-for="(sub_tag,key) in current_result_json_schema?.properties"
                           :label="'真实-' + sub_tag.title"
                           :sortable="true"
                           width="120"
          >

            <template #default="{row}">
              <el-text>{{row?.tags[key]?.tag_value_correct }}</el-text>
            </template>
          </el-table-column>
          <el-table-column v-for="(sub_tag,key) in current_result_json_schema?.properties"
                           :label="'预测-' + sub_tag.title   "
                           :sortable="true"
                           width="120"
          >

            <template #default="{row}">
              <el-text>{{row?.tags[key]?.tag_value_history }}</el-text>
            </template>
          </el-table-column>
          <el-table-column v-for="(sub_tag,key) in current_result_json_schema?.properties"
                           :label="'结果-' + sub_tag.title   "
                           :sortable="true" fixed="right"
                           width="120"

          >

            <template #default="{row}">
              <el-tag v-if="row?.tags[key]?.tag_value_history == row?.tags[key]?.tag_value_correct" type="success">
                正确
              </el-tag>
              <el-tag v-else type="danger">
                错误
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" fixed='right'>
            <template #default="{row}">
              <div class="dataset-sample-manager-button-group">
                <div style="cursor: pointer" @click="show_data_set_sample_meta(row)">

                  <el-tooltip effect="light">
                    <template #content>
                      <el-text>查看数据样本</el-text>
                    </template>
                    <el-image style="width: 20px;height: 20px" src="images/icon_circle_grey.svg"  />
                  </el-tooltip>
                </div>

                <el-popconfirm title="确定要删除么?" @confirm="delete_data_set_samples(row)">
                  <template #reference>
                    <div style="cursor: pointer">
                      <el-image style="width: 20px;height: 20px" src="images/trash_01_grey.svg"  />
                    </div>


                  </template>

                </el-popconfirm>
              </div>
            </template>
          </el-table-column>
        </el-table>
        <data_sample_meta/>
      </el-scrollbar>
    </el-main>
    <el-footer>
      <div class="dataset-sample-pagination" >
        <el-pagination
            :small="true"
            layout=" total, sizes, prev, pager, next"
            :total="data_set_sample_page_total"
            :page-sizes="[100,200,500,1000]"
            :page-size="data_set_sample_page_size"
            :current-page="data_set_sample_page_num"
            @update:page-size="hand_data_set_size_change"
            @update:current-page="hand_data_set_page_change"
        />
      </div>
    </el-footer>
  </el-container>

</template>

<style scoped>
#dataset-sample-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #D0D5DD;
  padding: 6px 8px;
  width: calc(100% - 16px);
}
.dataset-sample-manager-button-group{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 8px;
}
.dataset-sample-pagination{
  display: flex;
  justify-content: center;
  align-content: center;
  width: 100%;
  height: 100%;
}
.middle-box {
  display: flex;
  justify-content: center;
  align-items: center;

}
#dataset-sample-header-right{
  display: flex;
  flex-direction: row;
  gap: 8px;
  align-items: center;
  justify-content: center;
}
#sample-batch-op{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 8px 14px;
  border-radius: 8px;
  background-color: #EFF8FF;
  border: 1px solid #B2DDFF;
  box-shadow: 0 1px 2px 0 #1018280D;
  cursor: pointer;

}
</style>
