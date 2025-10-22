from instaui import ui
from instaui_tdesign import td


def lang_select():
    data = ui.data(
        [{"label": "english", "value": "en_US"}, {"label": "中文", "value": "zh_CN"}]
    )

    current = ui.use_language()
    options = ui.js_computed(inputs=[data, current], code=r"""(data,current)=> data""")

    mounted = ui.js_event(
        outputs=[current],
        code=r"""()=>{
const lang = navigator.language || navigator.userLanguage;
const isZh = lang.toLowerCase().startsWith('zh');
return isZh? 'zh_CN' : 'en_US';
}""",
    )

    return td.select(
        options=options,
        value=current,
        borderless=True,
        auto_width=True,
    ).on_mounted(mounted)
