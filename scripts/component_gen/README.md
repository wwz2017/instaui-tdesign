
## 组件生成工具
工具从 TDesign 官网的组件文档中自动生成组件代码，并自动生成组件文档。

### 运行方式
你需要到[TDesign 仓库](https://github.com/Tencent/tdesign-vue-next)，复制其 `packages\components` 到此目录下

此时目录结构如下：

```
- utils.py
- main.py
- components/
  - affix/
    - affix.md
    - affix.en-US.md
  ...
```


执行 `uv run main.py` 即可生成组件代码和文档。