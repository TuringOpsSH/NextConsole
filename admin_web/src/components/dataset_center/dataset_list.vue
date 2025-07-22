<script setup lang="ts">

import {
  add_new_data_set,
  data_set_list,
  data_set_page_num,
  data_set_page_size,
  data_set_page_total, delete_data_set,
  edit_data_set_meta,
  get_data_set_list,
  hand_data_set_page_change,
  hand_data_set_size_change,
  show_data_set_sample_list
} from "@/components/dataset_center/data_set";
import {onMounted} from "vue";

const props = defineProps({
  page_num: {
    type: String,
    required: false,
    default: 1,
  },
  page_size: {
    type: String,
    required: false,
    default: 10,
  },
}
);

onMounted(async () => {
  if (props.page_num){
    try{
      let page_num = parseInt(props.page_num);
      if (page_num > 0){
        data_set_page_num.value = page_num;
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
        data_set_page_size.value = page_size;
      }
    }
    catch (e) {
      console.error('props.page_size', e)
    }
  }
  await get_data_set_list();
});
</script>

<template>
  <el-container>
    <el-header style="padding: 0 !important;">
      <div id="dataset-header">
        <div id="dataset-title">
          <el-text style="font-size: 16px;line-height: 24px;font-weight: 600;color: #101828">数据集</el-text>
        </div>
        <div id="dataset-button-group">
          <div class="dataset-button" @click="add_new_data_set">
            <div class="middle-box">
              <el-image src="images/edit.svg"/>
            </div>
            <div class="middle-box">
              <el-text>新增数据集</el-text>
            </div>

          </div>

        </div>
      </div>
    </el-header>

    <el-main style="height: calc(100vh - 180px)">
      <el-scrollbar>
          <el-table :data="data_set_list" stripe style="width: 100%" :highlight-current-row="true"

      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="id" label="编号" width="120" :sortable="true"/>
        <el-table-column prop="dataset_name" label="数据集名称" width="180" :sortable="true"/>
        <el-table-column prop="dataset_desc" label="数据集描述" :sortable="true"/>
        <el-table-column prop="user_id" label="数据集作者" :sortable="true"/>
        <el-table-column prop="create_time" label="创建时间" :sortable="true"/>
        <el-table-column prop="update_time" label="更新时间" :sortable="true"/>
        <el-table-column label="操作" fixed='right'>
          <template #default="{row}">
            <div class="dataset-manager-button-group">
              <div style="cursor: pointer" @click="edit_data_set_meta(row)">
                <el-tooltip effect="light">
                  <template #content>
                    <el-text>编辑数据集元信息</el-text>
                  </template>
                  <el-image style="width: 20px;height: 20px"
                            src="images/edit.svg"/>
                </el-tooltip>
              </div>
              <div style="cursor: pointer" @click="show_data_set_sample_list(row)">

                <el-tooltip effect="light">
                  <template #content>
                    <el-text>查看数据样本</el-text>
                  </template>
                  <el-image style="width: 20px;height: 20px" src="images/icon_circle_grey.svg"  />
                </el-tooltip>
              </div>
              <el-popconfirm title="确定要删除么?" @confirm="delete_data_set(row)">
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
        </el-scrollbar>
    </el-main>

    <el-footer>
      <div class="dataset-pagination" >
        <el-pagination
            :small="true"
            layout=" total, sizes, prev, pager, next"
            :total="data_set_page_total"
            :page-sizes="[10,20,50,100]"
            :page-size="data_set_page_size"
            :current-page="data_set_page_num"
            @update:page-size="hand_data_set_size_change"
            @update:current-page="hand_data_set_page_change"
        />
      </div>
    </el-footer>
  </el-container>
</template>

<style scoped>
.middle-box {
  display: flex;
  justify-content: center;
  align-items: center;

}


#dataset-header{
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #D0D5DD;
  padding: 6px 8px;
  width: calc(100% - 16px);
}
.dataset-button{
  padding: 8px 16px;
  display: flex;
  flex-direction: row;
  gap: 6px;
  border-radius: 8px;
  border: 1px solid #D0D5DD;
  cursor: pointer;
}
.dataset-button:hover{
  background-color: #EFF8FF;
  border: 1px solid #B2DDFF;
}
.dataset-pagination{
  display: flex;
  justify-content: center;
  align-content: center;
  width: 100%;
  height: 100%;
}
.dataset-manager-button-group{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 8px;

}
</style>
