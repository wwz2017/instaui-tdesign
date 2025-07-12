import re
from collections import defaultdict


def parse_md_sections(md_text: str) -> dict:
    lines = md_text.strip().splitlines()
    result = defaultdict(lambda: defaultdict(dict))

    current_component = None
    current_section_type = None
    current_table_headers = []
    current_table_rows = []

    def flush_table():
        nonlocal \
            current_component, \
            current_section_type, \
            current_table_headers, \
            current_table_rows
        if not current_component or not current_table_headers:
            return

        table_data = [
            dict(zip(current_table_headers, row)) for row in current_table_rows
        ]
        if current_section_type in ["props", "events", "methods"]:
            result[current_component][current_section_type] = table_data
        else:
            result[current_component].setdefault("extra", {})[current_section_type] = (
                table_data
            )

        # 重置状态
        current_section_type = None
        current_table_headers = []
        current_table_rows = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 检测 section 开头
        # e.g. "### Tabs Props"
        if (
            line.endswith("BaseTableCol")
            or line.endswith("PrimaryTableCol")
            or line.endswith("GuideStep")
        ):
            line = line + " Props"
        m_component = re.match(r"^###\s+([A-Za-z0-9_]+)\s+(Props|Events)\s*$", line)

        if m_component:
            flush_table()
            current_component = m_component.group(1)
            section = m_component.group(2).lower()
            current_section_type = section
            continue

        # 检测实例方法，如 "### TabPanelInstanceFunctions 组件实例方法"
        m_instance_fn = re.match(
            r"^###\s+([A-Za-z0-9_]+)InstanceFunctions\s+组件实例方法$", line
        )
        if m_instance_fn:
            flush_table()
            current_component = m_instance_fn.group(1)
            current_section_type = "methods"
            continue

        # 检测无法归类的 extra 段落，如 "### TableRowState"
        m_extra = re.match(r"^###\s+([A-Za-z0-9_]+)\s*$", line)
        if m_extra:
            flush_table()
            current_component = "Tabs"  # 默认归属当前组件（可调整策略）
            current_section_type = m_extra.group(1)
            continue

        # 表头
        if "|" in line and not current_table_headers:
            current_table_headers = [x.strip() for x in line.strip("|").split("|")]
            # 如果里面有 "说明" ，统一改成 "描述"
            if "说明" in current_table_headers:
                current_table_headers[current_table_headers.index("说明")] = "描述"
            continue

        # 分隔线
        if re.match(r"^\s*\|\s*-+", line):
            continue

        # 表格行
        if current_table_headers and "|" in line:
            row = smart_split_md_row(line.strip("|"))
            if len(row) == len(current_table_headers):
                current_table_rows.append(row)
            else:
                print(f"❌ Invalid table row: {line}")
            continue

    # 最后一张表
    flush_table()

    # 清除不完整组件（没有 props/events/methods）
    filtered_result = {}
    for comp, data in result.items():
        if any(key in data for key in ["props", "events", "methods"]):
            filtered_result[comp] = data

    return filtered_result


def smart_split_md_row(line: str) -> list[str]:
    """
    智能分割 markdown 表格行，忽略反引号中的 |
    """
    parts = []
    current = ""
    in_backtick = False
    i = 0
    while i < len(line):
        char = line[i]
        if char == "`":
            in_backtick = not in_backtick
            current += char
        elif char == "|" and not in_backtick:
            parts.append(current.strip())
            current = ""
        else:
            current += char
        i += 1
    parts.append(current.strip())  # 最后一列
    return parts
