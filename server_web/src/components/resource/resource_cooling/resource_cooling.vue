<script setup lang="ts">
import {
  cool_record_dialog, cooling_resource, current_cool_record, current_cooling_user,
  exit_cooling_page,
  init_cooling_record, update_cooling_limit
} from "@/components/resource/resource_cooling/resource_cooling";
import {onMounted} from "vue";
import {get_resource_icon} from "@/components/resource/resource_list/resource_list";
const props = defineProps(
    {
      cooling_id: {
        type: String,
        default: '',
        required: true
      },


    }
)
onMounted(async ()=> {
    if (props.cooling_id){
      try {
        await init_cooling_record(parseInt(props.cooling_id))
      }catch (e) {
        // console.log(e)
      }
    }
  })


</script>

<template>


    <el-dialog v-model="cool_record_dialog" title="共享资源下载拦截" draggable :close-on-click-modal="false"
                :close-on-press-escape="false"  width="50%" style="max-width: 600px" :show-close="false" >
      <div>
        <div style="display:flex;flex-direction: column;gap: 12px;width: 100%;height: 100%">
          <div class="field-row">
            <div  class="field-name">
              <el-text>被拦截用户：</el-text>
            </div>
            <div class="field-value">
              <el-avatar :src="current_cooling_user?.user_avatar" v-if="current_cooling_user?.user_avatar"/>
              <el-avatar v-else>{{ current_cooling_user?.user_nick_name_py}}</el-avatar>
              <el-text>{{ current_cooling_user.user_nick_name }}</el-text>
              <el-text>{{ current_cooling_user.user_email}}</el-text>
            </div>
          </div>
          <div class="field-row">
            <div class="field-name">
              <el-text>被拦截资源：</el-text>
            </div>
            <div class="field-value">
              <el-image :src="get_resource_icon(cooling_resource)" />
              <el-text>{{ cooling_resource.resource_name }}</el-text>
            </div>
          </div>
          <div class="field-row">
            <div class="field-name">
              <el-tooltip content="为该用户在原有下载限制下扩展可下载的资源数目">
                <el-text>扩展限制：</el-text>
              </el-tooltip>
            </div>
            <div class="field-value">
              <el-input-number v-model="current_cool_record.author_allow_cnt" :min="0" :max="1000" :step="1"
                               style="width: 100%"/>
            </div>
          </div>

        </div>


      </div>
      <template #footer>
        <div class="std-middle-box">
          <el-button @click="exit_cooling_page()">关闭</el-button>
          <el-button type="primary" @click="update_cooling_limit()">更新授权</el-button>
        </div>

      </template>
    </el-dialog>

</template>

<style scoped>
.std-middle-box{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  height: 100%;
  width: 100%;
}
.field-row{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  width: 100%;
  height: 100%;
  gap: 12px;
}
.field-name{
  width : 100px;
}
.field-value{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 12px;
}
</style>