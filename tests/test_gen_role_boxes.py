"""Tests for gen_role_boxes.py: the colored role chips."""

import pytest
from PIL import Image

import gen_role_boxes as grb


def test_make_chip_size_color_and_transparent_corner(tmp_path):
    out = tmp_path / "chip.png"

    grb.make_chip("#31847f", out)

    img = Image.open(out).convert("RGBA")
    assert img.size == (grb.SIZE, grb.SIZE)
    assert img.getpixel((grb.SIZE // 2, grb.SIZE // 2)) == (0x31, 0x84, 0x7F, 255)
    assert img.getpixel((0, 0))[3] == 0  # rounded corner is transparent


def test_colors_are_valid_hex():
    for codename, color in grb.COLORS.items():
        assert len(color) == 7 and color.startswith("#"), codename
        int(color[1:], 16)


def test_every_role_has_a_color():
    roles = {p.stem for p in grb.ROLES.glob("*.md")}
    assert roles == set(grb.COLORS)


@pytest.mark.parametrize("codename", sorted(grb.COLORS))
def test_committed_chip_matches_configured_color(codename):
    chip = grb.ROLES / f"{codename}-box.png"
    assert chip.exists(), f"missing {chip.name}; run gen_role_boxes.py"
    img = Image.open(chip).convert("RGBA")
    expected = tuple(int(grb.COLORS[codename][i : i + 2], 16) for i in (1, 3, 5))
    assert img.getpixel((grb.SIZE // 2, grb.SIZE // 2)) == (*expected, 255)


def test_main_writes_one_chip_per_role(tmp_path, monkeypatch, capsys):
    (tmp_path / "roles").mkdir()
    monkeypatch.setattr(grb, "ROLES", tmp_path / "roles")

    grb.main()

    written = sorted(p.name for p in (tmp_path / "roles").glob("*-box.png"))
    assert written == sorted(f"{c}-box.png" for c in grb.COLORS)
    assert "wrote" in capsys.readouterr().out
