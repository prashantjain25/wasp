"""
Structural tests for CLI commands and menu architecture.
Verifies two-level (backend -> model) pattern, no /backend, HELP content.
"""

import ast, os, sys

CLI_PATH = os.path.expanduser("~/wasp/wasp")

def test_syntax():
    """File must be valid Python."""
    with open(CLI_PATH) as f:
        ast.parse(f.read())

def test_no_cmd_backend():
    """cmd_backend function must not exist (removed)."""
    with open(CLI_PATH) as f:
        tree = ast.parse(f.read())
    names = {n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}
    assert "cmd_backend" not in names, "cmd_backend still defined"

def test_no_backend_in_commands():
    """COMMANDS dict must not have '/backend' entry."""
    with open(CLI_PATH) as f:
        content = f.read()
    # Extract COMMANDS dict
    start = content.find("COMMANDS = {")
    end = content.find("}", start)
    cmds = content[start:end]
    assert "/backend" not in cmds, "/backend still in COMMANDS"

def test_commands_present():
    """All expected commands must be in COMMANDS dict."""
    with open(CLI_PATH) as f:
        content = f.read()
    start = content.find("COMMANDS = {")
    end = content.find("}", start)
    cmds = content[start:end]
    for cmd in ["/start", "/stop", "/model", "/settings", "/agent"]:
        assert cmd in cmds, f"{cmd} missing from COMMANDS"

def test_cmd_start_two_level():
    """cmd_start must list providers (not flat models) in first level."""
    with open(CLI_PATH) as f:
        content = f.read()
    # Find cmd_start
    start = content.find("def cmd_start(")
    end = content.find("\ndef ", start + 1)
    body = content[start:end]
    assert "Select backend" in body, "cmd_start should show backend list first"
    assert "Two-level" in body, "cmd_start missing two-level docstring"

def test_cmd_stop_two_level():
    """cmd_stop must list providers in first level."""
    with open(CLI_PATH) as f:
        content = f.read()
    start = content.find("def cmd_stop(")
    end = content.find("\ndef ", start + 1)
    body = content[start:end]
    assert "Select backend" in body, "cmd_stop should show backend list first"
    assert "Two-level" in body, "cmd_stop missing two-level docstring"

def test_cmd_model_two_level():
    """cmd_model must list providers in first level."""
    with open(CLI_PATH) as f:
        content = f.read()
    start = content.find("def cmd_model(")
    end = content.find("\ndef ", start + 1)
    body = content[start:end]
    assert "Select backend" in body, "cmd_model should show backend list first"
    assert "Two-level" in body, "cmd_model missing two-level docstring"

def test_pick_is_arrow_key():
    """menu.pick must be arrow-key style, not numbered input."""
    menu_path = os.path.expanduser("~/wasp/menu.py")
    with open(menu_path) as f:
        content = f.read()
    assert "Arrow-key" in content, "menu.pick should use arrow-key navigation"
    assert "tty.setraw" in content, "menu.pick should use raw terminal input"
    assert "\\x1b[A" in content or "\x1b[A" in content, "menu.pick missing up-arrow handler"

def test_help_no_flat_list():
    """HELP should describe two-level pattern, not 'flat list'."""
    with open(CLI_PATH) as f:
        content = f.read()
    start = content.find("HELP = \"\"\"")
    end = content.find("\"\"\"", start + 8)
    help_text = content[start:end]
    assert "flat list" not in help_text.lower(), "HELP still mentions flat list"
    assert "Pick backend" in help_text, "HELP missing two-level description"

def test_logging_proxy_kept():
    """LoggingProxy must be preserved for architecture extensibility."""
    with open(CLI_PATH) as f:
        content = f.read()
    assert "class LoggingProxy" in content, "LoggingProxy was removed"

def test_cloud_extension_comment():
    """Factory must have cloud provider extension comment."""
    with open(CLI_PATH) as f:
        content = f.read()
    assert "Future cloud/internet LLM providers" in content, "Cloud extension comment missing"

def test_no_shutil():
    """shutil import must not exist (unused)."""
    with open(CLI_PATH) as f:
        content = f.read()
    assert "import shutil" not in content, "shutil still imported"

def test_no_any_typing():
    """Any must not be in typing import (unused)."""
    with open(CLI_PATH) as f:
        content = f.read()
    assert "from typing import Any" not in content, "Any still in typing import"

def test_providers_cloud_stub():
    """providers_cloud.py must exist with docstring."""
    stub = os.path.expanduser("~/wasp/providers_cloud.py")
    assert os.path.exists(stub), "providers_cloud.py missing"
    with open(stub) as f:
        assert "Cloud" in f.read(), "providers_cloud.py missing docstring"

def test_help_examples():
    """HELP must have workflow examples."""
    with open(CLI_PATH) as f:
        content = f.read()
    start = content.find("HELP = \"\"\"")
    end = content.find("\"\"\"", start + 8)
    help_text = content[start:end]
    # Should have at least 3 example sections
    examples = [l for l in help_text.split("\n") if "wasp " in l and not l.strip().startswith("    /")]
    assert len(examples) >= 3, f"Only {len(examples)} examples in HELP"







def test_model_sublist_matches_by_id():
    """_model_sublist must match names by ID, not index position."""
    with open(CLI_PATH) as f:
        content = f.read()
    # _model_sublist and cmd_stop should both use name_map dict lookup
    for func in ["_model_sublist"]:
        start = content.find("def " + func)
        end = content.find("\n\ndef ", start)
        body = content[start:end]
        assert "name_map" in body, f"{func} missing name_map lookup"
        assert "name_map.get(mid, mid)" in body or "name_map.get(mid" in body, f"{func} missing .get() call"

def test_menu_import():
    """menu.pick must be importable."""
    from menu import pick
    assert callable(pick)
        # Early return for <2 items (no stdin needed)
    assert pick(["only"]) == -1
    assert pick(["only"]) == -1


def test_is_running_uses_urlopen():
    """is_running() must use urlopen(), not Request.open()."""
    with open(CLI_PATH) as f:
        content = f.read()
    start = content.find("def is_running")
    end = content.find("\n    def ", start + 1)
    body = content[start:end]
    assert "urlopen" in body, "is_running missing urlopen call"
    assert ".open(timeout" not in body, "is_running uses wrong .open() pattern"

def test_no_fzf_references():
    """No fzf references should exist in the file."""
    with open(CLI_PATH) as f:
        content = f.read()
    # Only exception is the _pick docstring mention
    assert "fzf" not in content.lower(), "fzf still referenced in code"
