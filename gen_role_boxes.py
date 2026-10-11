#!/usr/bin/env python3
"""Generate the colored 'chip' icons used in role signatures.

Each role has a codename that maps to a color. This writes a small rounded
square PNG in that exact hex to roles/<codename>-box.png — the role's
equivalent of a persona's face icon. The function emoji that sits beside the
chip lives in the markdown signature, not in the image, so no emoji font is
needed. Re-run only when a color changes.
"""

from pathlib import Path
from PIL import Image, ImageDraw

ROLES = Path(__file__).parent / "roles"

# codename -> hex color
COLORS = {
    "slate": "#64748b",
    "cyan": "#06b6d4",
    "ochre": "#cc7722",
    "sage": "#87a96b",
    "coral": "#ff6f61",
}

SIZE = 72       # source resolution; rendered small (width≈18) in signatures
RADIUS = 16     # corner rounding, in source pixels


def make_chip(hex_color: str, out: Path) -> None:
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([0, 0, SIZE - 1, SIZE - 1], radius=RADIUS, fill=hex_color)
    img.save(out)


def main() -> None:
    for codename, hex_color in COLORS.items():
        out = ROLES / f"{codename}-box.png"
        make_chip(hex_color, out)
        print(f"wrote {out.relative_to(ROLES.parent)}  ({hex_color})")


if __name__ == "__main__":
    main()
