<template>
  <div class="resource-editor">
    <!-- 顶部操作栏 -->
    <div class="action-bar">
      <button class="save-btn" :disabled="saving" @click="handleSave">
        <span v-if="saving">保存中...</span>
        <span v-else>保存</span>
      </button>
      <div v-if="lastSavedTime" class="last-saved">上次保存: {{ formatTime(lastSavedTime) }}</div>
    </div>

    <!-- 工具栏 -->
    <div v-if="editor" class="toolbar">
      <!-- 文本样式 -->
      <button
        :class="{ 'is-active': editor.isActive('bold') }"
        class="toolbar-btn"
        title="粗体"
        @click="editor.chain().focus().toggleBold().run()"
      >
        <span class="icon">B</span>
      </button>

      <button
        :class="{ 'is-active': editor.isActive('italic') }"
        class="toolbar-btn"
        title="斜体"
        @click="editor.chain().focus().toggleItalic().run()"
      >
        <span class="icon">I</span>
      </button>

      <button
        :class="{ 'is-active': editor.isActive('underline') }"
        class="toolbar-btn"
        title="下划线"
        @click="editor.chain().focus().toggleUnderline().run()"
      >
        <span class="icon">U</span>
      </button>

      <button
        :class="{ 'is-active': editor.isActive('strike') }"
        class="toolbar-btn"
        title="删除线"
        @click="editor.chain().focus().toggleStrike().run()"
      >
        <span class="icon" style="text-decoration-line: line-through"> S </span>
      </button>

      <div class="toolbar-divider" />
      <button
        :class="{ 'is-active': editor.isActive('paragraph') }"
        class="toolbar-btn"
        title="正文"
        @click="editor.chain().focus().setParagraph().run()"
      >
        <span class="icon">¶</span>
      </button>
      <!-- 标题 -->
      <button
        :class="{ 'is-active': editor.isActive('heading', { level: 1 }) }"
        class="toolbar-btn"
        title="标题1"
        @click="editor.chain().focus().toggleHeading({ level: 1 }).run()"
      >
        H1
      </button>

      <button
        :class="{ 'is-active': editor.isActive('heading', { level: 2 }) }"
        class="toolbar-btn"
        title="标题2"
        @click="editor.chain().focus().toggleHeading({ level: 2 }).run()"
      >
        H2
      </button>

      <button
        :class="{ 'is-active': editor.isActive('heading', { level: 3 }) }"
        class="toolbar-btn"
        title="标题3"
        @click="editor.chain().focus().toggleHeading({ level: 3 }).run()"
      >
        H3
      </button>

      <div class="toolbar-divider" />

      <!-- 列表 -->
      <button
        :class="{ 'is-active': editor.isActive('bulletList') }"
        class="toolbar-btn"
        title="无序列表"
        @click="editor.chain().focus().toggleBulletList().run()"
      >
        <span class="icon">•</span>
      </button>

      <button
        :class="{ 'is-active': editor.isActive('orderedList') }"
        class="toolbar-btn"
        title="有序列表"
        @click="editor.chain().focus().toggleOrderedList().run()"
      >
        <span class="icon">1.</span>
      </button>

      <div class="toolbar-divider" />

      <!-- 对齐方式 -->
      <button
        :class="{ 'is-active': editor.isActive({ textAlign: 'left' }) }"
        class="toolbar-btn"
        title="左对齐"
        @click="editor.chain().focus().setTextAlign('left').run()"
      >
        <span class="icon">左</span>
      </button>

      <button
        :class="{ 'is-active': editor.isActive({ textAlign: 'center' }) }"
        class="toolbar-btn"
        title="居中"
        @click="editor.chain().focus().setTextAlign('center').run()"
      >
        <span class="icon">中</span>
      </button>

      <button
        :class="{ 'is-active': editor.isActive({ textAlign: 'right' }) }"
        class="toolbar-btn"
        title="右对齐"
        @click="editor.chain().focus().setTextAlign('right').run()"
      >
        <span class="icon">右</span>
      </button>
      <button
        :class="{ 'is-active': editor.isActive('superscript') }"
        class="toolbar-btn"
        title="上标"
        @click="toggleSuperscript"
      >
        <span class="icon">x²</span>
      </button>

      <!-- 下标 -->
      <button
        :class="{ 'is-active': editor.isActive('subscript') }"
        class="toolbar-btn"
        title="下标"
        @click="toggleSubscript"
      >
        <span class="icon">x₂</span>
      </button>

      <!-- 表情符号 -->
      <button class="toolbar-btn" title="表情符号" @click="emojiDialogVisible = true">
        <span class="icon">😊</span>
      </button>

      <!-- 公式 -->
      <button class="toolbar-btn" title="插入公式" @click="formulaDialogVisible = true">
        <span class="icon">∑</span>
      </button>

      <!-- 字数统计 -->
      <div class="word-count" title="字数统计">{{ wordCount }} 字</div>

      <!-- 预览 -->
      <button :class="{ 'is-active': previewMode }" class="toolbar-btn" title="预览模式" @click="togglePreview">
        <span class="icon">👁️</span>
      </button>
      <div class="toolbar-divider" />

      <!-- 链接 -->
      <button
        :class="{
          'is-active': editor.isActive('link'),
          'link-active': editor.isActive('link')
        }"
        class="toolbar-btn"
        :title="editor.isActive('link') ? '取消链接' : '添加链接'"
        @click="setLink"
      >
        <span class="icon">{{ editor.isActive('link') ? '🔗❌' : '🔗' }}</span>
      </button>

      <!-- 图片上传 -->
      <label for="image-upload" class="toolbar-btn" title="上传图片">
        <span class="icon">🖼️</span>
        <input id="image-upload" type="file" accept="image/*" style="display: none" @change="handleImageUpload" />
      </label>

      <!-- 多媒体上传 -->
      <label for="media-upload" class="toolbar-btn" title="上传多媒体">
        <span class="icon">🎬</span>
        <input
          id="media-upload"
          type="file"
          accept="video/*,audio/*"
          style="display: none"
          @change="handleMediaUpload"
        />
      </label>

      <div class="toolbar-divider" />

      <!-- 代码块 -->
      <button
        :class="{ 'is-active': editor.isActive('codeBlock') }"
        class="toolbar-btn"
        title="代码块"
        @click="editor.chain().focus().toggleCodeBlock().run()"
      >
        <span class="icon">{}</span>
      </button>

      <!-- 引用 -->
      <button
        :class="{ 'is-active': editor.isActive('blockquote') }"
        class="toolbar-btn"
        title="引用"
        @click="editor.chain().focus().toggleBlockquote().run()"
      >
        <span class="icon">❝</span>
      </button>

      <!-- 分隔线 -->
      <button class="toolbar-btn" title="分隔线" @click="editor.chain().focus().setHorizontalRule().run()">
        <span class="icon">—</span>
      </button>

      <div class="toolbar-divider" />

      <!-- 撤销/重做 -->
      <button
        :disabled="!editor.can().undo()"
        class="toolbar-btn"
        title="撤销"
        @click="editor.chain().focus().undo().run()"
      >
        <span class="icon">↩</span>
      </button>

      <button
        :disabled="!editor.can().redo()"
        class="toolbar-btn"
        title="重做"
        @click="editor.chain().focus().redo().run()"
      >
        <span class="icon">↪</span>
      </button>
    </div>

    <!-- 编辑器内容区域 -->
    <el-scrollbar>
      <EditorContent :editor="editor" class="editor-content" />
    </el-scrollbar>
    <!-- 链接输入对话框 -->
    <div v-if="linkDialogVisible" class="dialog-overlay">
      <div class="link-dialog">
        <h3>添加链接</h3>
        <input v-model="linkUrl" type="text" placeholder="输入链接地址" class="link-input" @keyup.enter="confirmLink" />
        <div class="dialog-actions">
          <button class="dialog-btn primary" @click="confirmLink">确认</button>
          <button class="dialog-btn" @click="cancelLink">取消</button>
        </div>
      </div>
    </div>
  </div>
  <!-- 表情符号对话框 -->
  <div v-if="emojiDialogVisible" class="dialog-overlay">
    <div class="emoji-dialog">
      <h3>选择表情符号</h3>
      <div class="emoji-grid">
        <button
          v-for="emoji in ['😀', '😊', '😂', '❤️', '👍', '🎉', '⭐', '🔥', '📚', '💡']"
          :key="emoji"
          class="emoji-btn"
          @click="insertEmoji(emoji)"
        >
          {{ emoji }}
        </button>
      </div>
      <div class="dialog-actions">
        <button class="dialog-btn" @click="emojiDialogVisible = false">取消</button>
      </div>
    </div>
  </div>

  <!-- 公式对话框 -->
  <div v-if="formulaDialogVisible" class="dialog-overlay">
    <div class="formula-dialog">
      <h3>插入数学公式</h3>

      <div class="formula-input-group">
        <input
          v-model="formulaInput"
          type="text"
          placeholder="输入LaTeX公式，如: E=mc^2"
          class="formula-input"
          @keyup.enter="insertInlineFormula"
        />
        <div class="input-actions">
          <button class="clear-btn" title="清空" @click="formulaInput = ''">🗑️</button>
        </div>
      </div>

      <!-- KaTeX 预览 -->
      <div v-if="formulaInput" class="formula-preview">
        <div class="preview-label">行内公式预览:</div>
        <div class="katex-preview" v-html="renderFormulaPreview(formulaInput)" />

        <div class="preview-label" style="margin-top: 12px">块级公式预览:</div>
        <div class="katex-preview display" v-html="renderDisplayFormula(formulaInput)" />
      </div>

      <!-- 公式示例 -->
      <div v-if="!formulaInput" class="formula-examples">
        <div class="examples-label">常用公式:</div>
        <div class="example-grid">
          <button
            v-for="(example, index) in formulaExamples"
            :key="index"
            class="example-btn"
            :title="example.description"
            @click="formulaInput = example.formula"
          >
            <div class="example-preview" v-html="renderFormulaPreview(example.formula)" />
            <span class="example-name">{{ example.name }}</span>
          </button>
        </div>
      </div>

      <div class="formula-actions">
        <div class="insert-buttons">
          <button class="dialog-btn primary" @click="insertInlineFormula">插入行内公式</button>
          <button class="dialog-btn primary" @click="insertDisplayFormula">插入块级公式</button>
        </div>
        <button class="dialog-btn" @click="formulaDialogVisible = false">取消</button>
      </div>

      <div class="formula-help">
        <details>
          <summary>LaTeX 语法帮助</summary>
          <div class="help-content">
            <p><strong>分数:</strong> <code>\frac{a}{b}</code></p>
            <p><strong>上下标:</strong> <code>x^2</code>, <code>x_1</code></p>
            <p><strong>根号:</strong> <code>\sqrt{x}</code>, <code>\sqrt[n]{x}</code></p>
            <p><strong>希腊字母:</strong> <code>\alpha</code>, <code>\beta</code>, <code>\pi</code></p>
            <p><strong>积分:</strong> <code>\int_a^b f(x)dx</code></p>
            <p><strong>求和:</strong> <code>\sum_{i=1}^n</code></p>
          </div>
        </details>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import Image from '@tiptap/extension-image';
