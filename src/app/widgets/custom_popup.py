from textual.screen import ModalScreen
from textual.containers import Vertical
from textual.widgets import Label, Static


class CustomPopup(ModalScreen[bool]):

    DEFAULT_CSS = """
    CustomPopup {
        align: center middle;
    }

    #dialog {
        width: 50;
        height: auto;
        border: round $accent;
        background: $surface;
        padding: 1 2;
    }

    #mensaje {
        height: auto;
        padding-bottom: 1;
        text-align: center;
    }
    """

    def __init__(self, mensaje, **kwargs):
        super().__init__(**kwargs)
        self.__mensaje = mensaje

    def compose(self):
        with Vertical(id="dialog"):
            yield Label(self.__mensaje, id="mensaje")
            yield Static("", id="progress_bar")

    async def show_widget(self, widget):
        placeholder = self.query_one("#progress_bar", Static)
        await placeholder.remove()  # quita el Static vacío
        await self.query_one("#dialog", Vertical).mount(widget)  # monta el widget real dentro del dialog