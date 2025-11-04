<template>
  <el-scrollbar style="width: 100%">
    <div
      ref="editableDiv"
      contenteditable="true"
      class="editableDiv"
      :style="{ height: height + 'px' }"
      :data-placeholder="placeholder"
      @input="handleInput"
      @blur="handleBlur"
    />
    <div
      v-show="showParamsListFlag"
      ref="paramsBox"
      class="input-params-box"
      :style="{ left: divLeft + 'px', top: divTop + 'px' }"
      @blur="showParamsListFlag = false"
    >
      <el-scrollbar style="width: 100%">
        <div class="input-param-list">
          <el-divider>
            <el-text>输入变量</el-text>
          </el-divider>
          <div
            v-for="key in localNodeDetail?.node_input_params_json_schema?.ncOrders"
            :key="key"
            class="input-param"
            @click="clickParams(key, $event)"
          >
            <div>
              <el-text>
                {{ key }}
              </el-text>
            </div>
            <div>
              <el-tag type="primary">
                {{ localNodeDetail?.node_input_params_json_schema?.properties[key].type }}
              </el-tag>
            </div>
          </div>
          <el-divider>
            <el-text>输出变量</el-text>
          </el-divider>
          <div
            v-for="key in localNodeDetail?.node_result_params_json_schema?.ncOrders"
            :key="key"
            class="input-param"
            @click="clickParams(key, $event)"
          >
            <div>
              <el-text>
                {{ key }}
              </el-text>
            </div>
            <div>
              <el-tag type="primary">
                {{ localNodeDetail?.node_result_params_json_schema?.properties[key].type }}
              </el-tag>
            </div>
          </div>
          <div
            v-show="
              !localNodeDetail?.node_input_params_json_schema?.properties ||
              !Object.keys(localNodeDetail?.node_input_params_json_schema?.properties)
            "
            class="std-middle-box"
          >
            <el-empty description="暂无输入变量，请先配置" />
          </div>
        </div>
      </el-scrollbar>
    </div>
  </el-scrollbar>
</template>

<script setup>
import { ref, defineProps, defineEmits, onMounted, watch, nextTick } from 'vue';
const props = defineProps({
  value: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: '请输入内容'
  },
  node: {
    type: Object,
    default: null
  }
});
const height = ref(300); // 初始高度
const emits = defineEmits(['update:value']);
const editableDiv = ref(null);
const localNodeDetail = ref();
const showParamsListFlag = ref(false);
const paramsBox = ref();
// 控制浮动 div 的显示
// 浮动 div 的 left 位置
const divLeft = ref(0);
// 浮动 div 的 top 位置
const divTop = ref(0);
const savedPosition = ref(null); // 用于保存光标位置