import Link from '@tiptap/extension-link';
import Subscript from '@tiptap/extension-subscript';
import Superscript from '@tiptap/extension-superscript';
import TextAlign from '@tiptap/extension-text-align';
import Typography from '@tiptap/extension-typography';
import Underline from '@tiptap/extension-underline';
import StarterKit from '@tiptap/starter-kit';
import { useEditor, EditorContent } from '@tiptap/vue-3';
import katex from 'katex';
import { watch, onBeforeUnmount, ref, nextTick, reactive } from 'vue';
import 'katex/dist/katex.min.css';
import { ResourceItem } from '@/types/resource-type';

// 新增状态变量
const currentViewResource = reactive<ResourceItem>(
  // @ts-ignore
  {
    sub_rag_file_cnt: 0,
    id: null,
    resource_parent_id: null,
    user_id: null,
    resource_name: null,
    resource_type: null,
    resource_desc: null,
    resource_icon: null,
    resource_format: null,
    resource_path: null,
    resource_size_in_MB: null,
    resource_status: null,
    ref_status: null,
    create_time: null,
    update_time: null,
    delete_time: null,
    show_buttons: null,
    resource_parent_name: null,
    resource_is_selected: null,
    sub_resource_dir_cnt: null,
    sub_resource_file_cnt: null,
    resource_feature_code: '',
    resource_is_supported: false,
    resource_show_url: '',
    resource_source_url: '',
    resource_title: '',
    resource_source: 'resource_center',
    ref_text: null,
    rerank_score: null,
    view_config: {
      engine: 'tiptap',
      read_only: false
    }
  }
);
const emojiDialogVisible = ref(false);
const formulaDialogVisible = ref(false);
const previewMode = ref(false);
const wordCount = ref(0);
const formulaInput = ref('');

