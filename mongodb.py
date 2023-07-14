#!/usr/bin/env python3
import util
import os

def ensure(password=util.Password()):
    print("*** Ensure mongodb")
    codename = util.run("lsb_release -cs", capture_output=True).stdout.strip()
    print("Codename is", codename)

    util.sudo("apt update", password)
    util.sudo("DEBIAN_FRONTEND=noninteractive apt-get install -y wget", password)
    
    util.sudo("bash -c \" wget -qO- https://www.mongodb.org/static/pgp/server-6.0.asc | apt-key add\"", password)
    util.sudo(f"""bash -c "echo deb https://repo.mongodb.org/apt/ubuntu {codename}/mongodb-org/6.0 multiverse | tee /etc/apt/sources.list.d/mongodb-org-6.0.list" """, password)

    util.sudo("apt update", password)
    util.sudo("apt install -y mongodb-org", password)

if __name__ == "__main__":
    util.cd_script_dir()
    ensure(util.Password())