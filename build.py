#!/usr/bin/env python3
"""Build shipped persona files from a role harness + a character overlay.

Each persona is authored as two sources, so the role mechanism lives in
exactly one place and the backstory simply *expands* it:

  - roles/<codename>.md           the bland, reusable "harness" (the role)
  - personas/<name>/character.md   the character that expands that role

The character file contains one or more markers of the form:

    <!-- ROLE:<codename> -->

Each marker is replaced by the *injectable* block of roles/<codename>.md —
the text fenced between <!-- INJECT:start --> and <!-- INJECT:end -->. The
material outside that fence (the role's standalone intro and invocation
notes) is for using the harness on its own and is not spliced in.

Output: personas/<name>/<name>.md  (generated — do not edit by hand)
"""

import re
from pathlib import Path

ROOT = Path(__file__).parent
ROLES = ROOT / "roles"
PERSONAS = ROOT / "personas"

ROLE_MARKER = re.compile(r"<!--\s*ROLE:([a-z0-9-]+)\s*-->")
INJECT_BLOCK = re.compile(
    r"<!--\s*INJECT:start\s*-->(.*?)<!--\s*INJECT:end\s*-->", re.DOTALL
)


def role_inject(codename: str) -> str:
    """Return the fenced injectable block from roles/<codename>.md."""
    role_file = ROLES / f"{codename}.md"
    if not role_file.exists():
        raise FileNotFoundError(f"role '{codename}' not found at {role_file}")
    match = INJECT_BLOCK.search(role_file.read_text())
    if not match:
        raise ValueError(
            f"{role_file} has no <!-- INJECT:start --> / <!-- INJECT:end --> fence"
        )
    return match.group(1).strip()


def build_persona(char_path: Path) -> Path:
    """Splice a character overlay with its role(s) and write <name>.md."""
    name = char_path.parent.name
    body = ROLE_MARKER.sub(lambda m: role_inject(m.group(1)), char_path.read_text())
    banner = (
        "<!-- GENERATED FILE — do not edit directly.\n"
        f"     Source: personas/{name}/character.md + roles/*.md\n"
        "     Regenerate with: python build.py -->\n\n"
    )
    out = char_path.parent / f"{name}.md"
    out.write_text(banner + body)
    return out


def main() -> None:
    built = [build_persona(p) for p in sorted(PERSONAS.glob("*/character.md"))]
    if not built:
        print("No character.md files found — nothing to build.")
        return
    for out in built:
        print(f"built {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