interface IProps {
  modelValue?: string;
  placeholder?: string;
  resourceId?: string | number;
}

const props = withDefaults(defineProps<IProps>(), {
  modelValue: '',
  placeholder: '开始输入内容...',
  resourceId: undefined
});

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void;
  (e: 'save', content: string, resourceId?: string | number): Promise<boolean>;
}>();

// 编辑器实例
const editor = useEditor({
  content: props.modelValue,
  extensions: [
    StarterKit,
    Underline,
    Link.configure({
      openOnClick: false,
      // eslint-disable-next-line @typescript-eslint/naming-convention
      HTMLAttributes: {
        class: 'editor-link',
        target: '_blank',
        rel: 'noopener noreferrer'
      }
    }),
    Image.configure({
      // eslint-disable-next-line @typescript-eslint/naming-convention
      HTMLAttributes: {
        class: 'editor-image'
      }
    }),
    TextAlign.configure({
      types: ['heading', 'paragraph']
    }),
    Superscript,
    Subscript,
    Typography
  ],
  editorProps: {
    attributes: {
      class: 'prose prose-sm sm:prose lg:prose-lg xl:prose-2xl mx-auto focus:outline-none',
      placeholder: props.placeholder
    }
  },
  onUpdate: () => {
    if (editor.value) {
      emit('update:modelValue', editor.value.getHTML());
    }
  }
});

