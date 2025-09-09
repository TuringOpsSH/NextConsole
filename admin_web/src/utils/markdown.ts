import hljs from 'highlight.js';
import MarkdownIt from 'markdown-it';

export const md_question = new MarkdownIt({
  // html: true,
  linkify: true,
  typographer: true,
  breaks: true,
  highlight: function (str, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return (
          '<pre class="hljs" style="white-space: pre-wrap; overflow: auto ; position: relative">' +
          '<img src="/images/copy.svg" alt="复制" ' +
          'class="answer-code-copy" style="position: absolute;top: 0;right: 0;width: 20px;height: 20px;"' +
          ' /><code class="hljs-code" style="padding: 10px 0 10px 0">' +
          hljs.highlight(str, { language: lang, ignoreIllegals: true }).value +
          '</code></pre>'
        );
      } catch (__) {}
    }
    return (
      '<pre class="hljs" style="white-space: pre-wrap; overflow: auto ; position: relative">' +
      '<img src="/images/copy.svg" alt="复制" ' +
      'class="answer-code-copy" style="position: absolute;top: 0;right: 0;width: 20px;height: 20px;"' +
      ' />' +
      str +
      ' </pre>'
    );
  }
});

export const md_answer = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
  breaks: true,
  highlight: function (str, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return (
          '<pre class="hljs" style="white-space: pre-wrap; overflow: auto ; position: relative">' +
          '<img src="/images/copy.svg" alt="复制" ' +
          'class="answer-code-copy" style="position: absolute;top: 0;right: 0;width: 20px;height: 20px;"' +
          ' /><code class="hljs-code" >' +
          '<br>' +
          hljs.highlight(str, { language: lang, ignoreIllegals: true }).value +
          '<br>' +
          '</code></pre>'
        );
      } catch (__) {}
    }

    return (
      '<pre class="hljs" style="white-space: pre-wrap; overflow: auto ; position: relative">' +
      '<img src="/images/copy.svg" alt="复制" ' +
      'class="answer-code-copy" style="position: absolute;top: 0;right: 0;width: 20px;height: 20px;"' +
      ' /><code class="hljs-code">' +
      hljs.highlight(str, { language: 'javascript', ignoreIllegals: true }).value +
      '</code></pre>'
    );
  }
});

export function compiledMarkdown(msg_content: string, model: number = 2) {
  if (model === 1) {
    if (msg_content) {
      return md_question.render(msg_content);
    } else {
      return '';
    }
  } else {
    if (msg_content) {
      return md_answer.render(msg_content);
    } else {
      return '';
    }
  }
}
