// .eslintrc.js
module.exports = {
  root: true,
  env: {
    browser: true,
    es2021: true,
    node: true
  },
  extends: [
    'eslint:recommended',
    'plugin:vue/vue3-recommended', // Vue3 官方推荐规则
    'plugin:@typescript-eslint/recommended' // TypeScript 推荐规则
  ],
  parser: 'vue-eslint-parser', // 解析 Vue 文件
  parserOptions: {
    parser: '@typescript-eslint/parser', // 解析 TypeScript
    ecmaVersion: 'latest',
    sourceType: 'module',
    project: './tsconfig.json', // 关联 TypeScript 配置
    extraFileExtensions: ['.vue']
  },
  plugins: ['@typescript-eslint', 'prettier', 'import'],
  rules: {
    // TypeScript 规范
    '@typescript-eslint/no-explicit-any': 'warn', // 禁止使用 any（警告级别）
    '@typescript-eslint/no-unused-vars': 'error', // 禁止未使用的变量
    '@typescript-eslint/ban-ts-comment': 'off', // 允许使用 @ts-ignore
    '@typescript-eslint/naming-convention': [
      // 命名约定
      'error',
      {
        selector: 'interface',
        format: ['PascalCase'],
        prefix: ['I'] // 强制接口以 I 开头，如 IUser
      },
      {
        selector: 'typeAlias',
        format: ['PascalCase'],
        prefix: ['T'] // 类型别名以 T 开头，如 TResponse
      },
      // {
      //   selector: 'default', // 默认规则
      //   format: ['camelCase', 'UPPER_CASE'], // 允许 camelCase 和 UPPER_CASE
      //   leadingUnderscore: 'allow' // 可选：允许前导下划线
      // },
      {
        selector: 'variable',
        modifiers: ['destructured'], // 针对解构变量
        format: null // 完全跳过格式校验
      },
      {
        selector: 'property', // 对象属性
        format: ['camelCase', 'snake_case'], // 允许 camelCase 和 snake_case
        leadingUnderscore: 'allow' // 允许前导下划线
      }
    ],
    // Vue3 规范
    'vue/html-self-closing': [
      // 自动闭合标签
      'error',
      {
        html: { void: 'always', normal: 'always' }
      }
    ],
    'vue/attributes-order': 'error', // 属性顺序规范
    'vue/no-v-html': 'warn', // 避免使用 v-html
    // 通用 JavaScript 规范
    'no-console': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    'max-depth': ['error', 4], // 最大嵌套深度 4 层
    complexity: ['error', { max: 20 }], // 圈复杂度不超过
    'no-empty-function': 'error', // 禁止空函数
    'no-useless-escape': 'off', // 允许必要的转义字符
    'prettier/prettier': ['error', { endOfLine: 'auto' }],
    'vue/max-attributes-per-line': 'off',
    'vue/singleline-html-element-content-newline': 'off',
    // 强制方法名使用小驼峰（camelcase）
    camelcase: [
      'error',
      {
        allow: ['^UNSAFE_'], // 允许以 UNSAFE_ 开头的特殊方法（如 React 生命周期）
        ignoreDestructuring: true, // 忽略解构变量
        properties: 'never' // 不检查对象属性名
      }
    ],
    // 强制 Vue 文件名使用大驼峰（PascalCase）
    'vue/component-name-in-template-casing': [
      'error',
      'PascalCase',
      {
        registeredComponentsOnly: false, // 包括所有组件（包括未注册的）
        ignores: ['/^el-/', '/^router-*/']
      }
    ],

    // 关闭组件名必须多单词的限制（避免与文件名大驼峰冲突）
    'vue/multi-word-component-names': 'off', //
    'import/order': [
      'error',
      {
        groups: ['builtin', 'external', 'internal', 'parent', 'sibling', 'index'],
        pathGroups: [
          {
            pattern: '@/**', // 匹配别名路径
            group: 'internal', // 归类为内部模块
            position: 'before' // 在 internal 组内优先排序
          },
          {
            pattern: '*.css', // 样式文件
            group: 'index', // 置于最后
            patternOptions: { matchBase: true }
          }
        ],
        alphabetize: { order: 'asc' } // 组内按字母升序
      }
    ]
  },
  globals: {
    defineProps: 'readonly', // Vue3 宏定义
    defineEmits: 'readonly',
    defineExpose: 'readonly',
    withDefaults: 'readonly'
  },
  ignorePatterns: [
    // 忽略文件/目录
    'dist',
    'node_modules',
    '**/*.js',
    '!.prettierrc.js' // 不忽略配置文件
  ]
};