// 状态管理
const saving = ref(false);
const lastSavedTime = ref<Date | null>(null);
const linkDialogVisible = ref(false);
const linkUrl = ref('');

// 监听编辑器内容变化，更新字数统计
watch(
  () => editor.value?.getText(),
  text => {
    if (text) {
      // 简单的字数统计（中文字符算一个词，英文单词按空格分割）
      const chineseChars = text.match(/[\u4e00-\u9fa5]/g) || [];
      const englishWords = text
        .replace(/[\u4e00-\u9fa5]/g, '')
        .trim()
        .split(/\s+/)
        .filter(word => word.length > 0);
      wordCount.value = chineseChars.length + englishWords.length;
    } else {
      wordCount.value = 0;
    }
  }
);

// 上标功能
const toggleSuperscript = () => {
  editor.value?.chain().focus().toggleSuperscript().run();
};

// 下标功能
const toggleSubscript = () => {
  editor.value?.chain().focus().toggleSubscript().run();
};

// 表情符号功能
const insertEmoji = (emoji: string) => {
  editor.value?.chain().focus().insertContent(emoji).run();
  emojiDialogVisible.value = false;
};

// 数学公式功能
const renderFormulaPreview = (formula: string): string => {
  try {
    return katex.renderToString(formula, {
      displayMode: false,
      throwOnError: false,
      errorColor: '#cc0000',
      output: 'html',
      strict: false
    });
  } catch (error) {
    return `<span class="formula-error">公式渲染错误: ${error}</span>`;
  }
};

const renderDisplayFormula = (formula: string): string => {
  try {
    return katex.renderToString(formula, {
      displayMode: true,
      throwOnError: false,
      errorColor: '#cc0000'
    });
  } catch (error) {
    return `<div class="formula-error">公式渲染错误: ${error}</div>`;
  }
};

// 修改插入公式函数
const insertFormula = (isDisplayMode: boolean = false) => {
  if (formulaInput.value.trim()) {
    try {
      const formulaHtml = isDisplayMode
        ? renderDisplayFormula(formulaInput.value)
        : renderFormulaPreview(formulaInput.value);

      const data = `<div class="example-preview" data-formula="${formulaInput.value}" data-display="true">${formulaHtml}</div>`;
      console.log(data, typeof data);
      editor.value?.chain().focus().insertContent(data).run();

      formulaInput.value = '';
      formulaDialogVisible.value = false;
    } catch (error) {
      console.error('公式插入错误:', error);
    }
  }
};

const insertInlineFormula = () => insertFormula(false);
const insertDisplayFormula = () => insertFormula(true);