function handleBlur() {
  const htmlContent = editableDiv.value.innerHTML;
  // 触发 update:value 事件，将新的值传递给外部
  if (htmlContent !== props.value) {
    // 如果内容有变化，则触发事件
    emits('update:value', htmlContent);
  }
  nextTick();
  // 保存光标位置
  const selection = window.getSelection();
  try {
    const range = selection.getRangeAt(0);
    savedPosition.value = {
      startPath: getNodePath(range.startContainer, editableDiv.value),
      startOffset: range.startOffset,
      endPath: getNodePath(range.endContainer, editableDiv.value),
      endOffset: range.endOffset
    };
  } catch (e) {
    console.log(e);
  }
}
const handleInput = () => {
  if (editableDiv.value.innerHTML.trim() === '<br>') {
    // 如果只包含 <br> 标签，则清空 div
    editableDiv.value.innerHTML = '';
  }
  // 根据光标前一个字符是不是/ 来判断是否唤出参数列表
  const selection = window.getSelection();
  if (selection.rangeCount > 0) {
    const range = selection.getRangeAt(0);
    const container = range.startContainer;
    const offset = range.startOffset;
    let prevChar = '';
    if (container.nodeType === Node.TEXT_NODE) {
      if (offset > 0) {
        prevChar = container.textContent[offset - 1];
      }
    } else {
      // 如果容器不是文本节点，尝试查找前一个文本节点
      if (container.childNodes.length > 0 && offset > 0) {
        const prevChild = container.childNodes[offset - 1];
        if (prevChild.nodeType === Node.TEXT_NODE) {
          prevChar = prevChild.textContent.slice(-1);
        }
      }
    }
    if (prevChar === '/') {
      // 显示参数列表
      setTimeout(() => {
        showParamsList();
      }, 10);
    } else {
      showParamsListFlag.value = false;
    }
  }
};
async function showParamsList() {
  const selection = window.getSelection();
  showParamsListFlag.value = true;
  await nextTick();

  if (selection.rangeCount > 0) {
    const range = selection.getRangeAt(0);
    const rect = range.getBoundingClientRect();

    // 获取视窗的宽度和高度
    const windowWidth = window.innerWidth;
    const windowHeight = window.innerHeight;

    // 计算 div 的宽度和高度
    const floatingDiv = paramsBox.value;
    const floatingDivWidth = floatingDiv.offsetWidth;
    const floatingDivHeight = floatingDiv.offsetHeight;

    // 默认位置：在光标右下方
    let left = rect.right;
    let top = rect.bottom;

    // 检查是否超出视窗右边
    if (left + floatingDivWidth > windowWidth) {
      left = rect.left - floatingDivWidth;
      // 如果左边也超出，则强制在视窗内
      if (left < 0) left = 0;
    }

    // 检查是否超出视窗底部
    if (top + floatingDivHeight > windowHeight) {
      top = rect.top - floatingDivHeight;
      // 如果顶部也超出，则强制在视窗内
      if (top < 0) top = 0;
    }

    // 确保不会超出视窗左侧
    if (left < 0) left = 0;

    // 确保不会超出视窗顶部
    if (top < 0) top = 0;

    // 应用计算后的位置
    divLeft.value = left;
    divTop.value = top;
  }

  await nextTick();
  // 添加焦点逻辑
  focusParamsBox();
}
function focusParamsBox() {
  if (paramsBox.value) {
    // 设置tabindex使div可聚焦
    paramsBox.value.setAttribute('tabindex', '-1');
    // 聚焦参数框
    paramsBox.value.focus();
  }
}

