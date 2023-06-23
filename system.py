#!/usr/bin/env python3
import util
import cargo


def main(password):
    install_helix(password)
    install_zellij()
    install_broot(password)


def install_zellij():
    if util.run("zellij -V").returncode == 0:
        print(" - already installed")
        return
    cargo.install_cargo()
    util.run("cargo install --locked zellij")
    
def install_broot(password=util.Password()):
    if util.run("broot -V").returncode == 0:
        print(" - already installed")
        return

    cargo.install_cargo()
    util.sudo("apt install -y build-essential libxcb1-dev libxcb-render0-dev libxcb-shape0-dev libxcb-xfixes0-dev", password)
    util.run("cargo install --locked broot")


def install_lazygit(password=util.Password()):
    if util.run("lazygit -v").returncode == 0:
        print(" - already installed")
        return

    ver = util.run(
        r"""curl -s "https://api.github.com/repos/jesseduffield/lazygit/releases/latest" | grep -Po '"tag_name": "v\K[^"]*'""",
        capture_output=True
    ).stdout.rstrip()
    arch = ("arm64" if util.is_aarch64 else "x86_64")

    file = f"lazygit_{ver}_Linux_{arch}.gz"

    util.run(f"curl -Lo lazygit.tar.gz \"https://github.com/jesseduffield/lazygit/releases/latest/download/{file}\"")
    util.run("tar xf lazygit.tar.gz lazygit")
    util.sudo("install lazygit /usr/local/bin", password)


def install_helix(password=util.Password()):
    if util.run("hx -V").returncode == 0:
        print(" - already installed")
        return
    
    util.sudo("add-apt-repository -y ppa:maveonair/helix-editor", password)
    util.sudo("apt update", password)
    util.sudo("apt install helix", password)


if __name__ == "__main__":
    main(util.Password())