// 更新公式示例
const formulaExamples = ref([
  {
    name: '二次公式',
    formula: 'x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}',
    description: '二次方程求根公式'
  },
  {
    name: '勾股定理',
    formula: 'a^2 + b^2 = c^2',
    description: '直角三角形边长关系'
  },
  {
    name: '欧拉公式',
    formula: 'e^{i\\pi} + 1 = 0',
    description: '数学中最优美的公式'
  },
  {
    name: '求和',
    formula: '\\sum_{i=1}^n i = \\frac{n(n+1)}{2}',
    description: '等差数列求和'
  },
  {
    name: '积分',
    formula: '\\int_a^b f(x)\\,dx = F(b) - F(a)',
    description: '微积分基本定理'
  },
  {
    name: '矩阵',
    formula: '\\begin{pmatrix} a & b \\\\ c & d \\end{pmatrix}',
    description: '2x2矩阵'
  }
]);
// 重新渲染所有公式（用于内容加载时）
const renderAllFormulas = () => {
  nextTick(() => {
    document.querySelectorAll('.katex-formula').forEach(element => {
      const formula = element.getAttribute('data-formula');
      const isDisplay = element.getAttribute('data-display') === 'true';

      if (formula) {
        try {
          const html = isDisplay ? renderDisplayFormula(formula) : renderFormulaPreview(formula);
          element.innerHTML = html;
        } catch (error) {
          element.innerHTML = `<span class="formula-error">渲染错误</span>`;
        }
      }
    });
  });
};

// 监听内容变化重新渲染公式
watch(
  () => editor.value?.getHTML(),
  () => {
    // renderAllFormulas();
  }
);

// 预览模式切换
const togglePreview = () => {
  previewMode.value = !previewMode.value;
};

// 修改链接功能 - 支持取消链接
const setLink = () => {
  if (!editor.value) return;

  if (editor.value.isActive('link')) {
    // 如果当前已选中链接，则取消链接
    editor.value.chain().focus().extendMarkRange('link').unsetLink().run();
  } else {
    // 否则打开链接对话框
    const previousUrl = editor.value.getAttributes('link').href;
    linkUrl.value = previousUrl || '';
    linkDialogVisible.value = true;
  }
};
// 监听外部内容变化
watch(
  () => props.modelValue,
  newValue => {
    if (editor.value && newValue !== editor.value.getHTML()) {
      editor.value.commands.setContent(newValue);
    }
  }
);

// 保存处理
const handleSave = async () => {
  if (!editor.value || saving.value) return;

  saving.value = true;
  try {
    const content = editor.value.getHTML();
    console.log(content);
    const success = await emit('save', content, props.resourceId);

    if (success) {
      lastSavedTime.value = new Date();
    }
  } catch (error) {
    console.error('保存失败:', error);
  } finally {
    saving.value = false;
  }
};

const confirmLink = () => {
  if (editor.value) {
    if (linkUrl.value) {
      editor.value.chain().focus().extendMarkRange('link').setLink({ href: linkUrl.value }).run();
    } else {
      editor.value.chain().focus().extendMarkRange('link').unsetLink().run();
    }
  }
  linkDialogVisible.value = false;
};

const cancelLink = () => {
  linkDialogVisible.value = false;
};

// 图片上传
const handleImageUpload = (event: Event) => {
  const input = event.target as HTMLInputElement;
  if (!input.files?.length || !editor.value) return;

  const file = input.files[0];
  const reader = new FileReader();

  reader.onload = e => {
    const result = e.target?.result;
    if (typeof result === 'string') {
      // 插入图片到编辑器
      editor.value.chain().focus().setImage({ src: result }).run();
    }
  };

  reader.readAsDataURL(file);
  input.value = ''; // 清除文件输入
};

// 多媒体上传
const handleMediaUpload = (event: Event) => {
  const input = event.target as HTMLInputElement;
  if (!input.files?.length || !editor.value) return;

  const file = input.files[0];
  const reader = new FileReader();

  reader.onload = e => {
    const result = e.target?.result;
    if (typeof result === 'string') {
      // 根据文件类型插入多媒体
      if (file.type.startsWith('video/')) {
        editor.value
          .chain()
          .focus()
          .insertContent(`<video controls src="${result}" class="editor-media"></video>`)
          .run();
      } else if (file.type.startsWith('audio/')) {
        editor.value
          .chain()
          .focus()
          .insertContent(`<audio controls src="${result}" class="editor-media"></audio>`)
          .run();
      }
    }
  };

  reader.readAsDataURL(file);
  input.value = ''; // 清除文件输入
};

// 格式化时间
const formatTime = (date: Date) => {
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  });
};

onBeforeUnmount(() => {
  // 清理编辑器实例
  if (editor.value) {
    editor.value.destroy();
  }
});
</script>

