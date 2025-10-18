# instaui-tdesign

<div align="center">

English|[简体中文](./README.zh-CN.md)

</div>
 
📖 Introduction
instaui-tdesign is a UI component library for InstaUI, built on top of TDesign.

## 📦 Installation
```
pip install instaui-tdesign -U
```

```
uv add instaui-tdesign
```


## 🖥️ Quick Start


```python
from instaui import ui
from instaui_tdesign import td

td.use(locale="en_US")

@ui.page('/')
def home():
    info = ui.state(
        {
            "name": "",
            "age": 0,
        }
    )

    @ui.computed(inputs=[info])
    def disabled_submit(info: dict) -> bool:
        return info["name"] == "" or info["age"] == 0

    @ui.event(inputs=[info])
    def handle_submit(info: dict):
        # Operations such as printing, writing to a database, etc.
        print(info)

    # ui
    with ui.container(size="1"), ui.column():
        ui.text(info)

        td.input(info["name"], label="NAME")
        td.input_number(info["age"], label="AGE", theme="row", min=0, max=100)
        td.button("submit", disabled=disabled_submit, on_click=handle_submit)

ui.server(debug=True).run()
```
