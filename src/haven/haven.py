from textual.app import App

from haven.screens.demo import DemoScreen
from haven.screens.game_screen import GameScreen
from haven.screens.menu_screen import MenuScreen

class Haven(App):

    SCREENS = {
        "menu": MenuScreen,
        "game": GameScreen,
        "demo": DemoScreen,
    }

    def on_mount(self):
        self.push_screen("demo")