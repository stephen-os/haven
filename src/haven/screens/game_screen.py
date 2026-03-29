from textual.screen import Screen
from textual.widgets import Static, Button

class GameScreen(Screen):
    def compose(self):
        yield Static("The adventure begins...")