function clickParams(key) {
  showParamsListFlag.value = false;
  let keyType = localNodeDetail.value?.node_input_params_json_schema?.properties[key]?.type;
  if (!keyType) {
    keyType = localNodeDetail.value?.node_result_params_json_schema?.properties[key]?.type;
  }
  // 创建变量元素
  const variableElement = document.createElement('div');
  variableElement.className = 'dy-variable';
  variableElement.setAttribute('contenteditable', 'false');
  variableElement.innerHTML = `<strong>${key}</strong> (${keyType})`;
  editableDiv.value?.focus();
  nextTick();
  // 恢复光标位置（增加安全检查）
  if (savedPosition.value) {
    try {
      const startNode = getNodeByPath(savedPosition.value.startPath, editableDiv.value);
      const endNode = getNodeByPath(savedPosition.value.endPath, editableDiv.value);

      // 验证节点有效性
      if (!startNode || !endNode) {
        console.log('Invalid saved position nodes', savedPosition.value, startNode, endNode);
        savedPosition.value = null;
        return;
      }

      // 验证偏移量
      const maxStartOffset =
        startNode.nodeType === Node.TEXT_NODE ? startNode.textContent.length : startNode.childNodes.length;
      const maxEndOffset = endNode.nodeType === Node.TEXT_NODE ? endNode.textContent.length : endNode.childNodes.length;

      if (savedPosition.value.startOffset > maxStartOffset || savedPosition.value.endOffset > maxEndOffset) {
        console.warn('Saved offsets out of range');
        savedPosition.value = null;
        return;
      }

      const selection = window.getSelection();
      if (selection) {
        const range = document.createRange();
        range.setStart(startNode, Math.min(savedPosition.value.startOffset, maxStartOffset));
        range.setEnd(endNode, Math.min(savedPosition.value.endOffset, maxEndOffset));
        selection.removeAllRanges();
        selection.addRange(range);
      }
    } catch (e) {
      console.error('Error restoring selection:', e);
      savedPosition.value = null;
    }
  }
  // 插入变量元素
  handleParamsRefInsert(variableElement);
  editableDiv.value?.focus();
}
function handleParamsRefInsert(variableElement) {
  const selection = window.getSelection();
  if (selection.rangeCount > 0) {
    const range = selection.getRangeAt(0);
    const container = range.startContainer;
    const offset = range.startOffset;
    let prevChar = '';
    if (container.nodeType === Node.TEXT_NODE) {
      if (offset > 0) {
        prevChar = container.textContent[offset - 1];
        if (prevChar === '/') {
          container.textContent = container.textContent.slice(0, offset - 1) + container.textContent.slice(offset);
          const newRange = document.createRange();
          newRange.setStart(container, offset - 1);
          newRange.insertNode(variableElement);
          newRange.setStartAfter(variableElement);
          newRange.collapse(true);
          selection.removeAllRanges();
          selection.addRange(newRange);
        }
      }
    } else {
      if (container.childNodes.length > 0 && offset > 0) {
        const prevChild = container.childNodes[offset - 1];
        if (prevChild.nodeType === Node.TEXT_NODE) {
          prevChar = prevChild.textContent.slice(-1);
          if (prevChar === '/') {
            prevChild.textContent = prevChild.textContent.slice(0, -1);

            const newRange = document.createRange();
            newRange.setStart(prevChild, prevChild.textContent.length);
            newRange.insertNode(variableElement);

            newRange.setStartAfter(variableElement);
            newRange.collapse(true);
            selection.removeAllRanges();
            selection.addRange(newRange);
          }
        }
      }
    }
  }
}
onMounted(() => {
  // 初始判断是否显示 placeholder
  localNodeDetail.value = props.node;
  editableDiv.value.innerHTML = props.value.replace(/\n/g, '<br>');
  showParamsListFlag.value = false;
});
watch(
  () => props.node,
  newVal => {
    if (newVal.id !== localNodeDetail.value?.id) {
      showParamsListFlag.value = false; // 隐藏参数列表
    }
    localNodeDetail.value = newVal;
  }
);
watch(
  () => props.value,
  newVal => {
    editableDiv.value.innerHTML = newVal.replace(/\n/g, '<br>');
  }
);
function getNodePath(node, root) {
  const path = [];

  // 验证输入参数
  if (!node || !root) return path;

  try {
    // 遍历父节点直到根节点
    while (node && node !== root && node !== document) {
      const index = getNodeIndex(node);
      if (index === -1) break; // 节点不在父节点的子节点列表中

      path.unshift(index);
      node = node.parentNode;

      // 防止无限循环
      if (path.length > 1000) {
        console.warn('Path too long, possible circular reference');
        return [];
      }
    }

    // 确保最终到达的是我们指定的根节点
    if (node !== root) {
      return [];
    }

    return path;
  } catch (error) {
    console.error('Error getting node path:', error);
    return [];
  }
}
function getNodeIndex(node) {
  if (!node || !node.parentNode) return -1;

  const children = node.parentNode.childNodes;
  for (let i = 0; i < children.length; i++) {
    if (children[i] === node) return i;
  }
  return -1;
}
function getNodeByPath(path, root) {
  // 验证输入参数
  if (!Array.isArray(path) || !root) return null;

  try {
    let node = root;

    // 遍历路径中的每个索引
    for (const index of path) {
      // 验证索引有效性
      if (typeof index !== 'number' || index < 0 || !node.childNodes || index >= node.childNodes.length) {
        return null;
      }

      node = node.childNodes[index];

      // 防止无限循环
      if (path.length > 1000) {
        console.warn('Path too long, possible circular reference');
        return null;
      }
    }

    return node;
  } catch (error) {
    console.error('Error getting node by path:', error);
    return null;
  }
}
</script>

<style scoped>
.std-middle-box {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  width: 100%;
}
.editableDiv {
  border-radius: 6px;
  padding: 6px;
  width: calc(100% - 15px);
  border: 1px solid #ccc;
  resize: vertical;
  overflow: auto;
  position: relative;
}
.editableDiv:focus-visible {
  /* 获得焦点时的边框样式 */
  outline-width: 0;
  border: 1px solid #409eff;
}
.editableDiv:empty::before {
  content: attr(data-placeholder);
  color: #999;
}
.input-params-box {
  position: fixed;
  top: 140px;
  right: 20px;
  max-height: 50vh;
  width: 400px;
  background: white;
  z-index: 999;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  gap: 12px;
  padding: 12px;
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  box-shadow:
    0 4px 8px rgba(0, 0, 0, 0.1),
    0 6px 20px rgba(0, 0, 0, 0.1); /* 阴影效果 */
}
.input-params-box:focus-visible {
  outline: none;
}
.input-param-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
  width: 100%;
  justify-content: flex-start;
  align-items: flex-start;
  max-height: 50vh;
}
.input-param {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  width: calc(100% - 12px);
  padding: 6px;
  gap: 12px;
  cursor: pointer;
  border-radius: 8px;
}
.input-param:hover {
  background-color: #f5f5f5;
}
</style>
