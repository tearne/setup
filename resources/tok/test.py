"""Tests for tok.py — pytest rewrite of test_tok.sh."""

import os
import signal
import subprocess
import time
from pathlib import Path

TOK = str(Path(__file__).parent / "tok.py")


def run_tok(args, stdin_text="", tok_dir=None, env_extra=None):
    env = os.environ.copy()
    if tok_dir:
        env["TOK_DIR"] = str(tok_dir)
    if env_extra:
        env.update(env_extra)
    return subprocess.run(
        [TOK, *args],
        input=stdin_text,
        capture_output=True,
        text=True,
        env=env,
    )


def add_secret(tok_dir, secret, passphrase, name=None):
    """Add a secret. If name is given it's appended (for the second+ secret)."""
    stdin = f"{secret}\n{passphrase}\n{passphrase}\n"
    if name is not None:
        stdin += f"{name}\n"
    return run_tok(["--add"], stdin_text=stdin, tok_dir=tok_dir)


# ---- Tests ----


def test_encrypt_decrypt_roundtrip(tmp_path):
    add_secret(tmp_path, "my-secret-token", "testpass")
    r = run_tok(["--stdout"], stdin_text="testpass\n", tok_dir=tmp_path)
    assert r.returncode == 0
    assert r.stdout.strip() == "my-secret-token"


def test_named_secret_roundtrip(tmp_path):
    add_secret(tmp_path, "my-secret-token", "testpass")
    add_secret(tmp_path, "another-secret", "testpass2", name="work")
    r = run_tok(["--stdout", "work"], stdin_text="testpass2\n", tok_dir=tmp_path)
    assert r.returncode == 0
    assert r.stdout.strip() == "another-secret"


def test_default_still_works_after_named(tmp_path):
    add_secret(tmp_path, "my-secret-token", "testpass")
    add_secret(tmp_path, "another-secret", "testpass2", name="work")
    r = run_tok(["--stdout"], stdin_text="testpass\n", tok_dir=tmp_path)
    assert r.returncode == 0
    assert r.stdout.strip() == "my-secret-token"


def test_list_includes_default(tmp_path):
    add_secret(tmp_path, "my-secret-token", "testpass")
    r = run_tok(["--list"], tok_dir=tmp_path)
    assert "default" in r.stdout


def test_list_includes_named(tmp_path):
    add_secret(tmp_path, "my-secret-token", "testpass")
    add_secret(tmp_path, "another-secret", "testpass2", name="work")
    r = run_tok(["--list"], tok_dir=tmp_path)
    assert "work" in r.stdout


def test_wrong_passphrase_rejected(tmp_path):
    add_secret(tmp_path, "my-secret-token", "testpass")
    r = run_tok(["--stdout"], stdin_text="wrongpass\n", tok_dir=tmp_path)
    assert r.returncode != 0


def test_missing_secret_rejected(tmp_path):
    add_secret(tmp_path, "my-secret-token", "testpass")
    r = run_tok(["--stdout", "nonexistent"], stdin_text="testpass\n", tok_dir=tmp_path)
    assert r.returncode != 0


def test_signal_clears_clipboard(tmp_path):
    # Set up a fake xclip that writes to a file
    add_secret(tmp_path, "my-secret-token", "testpass")

    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    clip_file = tmp_path / "clipboard"

    fake_xclip = fake_bin / "xclip"
    fake_xclip.write_text(f'#!/bin/bash\ncat > "{clip_file}"\n')
    fake_xclip.chmod(0o755)

    env = os.environ.copy()
    env["TOK_DIR"] = str(tmp_path)
    env["PATH"] = f"{fake_bin}:{env.get('PATH', '')}"
    env["DISPLAY"] = ":0"

    proc = subprocess.Popen(
        [TOK, "--time", "60"],
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
    )
    proc.stdin.write(b"testpass\n")
    proc.stdin.flush()

    # Wait for the secret to be copied
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline:
        if clip_file.exists() and clip_file.stat().st_size > 0:
            break
        time.sleep(0.1)

    assert clip_file.exists() and clip_file.stat().st_size > 0, \
        "secret was not copied to fake clipboard"

    proc.send_signal(signal.SIGTERM)
    proc.wait(timeout=5)

    # After SIGTERM the clipboard file should be empty (cleared)
    time.sleep(0.3)
    assert clip_file.read_text() == "", "clipboard was not cleared after signal"
