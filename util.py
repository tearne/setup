import os
import util
import sys
import getpass
import subprocess

import ensure
ensure.package("pexpect")

# pylint: disable=wrong-import-position,wrong-import-order
import pexpect


class Password:
    def __init__(self):
        self.p = None

    def get(self):
        if self.p:
            return self.p
        else:
            self.p = getpass.getpass()
            return self.p


def run(cmd, cwd=None, capture_output=False):
    print("*** Running:", cmd)
    
    return subprocess.run(
        cmd,
        shell=True,
        capture_output=capture_output,
        text=True,
        encoding='utf8',
        check=False,
        cwd=cwd
    )


def am_root():
    return os.geteuid() == 0


def is_aarch64():
    return os.uname().machine == 'aarch64'


def zero_exit_code(command):
    if util.run(command).returncode == 0:
        print(" - returned zero exit code")
        return True
    else:
        return False


def sudo(cmd, password, timeout=None, cwd=None):
    if am_root():
        run(cmd, cwd)
    else:
        command = f"sudo {cmd}"
        print("*** Running (sudo): ", cmd)
        print(f"     Timeout = {timeout}")
        child = pexpect.spawnu(command, cwd=cwd, timeout=timeout)
        child.logfile_read = sys.stdout
        options = ['password', pexpect.TIMEOUT, pexpect.EOF]
        index = child.expect(options, timeout=1)
        if index > 0:
            print(
                f"Error waiting for password prompt:\
                {options[index]} - {child.before.decode()}"
            )
            sys.exit(1)

        child.sendline(password.get())

        options = [pexpect.EOF, 'try again', pexpect.TIMEOUT]
        index = child.expect(options,timeout=timeout)
        if index == 0:
            return
        elif index == 1:
            print(f"Authentication failure: {options[index]}")
            sys.exit(1)
        else:
            print(f"Command failure running: {cmd}\n {options[index]}")
            sys.exit(1)
