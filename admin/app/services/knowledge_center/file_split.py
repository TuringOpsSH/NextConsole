from app.models.resource_center.resource_model import ResourceObjectMeta
from app.services.configure_center.response_utils import next_console_response
from typing import List, Dict, Union


def length_split(params):
    """
    使用长度分块方法将文档内容进行分块处理
        先按照指定的长度进行分块，然后再进行重叠处理，
        最终生成符合要求的分块内容
    """
    chunk_size = params.get("chunk_size", 2000)
    chunk_overlap = params.get("length_config", {}).get("chunk_overlap", 500)
    content = params.get("content")
    if not content:
        return []
    if chunk_overlap >= chunk_size:
        return next_console_response(error_status=True, error_message="重叠长度不能大于等于分块长度")
    result = []
    total_len = len(content)
    start = 0
    while start < total_len:
        # 计算当前块的结束位置
        end = min(start + chunk_size, total_len)
        WHITESPACE_CHARS = [' ', '\t', '\v', '\f', '\u3000']
        space_cnt = sum(content.count(c, start, end) for c in WHITESPACE_CHARS)
        end += space_cnt  # 增加空格数量，避免切分单词
        # 确保不切分完整的句子（智能边界扩展处理）
        if end < total_len:
            # 查找最近的句子边界
            boundary = min(
                content.find('\n\n', end, total_len),
                content.find('。', end, total_len),
                content.find('！', end, total_len),
                content.find('？', end, total_len),
                content.find('. ', end, total_len),
                content.find('? ', end, total_len),
                content.find('! ', end, total_len)
            )
            if boundary != -1 and boundary > start:
                end = boundary + 1  # 包含标点符号
        chunk_start = start - chunk_overlap if start - chunk_overlap > 0 else 0
        chunk_end = end + chunk_overlap if end + chunk_overlap < total_len else total_len
        result.append({
            "content": content[chunk_start:chunk_end].strip(),
        })

        # 更新下一个起始位置（考虑重叠）
        start = max(end, start + 1)  # 避免无限循环

        # 如果剩余内容不足一个块且不为空
        if start >= total_len:
            break
        if total_len - start < chunk_size and total_len - start > 0:
            result.append({
                "content": content[start:].strip(),
            })
            break
    return result


def symbol_split(params):
    """
    使用指定符号分块方法将文档内容进行分块处理
        通过指定的分隔符将文档内容进行分块处理，
        可以选择保留分隔符或合并分块
        separators
    """
    content = params.get("content")
    chunk_size = params.get("chunk_size", 1500)
    separators = params.get("symbol_config", {}).get("separators", ['---'])
    keep_separator = params.get("symbol_config", {}).get("keep_separator", True)
    merge_chunks = params.get("symbol_config", {}).get("merge_chunks", True)
    if not content:
        return []
    if not separators:
        return next_console_response(error_status=True, error_message="分隔符列表不能为空")
    result = []
    separators = sorted(separators, key=len, reverse=True)
    current_pos = 0
    last_split_pos = 0

    while current_pos < len(content):
        # 查找下一个分隔符出现位置
        next_split = find_next_separator(content, separators, current_pos)

        if next_split == -1:  # 无更多分隔符
            chunk = content[last_split_pos:]
            if chunk.strip():  # 避免添加空块
                result.append(chunk)
            break

        # 计算分隔符长度
        sep_len = len(next_split['separator'])

        # 确定分块内容范围
        chunk_start = last_split_pos
        chunk_end = next_split['position'] + (sep_len if keep_separator else 0)

        chunk = content[chunk_start:chunk_end].strip()
        if chunk:  # 忽略空块
            result.append(chunk)

        # 更新位置
        last_split_pos = next_split['position'] + sep_len
        current_pos = last_split_pos

        # 合并过小分块（当启用merge_chunks时）
    if merge_chunks and len(result) > 1:
        result = merge_small_chunks(result, chunk_size)
    result = [{"content": result.strip()} for result in result if result.strip()]
    return result


def find_next_separator(text, separators, start_pos):
    """查找下一个出现的分隔符及其位置"""
    min_pos = float('inf')
    found_sep = None

    for sep in separators:
        pos = text.find(sep, start_pos)
        if pos != -1 and pos < min_pos:
            min_pos = pos
            found_sep = sep

    return {"position": min_pos, "separator": found_sep} if found_sep else -1


def merge_small_chunks(chunks, target_size):
    """合并小于目标大小的连续分块"""
    merged = []
    current_chunk = ""

    for chunk in chunks:
        if len(current_chunk) + len(chunk) <= target_size:
            current_chunk += "\n" + chunk if current_chunk else chunk
        else:
            if current_chunk:
                merged.append(current_chunk)
            current_chunk = chunk

    if current_chunk:
        merged.append(current_chunk)

    return merged


def layout_split(params):
    """
    使用布局分块方法将markdown内容进行分块处理
        将markdown进行AST解析
        按照每个顶级块进行分块处理，
        可以选择合并分块或保留原始布局
    """
    content = params.get("content")
    chunk_size = params.get("chunk_size", 1500)
    merge_chunks = params.get("layout_config", {}).get("merge_chunks", True)
    preserve_structures = params.get("layout_config", {}).get("preserve_structures", ["code", "table"])
    if not content:
        return []
    from markdown_it import MarkdownIt
    from mdformat.renderer import MDRenderer
    md = MarkdownIt("zero")
    env = {}
    tokens = md.parse(content, env)

    chunks = []
    current_chunk = []
    current_size = 0

    def render_token(token) -> str:
        """渲染单个token为Markdown文本"""
        return MDRenderer().render([token], md.options, env)

    for token in tokens:
        if token.type == "inline":
            continue  # 跳过inline节点，由父节点处理

        token_content = render_token(token)
        token_len = len(token_content)

        # 强制保留的结构
        if token.type in preserve_structures:
            if current_chunk:
                chunks.append("".join(current_chunk))
                current_chunk = []
                current_size = 0
            chunks.append(token_content)
            continue

        # 需要分块的边界类型
        is_boundary = token.type in ("heading_open", "hr", "bullet_list_open", "ordered_list_open")

        if is_boundary or (merge_chunks and current_size + token_len > chunk_size):
            if current_chunk:
                chunks.append("".join(current_chunk))
            current_chunk = [token_content]
            current_size = token_len
        else:
            current_chunk.append(token_content)
            current_size += token_len

    if current_chunk:
        chunks.append("".join(current_chunk))

    # 后处理：合并过小分块
    if merge_chunks and len(chunks) > 1:
        chunks = _merge_small_chunks(chunks, chunk_size)
    # 转换为最终结果格式
    result = [{"content": chunk.strip()} for chunk in chunks if chunk.strip()]
    return result


def _merge_small_chunks(chunks: List[str], target_size: int) -> List[str]:
    """合并连续的小分块"""
    merged = []
    buffer = ""

    for chunk in chunks:
        if len(buffer) + len(chunk) <= target_size:
            buffer += "\n\n" + chunk if buffer else chunk
        else:
            if buffer:
                merged.append(buffer)
            buffer = chunk
    if buffer:
        merged.append(buffer)

    return merged

