from textual.app import App

from src.app.screens.main_screen import MainScreen

class MyApp(App):
    CSS_PATH = "styles.tcss"
    ENABLE_COMMAND_PALETTE = False

    def on_mount(self):
        self.push_screen(MainScreen())
