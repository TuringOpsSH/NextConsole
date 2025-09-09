<script setup lang="ts">
import {nextTick, ref, watch} from 'vue';
import {update_session} from "@/api/next-console";
import SingleFileUpload from "./SingleFileUpload.vue";
import MultipleFileUpload from "./MultipleFileUpload.vue";

const props = defineProps({
  session: {
    type: Object,
    required: true,
    default: {}
  },
  title: {
    type: String,
    required: false,
    default: '应用参数'
  }
})
const localSchema = ref({});
const localParams = ref({});
const localSessionId = ref(0);
const schemaReady = ref(false);
const formShow = ref(true);
const sessionFormRef = ref(null);
const localTitle = ref('应用参数');
async function updateParams() {
  const res = await update_session(
      {
        session_id: localSessionId.value,
        session_task_params: localParams.value
      }
  )
  if (!res.error_status) {
    localParams.value = res.result.session_task_params;
    const validRes = await sessionFormRef.value?.validate();
    if (!validRes) {
      return;
    }
    schemaReady.value = !!validRes;
  }
}
async function handleSingleFileUpdate(file, item) {
  if (file) {
    localParams.value[item] = {
      id: file.resource_id,
      icon: file.resource_icon,
      name: file.resource_name,
      size: file.resource_size,
    };
  } else {
    localParams.value[item] = {};
  }
  await updateParams();
  const validRes = await sessionFormRef.value?.validate();
  schemaReady.value = !!validRes;
}
async function handleMultipleFileUpdate(fileList, item) {
  if (fileList && fileList.length > 0) {
    localParams.value[item] = fileList.map(file => ({
      id: file.resource_id,
      icon: file.resource_icon,
      name: file.resource_name,
      size: file.resource_size,
    }));
  } else {
    localParams.value[item] = [];
  }
  await updateParams();
  const validRes = await sessionFormRef.value?.validate();
  schemaReady.value = !!validRes;
}
watch(() => props.session, async (newVal) => {
  localSessionId.value = newVal.id;
  localSchema.value = newVal.session_task_params_schema || {};
  localParams.value = newVal.session_task_params || {};
  await nextTick();
  let validRes = false;
  try {
    validRes = await sessionFormRef.value?.validate();
  } catch (e) {
    console.error('Error merging params:', e);
    validRes = false;
  }
  schemaReady.value = !!validRes;
}, { immediate: true , deep: true});

function close() {
  formShow.value = false;
}
watch(() => props.title, (newVal) => {
  localTitle.value = newVal || '应用参数';
}, { immediate: true });
defineExpose({
  schemaReady,
  close
});
</script>

<template>

<div class="main-area">

    <el-row style="width: 100%"  >
    <el-col :span="2" :xs="1" />
    <el-col :span="20" :xs="22">

        <div class="content">
        <div class="content-main">
          <div class="head-area">
            <div>
              <el-tooltip content="本次会话的参数设置" placement="top">
                <el-text size="large" type="primary">{{ localTitle }}</el-text>
              </el-tooltip>

            </div>
            <div class="head-area-right">
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
          <el-scrollbar>
            <transition name="dropdown">
              <div class="main-form-area" v-show="formShow">
              <el-form ref="sessionFormRef" label-position="top" :model="localParams" style="width: 100%;">
              <el-form-item v-for="item in localSchema.ncOrders"
                            :prop="item"
                            :required="localSchema?.required?.includes(item)"
                            :label="localSchema.properties?.[item]?.description || item"
                            :show-message="true"
                            @change="updateParams"
                            :rules="{
                            required: localSchema?.required?.includes(item),
                            message: (localSchema.properties?.[item]?.description || item) + '不能为空',
                            trigger: 'blur'
                          }"
              >
                <el-select v-if="localSchema.properties?.[item]?.enum?.length
                && !['file', 'file-list'].includes(localSchema.properties?.[item]?.typeName)"
                           v-model="localParams[item]"
                >
                  <el-option v-for="value in localSchema.properties?.[item]?.enum"  :value="value"  :label="value"/>
                </el-select>
                <el-input v-else-if="localSchema.properties?.[item]?.type=='string'"
                          v-model="localParams[item]"
                />
                <el-input-number v-if="localSchema.properties?.[item]?.type=='number'"
                                 v-model="localParams[item]" controls-position="right"
                />
                <el-input-number v-if="localSchema.properties?.[item]?.type=='integer'"
                                 v-model="localParams[item]" controls-position="right" :precision="0"
                />
                <el-radio-group v-else-if="localSchema.properties?.[item]?.type=='boolean'"
                                v-model="localParams[item]"
                >
                  <el-radio :value="true">是</el-radio>
                  <el-radio :value="false">否</el-radio>
                </el-radio-group>
                <div v-else-if="localSchema.properties?.[item]?.typeName=='file'" style="width: 100%">
                  <SingleFileUpload :session-id="localSessionId" :file="{
                  resource_id: localParams[item]?.id,
                  resource_icon: localParams[item]?.icon,
                  resource_name: localParams[item]?.name,
                  resource_size: localParams[item]?.size
                }"  :accept="localSchema.properties?.[item]?.enum"
                     @update:file="file => handleSingleFileUpdate(file, item)"
                  />
                </div>
                <div v-else-if="localSchema.properties?.[item]?.typeName=='file-list'" style="width: 100%">
                  <MultipleFileUpload :session-id="localSessionId" :file-list="localParams[item]"
                                      :accept="localSchema.properties?.[item]?.enum"
                                      @update:file="file => handleMultipleFileUpdate(file, item)"
                  />
                </div>
              </el-form-item>

            </el-form>

          </div>
            </transition>
          </el-scrollbar>
        </div>
      </div>
    </el-col>
    <el-col :span="2" :xs="1" />
  </el-row>

</div>
</template>

<style scoped>

.content {
  width: 100%;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  height: 100%;


}
.content-main {
  width: calc(100% - 40px);
  padding: 20px;
}
.main-area {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.head-area {
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 10px;
  border-bottom: 1px solid #e4e7ed;
  margin-bottom: 20px;
}
.head-area-right {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 10px;
}
.el-button {
  transition: all 0.3s ease;
}

.el-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
.main-form-area {
  width: 100%;
  max-height: calc(100vh - 500px);
}
.el-form-item {
  margin-bottom: 20px;
}
#upload-box {
  position: fixed;
  bottom: 250px;
  right: 380px;
  max-width: 200px;
  z-index: 99;
}
.dropdown-enter-active {
  transition: all 0.5s ease-out;
}
.dropdown-leave-active {
  transition: all 0.5s ease-in;
}

.dropdown-enter-from {
  transform: translateY(-100%) scaleY(0);
  opacity: 0;
}
.dropdown-enter-to {
  transform: translateY(0) scaleY(1);
  opacity: 1;
}

.dropdown-leave-from {
  transform: translateY(0) scaleY(1);
  opacity: 1;
}
.dropdown-leave-to {
  transform: translateY(-100%) scaleY(0);
  opacity: 0;
}
</style>
