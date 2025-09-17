from __tests.screen import BaseContext


class ZeroContext(BaseContext):
    def open(self, html_str: str):
        self.page.set_content(html_str)
