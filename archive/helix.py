#!/usr/bin/env python3
from pathlib import Path
import util


def ensure(password=util.Password()):
    print("*** Ensure helix")
    target_config = Path("~/.config/helix/config.toml").expanduser()
    held_config = Path("dot_config/helix/config.toml").absolute()

    if not (target_config.exists() or target_config.is_symlink()):
        print(f"*** linking helix config ({target_config})")
        target_config.parent.mkdir(parents=True, exist_ok=True)
        target_config.symlink_to(held_config)
    else:
        print(f" - Not linking config - already exists ({target_config})")

    if util.zero_exit_code("hx -V"):
        return
    print(" - installing helix")

    util.sudo("add-apt-repository -y ppa:maveonair/helix-editor", password)
    util.sudo("apt update", password)
    util.sudo("apt install helix", password)


if __name__ == "__main__":
    util.cd_script_dir()
    ensure(util.Password())
