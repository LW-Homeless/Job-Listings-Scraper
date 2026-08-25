from textual.containers import ScrollableContainer


class CustomProcessLog(ScrollableContainer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_widget(self, widget):
        self.mount(widget)
        self.scroll_end()

    def remove_widget(self):
        self.remove_children()
