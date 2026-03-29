from pathlib import Path

from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Horizontal, Vertical, Container
from textual.widgets import Static, Input, TabbedContent, TabPane, RichLog

from haven.utils.pixel_art import image_to_blocks

# Path to test image (relative to project root)
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
TEST_IMAGE = PROJECT_ROOT / "test.png"


class PortraitBox(Static):
    """Displays character pixel/ASCII art."""
    pass


class StatsPanel(Static):
    """Quick stats display."""
    pass


class DemoScreen(Screen):
    CSS = """
    DemoScreen {
        layout: grid;
        grid-size: 2 2;
        grid-columns: 2fr 1fr;
        grid-rows: 1fr auto;
    }

    #main-panel {
        column-span: 1;
        border: solid green;
        padding: 1;
    }

    #side-panel {
        border: solid blue;
        padding: 1;
    }

    #input-area {
        column-span: 2;
        height: auto;
        border: solid yellow;
        padding: 0 1;
    }

    PortraitBox {
        height: 20;
        width: 40;
        border: dashed white;
        padding: 0 1;
    }

    StatsPanel {
        height: auto;
        padding: 1;
        border: solid gray;
        margin-top: 1;
    }

    #story-log {
        height: 100%;
    }

    TabbedContent {
        height: 100%;
    }

    TabPane {
        padding: 1;
    }

    #command-input {
        margin: 1 0;
    }
    """

    def compose(self) -> ComposeResult:
        # Main content area with tabs
        with Container(id="main-panel"):
            with TabbedContent():
                with TabPane("Story", id="tab-story"):
                    yield RichLog(id="story-log", highlight=True, markup=True)
                with TabPane("Inventory", id="tab-inventory"):
                    yield Static("🎒 Inventory\n\n• Rusty sword\n• Health potion x2\n• Old map\n• 50 gold coins")
                with TabPane("Journal", id="tab-journal"):
                    yield Static("📜 Journal\n\n[Day 1]\nArrived at the Old Farm.\nThe farmer speaks of a curse...")

        # Side panel with portrait and stats
        with Vertical(id="side-panel"):
            # Load pixel art from image
            if TEST_IMAGE.exists():
                pixel_art = image_to_blocks(TEST_IMAGE)
                yield PortraitBox(pixel_art, id="portrait")
            else:
                yield PortraitBox("(no image)", id="portrait")
            yield StatsPanel(
                "❤️  HP: ████████░░ 80/100\n"
                "💰 Gold: 50\n"
                "📍 Old Farm"
            )

        # Command input at bottom
        with Container(id="input-area"):
            yield Static("What do you do?")
            yield Input(placeholder="Enter command...", id="command-input")

    def on_mount(self) -> None:
        """Populate story log with example content."""
        log = self.query_one("#story-log", RichLog)
        log.write("[bold]The Old Farm[/bold]")
        log.write("")
        log.write("You arrive at a weathered farm on the outskirts of town.")
        log.write("The crops are wilted and a strange mist hangs in the air.")
        log.write("")
        log.write("A [bold]farmer[/bold] looks up from his work.")
        log.write("")
        log.write('[italic]"Traveler, these fields weren\'t always like this.[/italic]')
        log.write('[italic]The curse came three moons ago..."[/italic]')
        log.write("")
        log.write("[dim]> look around[/dim]")
        log.write("")
        log.write("You see a [cyan]rusty hoe[/cyan], wilted crops, and a [cyan]locked shed[/cyan].")
        log.write("The farmer watches you with weary eyes.")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle command input."""
        command = event.value
        if command.strip():
            log = self.query_one("#story-log", RichLog)
            log.write("")
            log.write(f"[dim]> {command}[/dim]")
            log.write("")
            log.write(f'[italic]You typed: "{command}"[/italic]')
            event.input.value = ""
