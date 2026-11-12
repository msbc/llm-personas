"""Tests for build.py: splicing role harnesses into persona character files."""

import json
import re
import shutil
from pathlib import Path

import pytest

import build


@pytest.fixture
def fake_roles(tmp_path, monkeypatch):
    """Point build.ROLES at a temporary directory with one sample role."""
    roles = tmp_path / "roles"
    roles.mkdir()
    (roles / "demo.md").write_text(
        "# Demo\n\nStandalone intro.\n\n"
        "<!-- INJECT:start -->\n## Harness\n\nThe injected body.\n"
        "<!-- INJECT:end -->\n\n"
        "## Invocation\n\nStandalone notes.\n"
    )
    monkeypatch.setattr(build, "ROLES", roles)
    return roles


def test_role_inject_returns_only_the_fenced_block(fake_roles):
    assert build.role_inject("demo") == "## Harness\n\nThe injected body."


def test_role_inject_missing_role(fake_roles):
    with pytest.raises(FileNotFoundError, match="role 'nope' not found"):
        build.role_inject("nope")


def test_role_inject_missing_fence(fake_roles):
    (fake_roles / "bare.md").write_text("# No fence here\n")
    with pytest.raises(ValueError, match="INJECT:start"):
        build.role_inject("bare")


def test_build_persona_splices_role_and_adds_banner(fake_roles, tmp_path):
    char_dir = tmp_path / "personas" / "pip"
    char_dir.mkdir(parents=True)
    char = char_dir / "character.md"
    char.write_text("# Pip\n\n<!-- ROLE:demo -->\n\nBackstory.\n")

    out = build.build_persona(char)

    assert out == char_dir / "pip.md"
    text = out.read_text()
    assert text.startswith("<!-- GENERATED FILE")
    assert "Source: personas/pip/character.md" in text
    assert "The injected body." in text
    assert "<!-- ROLE:demo -->" not in text
    assert "Standalone intro." not in text
    assert "Standalone notes." not in text


@pytest.mark.parametrize(
    "char_path",
    sorted(build.PERSONAS.glob("*/character.md")),
    ids=lambda p: p.parent.name,
)
def test_committed_persona_is_up_to_date(char_path, tmp_path):
    """The checked-in <name>.md must match a fresh build of its sources."""
    scratch = tmp_path / char_path.parent.name
    scratch.mkdir()
    shutil.copy(char_path, scratch / "character.md")

    rebuilt = build.build_persona(scratch / "character.md")

    committed = char_path.parent / rebuilt.name
    assert committed.read_text() == rebuilt.read_text(), (
        f"{committed.relative_to(build.ROOT)} is stale; run `python build.py`"
    )


def test_every_character_marker_names_an_existing_role():
    for char_path in build.PERSONAS.glob("*/character.md"):
        for codename in build.ROLE_MARKER.findall(char_path.read_text()):
            assert (build.ROLES / f"{codename}.md").exists(), (
                f"{char_path} references missing role '{codename}'"
            )


def test_main_reports_built_files(fake_roles, tmp_path, monkeypatch, capsys):
    personas = tmp_path / "personas"
    (personas / "pip").mkdir(parents=True)
    (personas / "pip" / "character.md").write_text("<!-- ROLE:demo -->\n")
    monkeypatch.setattr(build, "PERSONAS", personas)
    monkeypatch.setattr(build, "ROOT", tmp_path)

    build.main()

    assert "built personas/pip/pip.md" in capsys.readouterr().out
    assert (personas / "pip" / "pip.md").exists()


def test_main_with_no_characters(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(build, "PERSONAS", tmp_path)

    build.main()

    assert "nothing to build" in capsys.readouterr().out


def test_repo_root_is_this_checkout():
    assert Path(__file__).resolve().parent.parent == build.ROOT


def test_markdownlint_ignores_every_generated_persona():
    """Each generated <name>.md must be in the markdownlint ignore list.

    Otherwise adding a persona without updating the config makes CI lint
    generated output instead of its sources.
    """
    config_text = (build.ROOT / ".markdownlint-cli2.jsonc").read_text()
    # The config is JSONC; drop full-line // comments so json can parse it.
    config = json.loads(re.sub(r"^\s*//.*$", "", config_text, flags=re.MULTILINE))
    ignores = set(config["ignores"])

    char_paths = list(build.PERSONAS.glob("*/character.md"))
    assert char_paths, "no character.md files found; is PERSONAS pointing at the repo?"

    for char_path in char_paths:
        name = char_path.parent.name
        generated = f"personas/{name}/{name}.md"
        assert generated in ignores, (
            f"add {generated!r} to 'ignores' in .markdownlint-cli2.jsonc"
        )
