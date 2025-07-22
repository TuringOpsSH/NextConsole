import {ResourceItem} from "@/types/resource_type";

export function check_resource_rag_support(resource:ResourceItem){
    // 检查资源是否支持RAG
    // 格式预检查
    let all_support_formats = [
        // 文档
        "doc", "docx", "xls", "xlsx", "ppt", "pptx", "pdf", "txt",
        // 代码
        'css', 'js', 'json', 'xml', 'java', 'cpp', 'c', 'py', 'php', 'go', 'h', 'hpp',
        'rb', 'cs', 'sh', 'bat', 'swift', 'kt', 'ts', 'pl', 'lua', 'r', 'scala', 'sql', 'vb',
        'vbs', 'yaml', 'yml', 'md', 'ps1', 'ini', 'conf', 'properties', 'cmd', 'vue', 'jsx',
        'perl', 'db2', 'rs', 'mm', 'm', 'plsql', 'hs', 'hsc', 'Dockerfile', 'dart', 'pm', 'bash', 'svelte',
        // 网页
        "htm", "html",
    ]
    return true
}
