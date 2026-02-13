#!/usr/bin/env -S uv run --script
# /// script
# requires-python = "==3.12.*"
# ///

import subprocess
import sys
import os
import shutil
import getpass
import difflib
from pathlib import Path
from contextlib import contextmanager

# ---------------------------------------------------------------------------
# Comment out any tool you don't want installed
# ---------------------------------------------------------------------------

def install():
    install_htop()
    install_btop()
    install_incus()
    init_incus()
    install_rust()
    install_zellij()
    install_helix()
    install_harper_ls()
    install_tok()
    setup_local_bin_path()


# ---------------------------------------------------------------------------
# Installers
# ---------------------------------------------------------------------------

def install_htop():
    with task("htop"):
        if is_installed("htop"):
            log("already installed, skipping")
            return
        sudo("DEBIAN_FRONTEND=noninteractive apt-get install -y -qq htop")
        log("done")


def install_btop():
    with task("btop"):
        if is_installed("btop"):
            log("already installed, skipping")
            return
        sudo("DEBIAN_FRONTEND=noninteractive apt-get install -y -qq btop")
        log("done")


def install_incus():
    with task("incus"):
        if is_installed("incus"):
            log("already installed, skipping")
            return
        sudo("DEBIAN_FRONTEND=noninteractive apt-get install -y -qq incus")
        log("done")


def init_incus():
    in_container = subprocess.run("systemd-detect-virt --container --quiet", shell=True).returncode == 0
    # ZFS backend not tested in containers (no kernel modules available)
    backend = "dir" if in_container else "zfs"

    with task(f"incus init ({backend})"):
        sudo("systemctl start incus.service")
        if subprocess.run("incus storage show default", shell=True, capture_output=True).returncode == 0:
            log("already initialized, skipping")
            return
        if backend == "zfs":
            sudo("DEBIAN_FRONTEND=noninteractive apt-get install -y -qq zfsutils-linux")
        sudo(f"incus admin init --auto --storage-backend={backend}")
        log("done")


def install_rust():
    with task("Rust + Cargo + rust-analyzer"):
        if is_installed("rustc"):
            log("already installed, skipping")
            return
        run("curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y")
        cargo_bin = Path.home() / ".cargo" / "bin"
        os.environ["PATH"] = str(cargo_bin) + ":" + os.environ["PATH"]
        run("rustup component add rust-analyzer")
        log("done")


def install_zellij():
    with task("Zellij"):
        if is_installed("zellij"):
            log("already installed, skipping")
            return
        if not is_installed("cargo-binstall"):
            with task("cargo-binstall"):
                run("curl -L --proto '=https' --tlsv1.2 -sSf https://raw.githubusercontent.com/cargo-bins/cargo-binstall/main/install-from-binstall-release.sh | bash")
        run("cargo binstall --no-confirm zellij")
        log("done")


def install_helix():
    with task("Helix editor"):
        if is_installed("hx"):
            log("already installed, skipping")
            _link_helix_config()
            return

        with task("downloading latest .deb"):
            run(r"""curl -s https://api.github.com/repos/helix-editor/helix/releases/latest | grep -oP '"browser_download_url": "\K[^"]*amd64\.deb' | xargs curl -Lo /tmp/helix.deb""")

        with task("installing"):
            sudo("dpkg -i /tmp/helix.deb")
            run("rm /tmp/helix.deb")
            log("done")

        _link_helix_config()


def _link_helix_config():
    configs = [
        ("config.toml", "helix config"),
        ("languages.toml", "helix languages"),
    ]
    for filename, label in configs:
        with task(label):
            src = SCRIPT_DIR / "resources" / "helix" / filename
            dst = Path.home() / ".config" / "helix" / filename
            dst.parent.mkdir(parents=True, exist_ok=True)
            if dst.is_symlink() or dst.exists():
                if dst.is_symlink() and dst.resolve() == src.resolve():
                    log("symlink already correct")
                    continue
                if dst.is_symlink() and not dst.exists():
                    log(f"replacing dangling symlink {dst}")
                    dst.unlink()
                else:
                    diff = _config_diff(src, dst)
                    if diff is None:
                        log(f"{dst} exists with equivalent content, skipping")
                        continue
                    warn(f"{dst} differs from installable config, not overwriting (delete and rerun to update)", diff=diff)
                    continue
            rel = os.path.relpath(src, dst.parent)
            os.symlink(rel, dst)
            log(f"symlinked {dst} -> {rel}")


