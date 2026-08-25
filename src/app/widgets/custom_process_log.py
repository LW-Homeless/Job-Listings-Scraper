from textual.widgets import Static

from src.app.widgets.custom_label import CustomLabel


class Custom(Static):
    def __init__(self,title, **kwargs):
        super().__init__(**kwargs)

        self.__title = title

    def compose(self):
        yield CustomLabel(text=self.__title)
        yield Static("", id="")

    def show_widget(self, widgets):
        self.mount(widgets)