<style scoped>
.resource-editor {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: white;
  overflow: hidden;
  /* 新增 */
  display: flex;
  flex-direction: column;
  height: 100%;
}

.action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid #e2e8f0;
  background: #f8fafc;
  flex-shrink: 0;
}

.save-btn {
  padding: 8px 16px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: background 0.2s;
}

.save-btn:hover:not(:disabled) {
  background: #2563eb;
}

.save-btn:disabled {
  background: #93c5fd;
  cursor: not-allowed;
}

.last-saved {
  color: #64748b;
  font-size: 14px;
}

.toolbar {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  padding: 12px;
  border-bottom: 1px solid #e2e8f0;
  background: #f8fafc;
}

.toolbar-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 32px;
  height: 32px;
  padding: 0 8px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  background: white;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.toolbar-btn:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
}

.toolbar-btn.is-active {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

.toolbar-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.toolbar-btn .icon {
  font-weight: bold;
}

.toolbar-divider {
  width: 1px;
  height: 24px;
  background: #e2e8f0;
  margin: 0 4px;
  align-self: center;
}

.editor-content {
  max-height: calc(100vh - 320px);
  padding: 16px;
  outline: none;
}

/* 对话框样式 */
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.link-d {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  max-width: 90%;
}
.link-dialog {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  max-width: 90%;
}
.link-dialog h3 {
  margin: 0 0 16px 0;
  font-size: 18px;
}

.link-input {
  width: calc(100% - 24px);
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  margin-bottom: 16px;
  font-size: 14px;
}

.dialog-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

.dialog-btn {
  padding: 8px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  background: white;
  cursor: pointer;
}
.dialog-btn.primary {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

.dialog-btn:hover {
  background: #f1f5f9;
}

.dialog-btn.primary:hover {
  background: #2563eb;
}

/* 编辑器内容样式 */
:deep(.ProseMirror) {
  outline: none;
  min-height: 250px;
  line-height: 1.6;
}

:deep(.ProseMirror p.is-editor-empty:first-child::before) {
  content: attr(data-placeholder);
  float: left;
  color: #adb5bd;
  pointer-events: none;
  height: 0;
}

:deep(.ProseMirror h1) {
  font-size: 2em;
  font-weight: bold;
  margin: 0.67em 0;
  color: #1f2937;
}

:deep(.ProseMirror h2) {
  font-size: 1.5em;
  font-weight: bold;
  margin: 0.83em 0;
  color: #374151;
}

:deep(.ProseMirror h3) {
  font-size: 1.17em;
  font-weight: bold;
  margin: 1em 0;
  color: #4b5563;
}

:deep(.ProseMirror ul),
:deep(.ProseMirror ol) {
  padding: 0 1rem;
  margin: 1rem 0;
}

:deep(.ProseMirror ul li) {
  list-style-type: disc;
}

:deep(.ProseMirror ol li) {
  list-style-type: decimal;
}

:deep(.ProseMirror blockquote) {
  border-left: 3px solid #3b82f6;
  margin: 1rem 0;
  padding-left: 1rem;
  color: #64748b;
  font-style: italic;
}

:deep(.ProseMirror code) {
  background-color: #f1f5f9;
  color: #1f2937;
  padding: 0.2rem 0.4rem;
  border-radius: 0.3rem;
  font-size: 0.85em;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
}

:deep(.ProseMirror pre) {
  background: #1f2937;
  color: #f8fafc;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  margin: 1rem 0;
  overflow-x: auto;
}

:deep(.ProseMirror pre code) {
  background: none;
  color: inherit;
  padding: 0;
  font-size: 0.8rem;
}

:deep(.ProseMirror hr) {
  border: none;
  border-top: 2px solid #e2e8f0;
  margin: 2rem 0;
}

/* 链接样式 */
:deep(.editor-link) {
  color: #3b82f6;
  text-decoration: underline;
  cursor: pointer;
}

:deep(.editor-link:hover) {
  color: #2563eb;
}

/* 图片样式 */
:deep(.editor-image) {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin: 1rem 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 多媒体样式 */
:deep(.editor-media) {
  max-width: 100%;
  border-radius: 8px;
  margin: 1rem 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 对齐样式 */
:deep([data-text-align='left']) {
  text-align: left;
}

:deep([data-text-align='center']) {
  text-align: center;
}

:deep([data-text-align='right']) {
  text-align: right;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .toolbar {
    padding: 8px;
    gap: 2px;
  }

  .toolbar-btn {
    min-width: 28px;
    height: 28px;
    font-size: 12px;
  }

  .action-bar {
    padding: 8px 12px;
    flex-direction: column;
    gap: 8px;
    align-items: flex-start;
  }

  .editor-content {
    padding: 12px;
    min-height: 200px;
  }
}

/* 动画效果 */
.save-btn {
  transition: all 0.3s ease;
}

.toolbar-btn {
  transition: all 0.2s ease;
}

/* 焦点状态 */
:deep(.ProseMirror:focus) {
  outline: none;
}

:deep(.ProseMirror-focused) {
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
}

/* 选中文本样式 */
:deep(.ProseMirror ::selection) {
  background: #bfdbfe;
}

:deep(.ProseMirror ::-moz-selection) {
  background: #bfdbfe;
}

/* 滚动条样式 */
:deep(.ProseMirror) {
  scrollbar-width: thin;
  scrollbar-color: #cbd5e1 #f8fafc;
}

:deep(.ProseMirror::-webkit-scrollbar) {
  width: 6px;
}

:deep(.ProseMirror::-webkit-scrollbar-track) {
  background: #f8fafc;
}

:deep(.ProseMirror::-webkit-scrollbar-thumb) {
  background: #cbd5e1;
  border-radius: 3px;
}

:deep(.ProseMirror::-webkit-scrollbar-thumb:hover) {
  background: #94a3b8;
}

/* 代码块语法高亮占位样式 */
:deep(.hljs) {
  display: block;
  overflow-x: auto;
  padding: 0.5em;
  border-radius: 4px;
}

/* 表格样式（如果未来需要扩展） */
:deep(.ProseMirror table) {
  border-collapse: collapse;
  margin: 1rem 0;
  width: 100%;
}

:deep(.ProseMirror td),
:deep(.ProseMirror th) {
  border: 1px solid #e2e8f0;
  padding: 0.5rem;
  text-align: left;
}

:deep(.ProseMirror th) {
  background: #f8fafc;
  font-weight: bold;
}

/* 加载状态 */
.saving-indicator {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.saving-indicator::after {
  content: '';
  width: 12px;
  height: 12px;
  border: 2px solid transparent;
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* 错误状态 */
.error-message {
  color: #ef4444;
  font-size: 14px;
  margin-top: 8px;
}

/* 成功状态 */
.success-message {
  color: #10b981;
  font-size: 14px;
  margin-top: 8px;
}

/* 文件上传进度 */
.upload-progress {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #64748b;
}

.progress-bar {
  flex: 1;
  height: 4px;
  background: #e2e8f0;
  border-radius: 2px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #3b82f6;
  transition: width 0.3s ease;
}

/* 暗色模式支持 */
@media (prefers-color-scheme: dark) {
  .resource-editor {
    background: #1f2937;
    border-color: #374151;
    color: #f8fafc;
  }

  .action-bar {
    background: #374151;
    border-color: #4b5563;
  }

  .toolbar {
    background: #374151;
    border-color: #4b5563;
  }

  .toolbar-btn {
    background: #4b5563;
    border-color: #6b7280;
    color: #f8fafc;
  }

  .toolbar-btn:hover {
    background: #6b7280;
  }

  .toolbar-btn.is-active {
    background: #3b82f6;
  }

  :deep(.ProseMirror) {
    background: #1f2937;
    color: #f8fafc;
  }

  :deep(.ProseMirror pre) {
    background: #111827;
  }

  :deep(.ProseMirror code) {
    background: #374151;
    color: #f8fafc;
  }
}

/* 打印样式 */
@media print {
  .action-bar,
  .toolbar {
    display: none !important;
  }

  .resource-editor {
    border: none;
    background: none;
  }

  :deep(.ProseMirror) {
    min-height: auto;
  }
}
/* 字数统计样式 */
.word-count {
  padding: 0 12px;
  color: #64748b;
  font-size: 14px;
  display: flex;
  align-items: center;
  border-left: 1px solid #e2e8f0;
  margin-left: 8px;
}

/* 表情符号对话框 */
.emoji-dialog {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 300px;
}

.emoji-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 8px;
  margin: 16px 0;
}

.emoji-btn {
  font-size: 24px;
  padding: 8px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
}

.emoji-btn:hover {
  background: #f1f5f9;
  transform: scale(1.1);
}

/* 公式对话框 */
.formula-dialog {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
}

.formula-input {
  width: calc(100% - 24px);
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  margin: 16px 0;
  font-size: 14px;
}

.formula-preview {
  padding: 12px;
  background: #f8fafc;
  border-radius: 6px;
  margin: 8px 0;
  font-style: italic;
}

/* 预览模式样式 */
.preview-mode {
  background: #f8fafc;
  border: 2px solid #3b82f6;
}

.preview-mode .toolbar {
  opacity: 0.6;
}

/* 链接按钮激活状态 */
.toolbar-btn.is-active.link-active {
  background: #ef4444;
  color: white;
}

/* 数学公式样式 */
:deep(.math-formula) {
  font-style: italic;
  background: #f8fafc;
  padding: 2px 4px;
  border-radius: 4px;
  border: 1px solid #e2e8f0;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .word-count {
    display: none;
  }

  .emoji-dialog,
  .formula-dialog {
    width: 90%;
    max-width: 300px;
  }

  .emoji-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
/* KaTeX 公式样式 */
.katex-formula {
  display: inline-block;
  margin: 0 2px;
  vertical-align: middle;
}

/* 公式对话框样式 */
.formula-input-group {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 16px 0;
}

.formula-input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 14px;
  font-family: 'Monaco', 'Menlo', monospace;
}

.formula-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
}

.clear-btn {
  padding: 6px;
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}

.clear-btn:hover {
  background: #e2e8f0;
}

/* KaTeX 预览样式 */
.katex-preview {
  padding: 12px;
  background: #f8fafc;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
  min-height: 40px;
  overflow-x: auto;
}

.katex-preview.display {
  text-align: center;
  min-height: 60px;
}

/* 公式示例网格 */
.example-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
  margin: 8px 0;
}

.example-btn {
  padding: 8px;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  cursor: pointer;
  text-align: center;
  transition: all 0.2s;
}

.example-btn:hover {
  background: #f8fafc;
  border-color: #3b82f6;
  transform: translateY(-1px);
}

.example-preview {
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 4px;
}

.example-name {
  font-size: 11px;
  color: #64748b;
  display: block;
}

/* 公式操作按钮 */
.formula-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 16px 0;
  gap: 8px;
}

.insert-buttons {
  display: flex;
  gap: 8px;
}

/* 公式帮助 */
.formula-help {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #e2e8f0;
}

details {
  cursor: pointer;
}

summary {
  font-size: 12px;
  color: #64748b;
  font-weight: 500;
}

.help-content {
  margin-top: 8px;
  padding: 8px;
  background: #f8fafc;
  border-radius: 4px;
  font-size: 11px;
  font-family: 'Monaco', 'Menlo', monospace;
}

.help-content p {
  margin: 4px 0;
}

.help-content code {
  background: #e2e8f0;
  padding: 2px 4px;
  border-radius: 2px;
  color: #374151;
}

/* 公式错误样式 */
.formula-error {
  color: #ef4444;
  background: #fef2f2;
  padding: 4px 8px;
  border-radius: 4px;
  border: 1px solid #fecaca;
  font-size: 12px;
}

/* 编辑器中的公式样式 */
:deep(.katex) {
  font-size: 1.05em !important;
}

:deep(.katex-display) {
  margin: 1rem 0 !important;
  overflow-x: auto;
  overflow-y: hidden;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .example-grid {
    grid-template-columns: 1fr;
  }

  .formula-actions {
    flex-direction: column;
    align-items: stretch;
  }

  .insert-buttons {
    flex-direction: column;
  }

  .formula-dialog {
    width: 95%;
    margin: 0 10px;
  }
}

/* 暗色模式支持 */
@media (prefers-color-scheme: dark) {
  .katex-preview {
    background: #374151;
    border-color: #4b5563;
  }

  .example-btn {
    background: #374151;
    border-color: #4b5563;
    color: #f8fafc;
  }

  .example-btn:hover {
    background: #4b5563;
    border-color: #3b82f6;
  }

  .help-content {
    background: #374151;
    color: #f8fafc;
  }

  .help-content code {
    background: #4b5563;
    color: #f8fafc;
  }

  .formula-error {
    background: #7f1d1d;
    border-color: #ef4444;
    color: #fef2f2;
  }
}
</style>