def install_harper_ls():
    with task("harper-ls"):
        if is_installed("harper-ls"):
            log("already installed, skipping")
            return
        run("cargo binstall --no-confirm harper-ls")
        log("done")


def setup_local_bin_path():
    with task("~/.local/bin on PATH"):
        profile = Path.home() / ".profile"
        marker = 'PATH="$HOME/.local/bin:$PATH"'
        if profile.exists() and marker in profile.read_text():
            log("already configured")
            return
        with open(profile, "a") as f:
            f.write(f'\n# Added by setup.py\nexport {marker}\n')
        log(f"appended to {profile}")


def install_tok():
    with task("tok"):
        src = SCRIPT_DIR / "resources" / "tok" / "tok"
        dst = Path.home() / ".local" / "bin" / "tok"
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.is_symlink() or dst.exists():
            if dst.is_symlink() and dst.resolve() == src.resolve():
                log("symlink already correct")
                return
            if dst.is_symlink() and not dst.exists():
                log(f"replacing dangling symlink {dst}")
                dst.unlink()
            else:
                warn(f"{dst} already exists, not overwriting")
                return
        rel = os.path.relpath(src, dst.parent)
        os.symlink(rel, dst)
        log(f"symlinked {dst} -> {rel}")


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

_indent = 0
_password = None
_warnings = []
SCRIPT_DIR = Path(__file__).resolve().parent


def log(msg):
    prefix = "  " * _indent
    for line in msg.splitlines():
        print(f"{prefix}{line}", flush=True)


def warn(msg, diff=None):
    log(f"WARNING: {msg}")
    _warnings.append((msg, diff))


def _config_diff(src, dst):
    """Compare two config files ignoring whitespace.
    Returns unified diff string if they differ, None if equivalent."""
    src_lines = src.read_text().splitlines()
    dst_lines = dst.read_text().splitlines()
    if [l.strip() for l in src_lines] == [l.strip() for l in dst_lines]:
        return None
    return "\n".join(difflib.unified_diff(
        dst_lines, src_lines,
        fromfile=str(dst), tofile=str(src),
        lineterm="",
    ))


@contextmanager
def task(name):
    global _indent
    log(f"▶ {name}")
    _indent += 1
    try:
        yield
    finally:
        _indent -= 1


def run(cmd):
    proc = subprocess.Popen(
        cmd, shell=True, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    for line in proc.stdout:
        log(line.rstrip("\n"))
    proc.wait()
    if proc.returncode != 0:
        log(f"FAILED (exit {proc.returncode}): {cmd}")
        sys.exit(1)


def sudo(cmd):
    if os.geteuid() == 0:
        run(cmd)
    else:
        full = f"sudo -S {cmd}"
        proc = subprocess.Popen(
            full, shell=True, text=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        )
        proc.stdin.write(_password + "\n")
        proc.stdin.close()
        for line in proc.stdout:
            log(line.rstrip("\n"))
        proc.wait()
        if proc.returncode != 0:
            log(f"FAILED (exit {proc.returncode}): {cmd}")
            sys.exit(1)


def init_password():
    global _password
    if os.geteuid() == 0:
        return
    if subprocess.run("sudo -n true", shell=True, capture_output=True).returncode == 0:
        return
    _password = getpass.getpass("Enter sudo password: ")
    result = subprocess.run(
        "sudo -S true", shell=True, text=True,
        input=_password + "\n",
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    if result.returncode != 0:
        print("Error: incorrect password.")
        sys.exit(1)


def is_installed(cmd):
    return shutil.which(cmd) is not None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    with task("Dev environment setup"):
        init_password()

        with task("apt update"):
            sudo("DEBIAN_FRONTEND=noninteractive apt-get update -qq")

        install()

    if _warnings:
        log("")
        log("Warnings:")
        for msg, diff in _warnings:
            log(f"  - {msg}")
            if diff:
                for line in diff.splitlines():
                    log(f"    {line}")

    log("Setup complete.")


if __name__ == "__main__":
    main()
