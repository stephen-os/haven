from textual.screen import Screen
from textual.widgets import Static, Button

class MenuScreen(Screen):
    def compose(self):
        yield Static("Welcome to Haven")
        yield Button("New Game", id="new")
        yield Button("Load", id="load")