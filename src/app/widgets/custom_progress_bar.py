from textual.widgets import ProgressBar


class CustomProgressBar(ProgressBar):
    DEFAULT_CSS = """
        CustomProgressBar {
            margin-left: 1;
            margin-right: 1;
            width: 100%;
        }
        
        CustomProgressBar Bar {
            width: 1fr;
        }
    """
    def __init__(self, total, show_eta=False):
        super().__init__()

        self.total = total
        self.show_eta = show_eta
