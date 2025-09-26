# instaui-tdesign

<div align="center">

简体中文| [English](./README.md)

</div>
 
## 📖 介绍
instaui-tdesign 是 InstaUI 的一个 UI 组件库，基于 TDesign 进行封装。



## 📦 安装
```
pip install instaui-tdesign -U
```

```
uv add instaui-tdesign
```


## 🖥️ 快速开始


```python
from instaui import ui
import instaui_tdesign as td

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
        # 打印、写入数据库等操作
        print(info)

    # ui
    with ui.container(size="1"), ui.column():
        ui.text(info)

        td.input(info["name"], label="NAME")
        td.input_number(info["age"], label="AGE", theme="row", min=0, max=100)
        td.button("submit", disabled=disabled_submit, on_click=handle_submit)

ui.server(debug=True).run()
```
