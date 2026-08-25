from textual.widgets import Label


class CustomLabel(Label):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)

        self.text = str(text)

    def compose(self):
        yield Label(self.text)
