#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [ ]
# ///

from subprocess import run
import os

def main():
    ensure_cargo()


    
if "VIRTUAL_ENV" not in os.environ:
    raise SystemExit("Not running in venv.  Check if 'uv' is installed...")
    is_installed = run("uv -v", shell=True).returncode == 0
    print("is_installed", is_installed)
else:
    print(f"You're running from venv: {os.environ["VIRTUAL_ENV"]}")



def ensure_cargo():
    if run("cargo -V", shell=True).returncode == 0:
        print(" -  already installed")
        return

    run("curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y")
    # Update the path used by this Python process to include newly installed `cargo`
    pattern = "^PATH=(.*?)\\n$"
    string = run(""". "$HOME/.cargo/env" && env | grep ^PATH""", capture_output=True).stdout
    match = re.search(pattern, string)
    os.environ["PATH"] = match.group(1)


if __name__ == "__main__":
    main()
