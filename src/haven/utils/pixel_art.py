"""Convert pixel art images to colored terminal blocks."""

from pathlib import Path
from PIL import Image


def image_to_blocks(
    image_path: str | Path,
    width: int | None = None,
    use_half_blocks: bool = True,
) -> str:
    """
    Convert an image to colored block characters.

    Args:
        image_path: Path to the image file
        width: Target width in characters (None = use image width)
        use_half_blocks: If True, use ▀/▄ for 2 pixels per row (half height)

    Returns:
        String with Rich markup for colored blocks
    """
    img = Image.open(image_path).convert("RGBA")

    if width and width != img.width:
        ratio = width / img.width
        new_height = int(img.height * ratio)
        img = img.resize((width, new_height), Image.NEAREST)

    pixels = img.load()
    lines = []

    if use_half_blocks:
        # Process 2 rows at a time, using ▀ with fg=top pixel, bg=bottom pixel
        for y in range(0, img.height - 1, 2):
            line = ""
            for x in range(img.width):
                top = pixels[x, y]
                bottom = pixels[x, y + 1]

                # Skip fully transparent pixels
                if top[3] < 128 and bottom[3] < 128:
                    line += " "
                elif top[3] < 128:
                    # Only bottom pixel visible
                    line += f"[rgb({bottom[0]},{bottom[1]},{bottom[2]})]▄[/]"
                elif bottom[3] < 128:
                    # Only top pixel visible
                    line += f"[rgb({top[0]},{top[1]},{top[2]})]▀[/]"
                else:
                    # Both pixels visible
                    line += f"[rgb({top[0]},{top[1]},{top[2]}) on rgb({bottom[0]},{bottom[1]},{bottom[2]})]▀[/]"
            lines.append(line)

        # Handle odd height (last row)
        if img.height % 2:
            line = ""
            y = img.height - 1
            for x in range(img.width):
                px = pixels[x, y]
                if px[3] < 128:
                    line += " "
                else:
                    line += f"[rgb({px[0]},{px[1]},{px[2]})]▀[/]"
            lines.append(line)
    else:
        # Full blocks - one character per pixel
        for y in range(img.height):
            line = ""
            for x in range(img.width):
                px = pixels[x, y]
                if px[3] < 128:  # transparent
                    line += " "
                else:
                    line += f"[rgb({px[0]},{px[1]},{px[2]})]█[/]"
            lines.append(line)

    return "\n".join(lines)


def image_to_blocks_ansi(
    image_path: str | Path,
    width: int | None = None,
) -> str:
    """
    Convert image to blocks using ANSI escape codes directly.
    Useful if Rich markup isn't available.
    """
    img = Image.open(image_path).convert("RGBA")

    if width and width != img.width:
        ratio = width / img.width
        new_height = int(img.height * ratio)
        img = img.resize((width, new_height), Image.NEAREST)

    pixels = img.load()
    lines = []

    for y in range(0, img.height - 1, 2):
        line = ""
        for x in range(img.width):
            top = pixels[x, y]
            bottom = pixels[x, y + 1]

            if top[3] < 128 and bottom[3] < 128:
                line += " "
            elif top[3] < 128:
                line += f"\033[38;2;{bottom[0]};{bottom[1]};{bottom[2]}m▄\033[0m"
            elif bottom[3] < 128:
                line += f"\033[38;2;{top[0]};{top[1]};{top[2]}m▀\033[0m"
            else:
                line += f"\033[38;2;{top[0]};{top[1]};{top[2]};48;2;{bottom[0]};{bottom[1]};{bottom[2]}m▀\033[0m"
        lines.append(line)

    return "\n".join(lines)
