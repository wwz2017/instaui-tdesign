import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent
PARSED_DIR = BASE_DIR / "parsed"
OUTPUT_DIR = BASE_DIR / "component_types"
OUTPUT_DIR.mkdir(exist_ok=True)

JS_TYPE_MAP = {
    "boolean": "bool",
    "string": "str",
    "number": "float",
    "object": "typing.Dict",
    "array": "typing.List",
    "function": "str",  # default fallback
    "slot": None,
    "vnode": None,
}


def normalize_prop_name(name: str) -> str:
    name = re.sub(r"[（\(]暂未实现[）\)]$", "", name.strip())
    name = name.replace("-", "_")
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    return name.lower()


def extract_literal(description: str) -> str | None:
    match = re.search(r"[可选项|可选值][:：]?\s*([a-zA-Z0-9/_\- ]+)", description)
    if match:
        items = [x.strip() for x in match.group(1).split("/") if x.strip()]
        if items:
            all_literals = ", ".join(f'"{item}"' for item in items)
            return f"typing.Literal[{all_literals}]"
    return None


def js_type_to_py_type(name: str, js_type: str, description: str) -> str | None:
    # slot 类型忽略
    types = [t.strip().lower() for t in js_type.split("/")]

    # Event 类型（函数 + on_ 前缀）
    if "function" in js_type.lower() and name.lower().startswith("on_"):
        return "EventMixin"

    # Literal（string + 可选项）
    if "string" in js_type.lower():
        lit = extract_literal(description)
        if lit:
            return f"TMaybeRef[{lit}]"

    # 转换为 python 类型
    py_types = set()
    for t in types:
        for key, py in JS_TYPE_MAP.items():
            if key in t:
                if py:
                    py_types.add(f"TMaybeRef[{py}]")
                break
        else:
            py_types.add("TMaybeRef[typing.Any]")

    # Union or single type
    if not py_types:
        return None
    if len(py_types) == 1:
        return next(iter(py_types))
    return f"TMaybeRef[typing.Union[{', '.join(sorted(py_types))}]]"


def generate_class(component_name: str, props: list[dict]) -> str:
    lines = [f"class T{component_name}Props(TypedDict, total=False):"]
    has_valid = False

    for prop in props:
        name = prop.get("名称", "").strip()
        if name == "--" or name.endswith("（暂未实现）"):
            continue
        js_type = prop.get("类型", "").strip()
        desc = prop.get("描述", "").strip()
        py_name = normalize_prop_name(name)
        py_type = js_type_to_py_type(py_name, js_type, desc)

        if py_type:
            lines.append(f"    {py_name}: {py_type}")
            has_valid = True

    if not has_valid:
        lines.append("    pass")

    return "\n".join(lines)


def process_json(json_path: Path, output_path: Path):
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    classes = []
    for comp_name, section in data.items():
        props = section.get("props", [])
        if props:
            code = generate_class(comp_name, props)
            classes.append(code)

    if not classes:
        print(f"⚠️ No props found in {json_path.name}")
        return

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("import typing\n")
        f.write("from typing_extensions import TypedDict\n")
        f.write("from instaui.event.event_mixin import EventMixin\n")
        f.write("if typing.TYPE_CHECKING:\n")
        f.write("    from instaui.vars.types import TMaybeRef\n\n")
        f.write("\n\n".join(classes))
    print(f"✅ Generated: {output_path.name}")


def main():
    for component_dir in PARSED_DIR.iterdir():
        if not component_dir.is_dir():
            continue
        json_path = component_dir / f"{component_dir.name}.json"
        if not json_path.exists():
            print(f"❌ Missing: {json_path}")
            continue
        output_path = OUTPUT_DIR / f"{component_dir.name}.py"
        process_json(json_path, output_path)


if __name__ == "__main__":
    main()
