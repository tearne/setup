#!/usr/bin/python
import os
import util
import ensure
ensure.package("tempfile")
import tempfile

def install():
    password = util.Password()
 
    util.sudo("sudo apt-get -y install build-essential git libsystemd-dev", password)

    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Using temporary directory: {temp_dir}")
        util.run("git clone https://github.com/xorbit/LiFePO4wered-Pi.git", cwd=temp_dir)
        cwd = os.path.join(temp_dir, "LiFePO4wered-Pi")
        util.run("make all", cwd=cwd)
        util.sudo("sudo make user-install", password, cwd=cwd)

    print("Installed.  Get current battery voltage:")
    util.sudo("lifepo4wered-cli get vbat", password, timeout=5)


if __name__ == '__main__':
    install()