<script setup lang="ts">
import {ref, watch} from 'vue';
import {update_session} from "@/api/next_console";
const props = defineProps({
  schema: {
    type: Object,
    required: true,
    default: {}
  },
  params: {
    type: Object,
    required: true,
    default: {}
  },
  session_id: {
    type: Number,
    required: true,
    default: 0
  }
})
const localSchema = ref({});
const localParams = ref({});
const fixedParams = {};
const localSessionId = ref(0);
const schemaReady = ref(false);
const formShow = ref(true);
async function updateParams() {
  const res = await update_session(
      {
        session_id: localSessionId.value,
        session_task_params: localParams.value
      }
  )
  if (!res.error_status) {
    localParams.value = res.result.session_task_params;
    Object.assign(fixedParams, res.result.session_task_params);
  }
}
function compareObjects(obj1, obj2) {
  return JSON.stringify(obj1) === JSON.stringify(obj2);
}
watch(() => props.schema, (newVal) => {
  localSchema.value = newVal;
}, { immediate: true });
watch(() => props.params, (newVal) => {
  localParams.value = newVal;
  try {
    Object.assign(fixedParams, newVal)
  } catch (e) {
    console.error('Error merging params:', e);
  }
}, { immediate: true });
watch(() => props.session_id, (newVal) => {
  localSessionId.value = newVal;
}, { immediate: true });
defineExpose({
  schemaReady
});
</script>

<template>
<div class="main-area">
  <div class="content">
    <div class="head-area">
      <div>
          <el-text size="large" type="primary">会话参数</el-text>
        </div>
      <div class="head-area-right">
        <div>
          <el-button type="primary" text @click="updateParams" :disabled="compareObjects(fixedParams, localParams)">
            更新参数
          </el-button>
        </div>
        <div>
          <el-button type="primary" text @click="formShow = !formShow" v-if="formShow">
            收起
          </el-button>
          <el-button type="primary" text @click="formShow = !formShow" v-else>
            展开
          </el-button>
        </div>
      </div>
    </div>
    <div class="main-area" v-show="formShow">
      <el-form label-position="top" :model="localParams" style="width: 100%">
        <el-form-item v-for="item in localSchema.ncOrders"
                      :prop="item"
                      :required="localSchema?.required?.includes(item)"
                      :label="localSchema.properties?.[item]?.description || item"
        >
          <el-select v-if="localSchema.properties?.[item]?.emun?.length"
                     v-model="localParams[item]"
          >
            <el-option v-for="value in localSchema.properties?.[item]?.emun"  :value="value"  :label="value"/>
          </el-select>
          <el-input v-else-if="localSchema.properties?.[item]?.type=='string'"
                    v-model="localParams[item]"
          />
          <el-input-number v-if="localSchema.properties?.[item]?.type=='number'"
                           v-model="localParams[item]"
          />
          <el-radio-group v-else-if="localSchema.properties?.[item]?.type=='boolean'"
                          v-model="localParams[item]"
          >
            <el-radio :label="true">是</el-radio>
            <el-radio :label="false">否</el-radio>
          </el-radio-group>
          <el-upload action="" v-else-if="localSchema.properties?.[item]?.type=='file'">

          </el-upload>
        </el-form-item>
      </el-form>


    </div>
  </div>

</div>
</template>

<style scoped>
.main-area {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.content {
  width: 100%;
  max-width: 800px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.head-area {
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
.head-area-right {
  display: flex;
  flex-direction: row;
  align-items: center;
}
</style>
