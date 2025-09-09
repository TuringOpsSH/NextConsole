module.exports = {
  // 每行最大字符数（超过自动换行）
  printWidth: 120,
  // 缩进空格数
  tabWidth: 2,
  // 使用空格代替缩进符
  useTabs: false,
  // 语句末尾是否添加分号
  semi: true,
  // 使用单引号代替双引号
  singleQuote: true,
  // 对象属性引号规则（仅在必要时添加引号）
  quoteProps: 'as-needed',
  // JSX 中使用双引号
  jsxSingleQuote: false,
  // 多行数组/对象/参数列表末尾添加逗号
  trailingComma: 'none',
  // 对象/数组括号与内容之间添加空格
  bracketSpacing: true,
  // 将多行 HTML/JSX 元素的闭合标签放在最后一行的末尾
  bracketSameLine: false,
  // 箭头函数参数括号规则（单个参数时省略括号）
  arrowParens: 'avoid',
  // 换行符风格（统一为 LF）
  endOfLine: 'lf',
  // 自动格式化内嵌代码（如 Markdown 中的代码块）
  embeddedLanguageFormatting: 'auto',
  endOfLine: 'auto', // 自动识别并保留现有换行符
  htmlWhitespaceSensitivity: 'css', // 避免模板空格干扰
  vueIndentScriptAndStyle: false // 缩进 <script> 和 <style>
};
