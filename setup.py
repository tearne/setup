#!/usr/bin/env -S uv run --script
# /// script
# requires-python = "==3.12.*"
# ///

import subprocess
import sys
import os
import shutil
import getpass
import platform
import tarfile
import urllib.request
import json
from pathlib import Path
from contextlib import contextmanager

# ---------------------------------------------------------------------------
# Comment out any tool you don't want installed
# ---------------------------------------------------------------------------
TOOLS = [
    "htop",
    "btop",
    "incus",
    "rust",
    "zellij",
    "helix",
]

# ---------------------------------------------------------------------------
# Utility layer
# ---------------------------------------------------------------------------

_indent = 0
_password = None
SCRIPT_DIR = Path(__file__).resolve().parent


def log(msg):
    prefix = "  " * _indent
    for line in msg.splitlines():
        print(f"{prefix}{line}", flush=True)


@contextmanager
def task(name):
    global _indent
    log(f"▶ {name}")
    _indent += 1
    try:
        yield
    finally:
        _indent -= 1


def run(cmd, env=None):
    merged = {**os.environ, **(env or {})}
    result = subprocess.run(
        cmd, shell=True, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        env=merged,
    )
    if result.stdout.strip():
        for line in result.stdout.strip().splitlines():
            log(line)
    if result.returncode != 0:
        log(f"FAILED (exit {result.returncode}): {cmd}")
        sys.exit(1)


def sudo(cmd, env=None):
    if os.geteuid() == 0:
        run(cmd, env=env)
    else:
        full = f"sudo -S {cmd}"
        merged = {**os.environ, **(env or {})}
        result = subprocess.run(
            full, shell=True, text=True,
            input=_password + "\n",
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            env=merged,
        )
        if result.stdout.strip():
            for line in result.stdout.strip().splitlines():
                log(line)
        if result.returncode != 0:
            log(f"FAILED (exit {result.returncode}): {cmd}")
            sys.exit(1)


def init_password():
    global _password
    if os.geteuid() == 0:
        return
    _password = getpass.getpass("Enter sudo password: ")
    # Validate it
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
# Installers
# ---------------------------------------------------------------------------

def install_htop():
    with task("htop"):
        if is_installed("htop"):
            log("already installed, skipping")
            return
        sudo("apt-get install -y -qq htop", env={"DEBIAN_FRONTEND": "noninteractive"})
        log("done")


def install_btop():
    with task("btop"):
        if is_installed("btop"):
            log("already installed, skipping")
            return
        sudo("apt-get install -y -qq btop", env={"DEBIAN_FRONTEND": "noninteractive"})
        log("done")


def install_incus():
    with task("incus"):
        if is_installed("incus"):
            log("already installed, skipping")
            return
        sudo("apt-get install -y -qq incus", env={"DEBIAN_FRONTEND": "noninteractive"})
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

        machine = platform.machine()
        if machine == "x86_64":
            arch = "x86_64"
        elif machine == "aarch64":
            arch = "aarch64"
        else:
            log(f"Unsupported architecture: {machine}")
            sys.exit(1)

        with task("downloading latest release"):
            url = "https://api.github.com/repos/helix-editor/helix/releases/latest"
            with urllib.request.urlopen(url) as resp:
                release = json.loads(resp.read())

            tag = release["tag_name"]
            log(f"latest release: {tag}")

            # Find the tarball for this arch
            target = f"{arch}-linux"
            asset_url = None
            for asset in release["assets"]:
                name = asset["name"]
                if target in name and name.endswith(".tar.xz"):
                    asset_url = asset["browser_download_url"]
                    break

            if not asset_url:
                log(f"No release asset found for {target}")
                sys.exit(1)

            log(f"downloading {asset_url}")
            archive_path = Path("/tmp/helix-release.tar.xz")
            urllib.request.urlretrieve(asset_url, archive_path)

        with task("installing"):
            extract_dir = Path("/tmp/helix-extract")
            if extract_dir.exists():
                shutil.rmtree(extract_dir)
            extract_dir.mkdir()

            with tarfile.open(archive_path, "r:xz") as tar:
                tar.extractall(extract_dir)

            # Find the extracted directory (e.g. helix-25.01-x86_64-linux)
            extracted = list(extract_dir.iterdir())
            if len(extracted) != 1:
                log(f"Unexpected archive contents: {extracted}")
                sys.exit(1)
            helix_dir = extracted[0]

            local_bin = Path.home() / ".local" / "bin"
            local_bin.mkdir(parents=True, exist_ok=True)

            # Install the binary
            src_bin = helix_dir / "hx"
            dst_bin = local_bin / "hx"
            shutil.copy2(src_bin, dst_bin)
            dst_bin.chmod(0o755)

            # Install the runtime directory alongside the binary
            src_runtime = helix_dir / "runtime"
            dst_runtime = Path.home() / ".config" / "helix" / "runtime"
            dst_runtime.parent.mkdir(parents=True, exist_ok=True)
            if dst_runtime.exists():
                shutil.rmtree(dst_runtime)
            shutil.copytree(src_runtime, dst_runtime)

            # Ensure ~/.local/bin is on PATH
            if str(local_bin) not in os.environ["PATH"]:
                os.environ["PATH"] = str(local_bin) + ":" + os.environ["PATH"]

            log("done")

        # Cleanup
        archive_path.unlink(missing_ok=True)
        shutil.rmtree(extract_dir, ignore_errors=True)

        _link_helix_config()


def _link_helix_config():
    with task("helix config"):
        src = SCRIPT_DIR / "resources" / "helix" / "config.toml"
        dst = Path.home() / ".config" / "helix" / "config.toml"
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.exists() or dst.is_symlink():
            if dst.is_symlink() and dst.resolve() == src.resolve():
                log("symlink already correct")
                return
            log(f"WARNING: {dst} already exists, replacing")
            dst.unlink()
        os.symlink(src, dst)
        log(f"symlinked {dst} -> {src}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

INSTALLER = {
    "htop": install_htop,
    "btop": install_btop,
    "incus": install_incus,
    "rust": install_rust,
    "zellij": install_zellij,
    "helix": install_helix,
}


def main():
    with task("Dev environment setup"):
        init_password()

        with task("apt update"):
            sudo("apt-get update -qq", env={"DEBIAN_FRONTEND": "noninteractive"})

        for tool in TOOLS:
            INSTALLER[tool]()

    log("Setup complete.")


if __name__ == "__main__":
    main()
