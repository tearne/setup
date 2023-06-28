#!/usr/bin/env python3
import util
import cargo
import helix


def main(password):
    helix.ensure(password)
    ensure_zellij()
    ensure_broot(password)


def ensure_zellij():
    if util.zero_exit_code("zellij -V"):
        return
    print(" - installing zellij")

    cargo.ensure_cargo()
    util.run("cargo install --locked zellij")


def ensure_broot(password=util.Password()):
    if util.zero_exit_code("broot -V"):
        return
    print(" - installing broot")

    cargo.ensure_cargo()
    util.sudo(
        "apt install -y build-essential\
            ibxcb1-dev\
            ibxcb-render0-dev\
            ibxcb-shape0-dev\
            ibxcb-xfixes0-dev",
        password)
    util.run("cargo install --locked broot")


def ensure_lazygit(password=util.Password()):
    if util.zero_exit_code("lazygit -v"):
        return
    print(" - installing lazygit")

    ver = util.run(
        r"curl -s \"https://api.github.com/\
            repos/jesseduffield/lazygit/releases/latest\" \
            | grep -Po '\"tag_name\": \"v\\K[^\"]*'",
        capture_output=True
    ).stdout.rstrip()
    arch = ("arm64" if util.is_aarch64 else "x86_64")

    file = f"lazygit_{ver}_Linux_{arch}.gz"

    util.run(
        f"curl -Lo lazygit.tar.gz \
            \"https://github.com/jesseduffield/\
            lazygit/releases/latest/download/{file}\""
    )
    util.run("tar xf lazygit.tar.gz lazygit")
    util.sudo("install lazygit /usr/local/bin", password)


if __name__ == "__main__":
    main(util.Password())
