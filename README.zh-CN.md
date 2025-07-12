# instaui-tdesign

<div align="center">

简体中文| [English](./README.en.md)

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

td.use(locale='zh-CN')

@ui.page('/')
def home():
    td.button('按钮')

ui.server(debug=True).run()
```
