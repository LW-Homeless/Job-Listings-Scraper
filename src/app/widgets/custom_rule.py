from textual.widgets import Rule


class CustomRule(Rule):
    def __init__(self, orientation, line_style):
        super().__init__()

        self.orientation = orientation
        self.line_style = line_style

    def add_widget(self, widget):
        self.mount(widget)
