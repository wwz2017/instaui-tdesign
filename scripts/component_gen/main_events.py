import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
PARSED_DIR = BASE_DIR / "parsed"
OUTPUT_DIR = BASE_DIR / "component_events"
OUTPUT_DIR.mkdir(exist_ok=True)

EVENT_METHOD_TEMPLATE = """    def on_{event_name}(
        self,
        handler: EventMixin,
        *,
        extends: typing.Optional[typing.List] = None,
    ):
        self.on(
            "{event_name_str}",
            handler,
            extends=extends,
        )
        return self
"""

CLASS_TEMPLATE = """import typing
from instaui.event.event_mixin import EventMixin
from instaui.element.element import Element


class {class_name}(Element):
    def __init__(self):
        super().__init__("t-{tag_name}")

{methods}
"""


def to_snake_case(name: str) -> str:
    return name.replace("-", "_").lower()


def process_json(json_path: Path, output_path: Path):
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    classes = []
    for component_name, sections in data.items():
        events = sections.get("events", [])
        valid_events = [e for e in events if e.get("名称") and e["名称"] != "--"]
        if not valid_events:
            continue

        methods = "\n".join(
            EVENT_METHOD_TEMPLATE.format(
                event_name=to_snake_case(event["名称"]), event_name_str=event["名称"]
            )
            for event in valid_events
        )

        class_code = CLASS_TEMPLATE.format(
            class_name=component_name, tag_name=component_name.lower(), methods=methods
        )

        classes.append((component_name, class_code))

    for name, code in classes:
        out_path = output_path / f"{name.lower()}.py"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(code)
        print(f"✅ Generated: {out_path.name}")


def main():
    for comp_dir in PARSED_DIR.iterdir():
        if not comp_dir.is_dir():
            continue

        json_path = comp_dir / f"{comp_dir.name}.json"
        if not json_path.exists():
            print(f"❌ Skipped: {json_path.name} not found")
            continue

        process_json(json_path, OUTPUT_DIR)


if __name__ == "__main__":
    main()
