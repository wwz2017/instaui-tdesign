import json
from pathlib import Path
from utils import parse_md_sections

# 根目录
BASE_DIR = Path(__file__).resolve().parent
COMPONENTS_DIR = BASE_DIR / "components"
PARSED_DIR = BASE_DIR / "parsed"
TYPES_DIR = Path(__file__).parent / "component_types"


def parse_and_save(md_path: Path, output_path: Path):
    with open(md_path, encoding="utf-8") as f:
        md_text = f.read()
    parsed = parse_md_sections(md_text)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(parsed, f, ensure_ascii=False, indent=2)


def create_parsed_files():
    PARSED_DIR.mkdir(exist_ok=True)

    for component_dir in COMPONENTS_DIR.iterdir():
        if not component_dir.is_dir():
            continue

        component_name = component_dir.name
        zh_md = component_dir / f"{component_name}.md"
        en_md = component_dir / f"{component_name}.en-US.md"

        output_component_dir = PARSED_DIR / component_name
        output_component_dir.mkdir(parents=True, exist_ok=True)

        if zh_md.exists():
            zh_json = output_component_dir / f"{component_name}.json"
            parse_and_save(zh_md, zh_json)
            print(f"✅ Parsed: {zh_md} -> {zh_json}")
        else:
            print(f"⚠️  Missing zh file: {zh_md}")

        if en_md.exists():
            en_json = output_component_dir / f"{component_name}.en-US.json"
            parse_and_save(en_md, en_json)
            print(f"✅ Parsed: {en_md} -> {en_json}")
        else:
            print(f"⚠️  Missing en file: {en_md}")


if __name__ == "__main__":
    create_parsed_files()
