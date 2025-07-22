<script setup lang="ts">
import {computed, nextTick, onMounted, ref, watch} from "vue";
import * as echarts from "echarts";
import {md_answer} from "@/components/next_console/messages_flow/message_flow";
const props = defineProps({
  options: {
    type: Object,
    default: null,
  },
  msgId: {
    type: Number,
    default: ''
  },
  rawData: {
    type: Object,
    default: () => ([]),
  },
  sql: {
    type: String,
    default: ''
  },
  columns: {
    type: Array,
    default: () => ([])
  },
  pane: {
    type: String,
    default: 'data'
  },
})
const graphType = ref('data');
const sqlHtml = ref('');
let myChart = null
function getSqlHtml() {
  if (props.sql) {
    const sqlStr = "```sql\n" + props.sql;
    sqlHtml.value = md_answer.render(sqlStr);
  } else {
    sqlHtml.value = '无';
  }
}
function changeGraphSize(){
  // 修改div的宽度：600px window.innerWidth 的较小值
  const graphContent = document.getElementById(dynamicId.value);
  if (graphContent) {
    graphContent.style.width = `${Math.min(600, window.innerWidth - 120 )}px`;
  }
  if (myChart) {
    myChart.resize();
  }
}
const dynamicId = computed(() => {
  return `graph-content-${props.msgId}`;
});
onMounted(() => {
  // init sql html
  getSqlHtml();
  if (props.options != null) {
    try {
      myChart = echarts.init(document.getElementById(dynamicId.value))
      myChart.setOption( props.options);
    }
    catch (e) {
      console.error('echarts init error', e);
    }

  }
  window.addEventListener('resize', changeGraphSize);
  nextTick(() => {
    changeGraphSize();
  });
});
watch(
    () => props.options,
    (newOptions) => {
      console.log(newOptions, myChart)
      if (!myChart) {
        myChart = echarts.init(document.getElementById(dynamicId.value))
      }
      myChart.setOption(newOptions);
    },
    { deep: true } // 深度监听，确保对象内部属性的变化也能触发
);
watch(
    () => props.pane,
    (newPane) => {
      console.log(newPane)
      graphType.value = newPane;
    },
    { immediate: true }
);
</script>

<template>
  <div class="agent-graph-main">
    <el-tabs v-model="graphType">
      <el-tab-pane label="数据" name="data">
        <el-scrollbar>
          <div class="graph-content">
            <el-table :data="props.rawData" height="380px" border>
              <el-table-column v-for="col in props.columns" :prop="col" :label="col" />

            </el-table>
          </div>
        </el-scrollbar>

      </el-tab-pane>
      <el-tab-pane label="SQL" name="sql">
        <el-scrollbar>
          <div class="graph-content">
            <div v-html="sqlHtml"></div>
          </div>
        </el-scrollbar>
      </el-tab-pane>
      <el-tab-pane label="可视化" name="graph">
        <div v-show="props.options" class="graph-content" :id='dynamicId' />
        <el-empty v-show="!props.options" description="暂时不支持渲染此类数据"/>
      </el-tab-pane>
    </el-tabs>
  </div>

</template>

<style scoped>
.agent-graph-main{
  width: 100%;
  height: 400px;
}
.graph-content{
  width: 600px;
  height: 380px;
}
</style>
