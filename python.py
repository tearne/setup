#!/usr/bin/env python3
import tempfile
import util


def main(password):
    py_version = "3.12.1"
    compile_and_install_python(py_version, password)
    # ensure_venv(
    #     py_version,
    #     "GitPython",
    #     "boto3",
    #     "dpath",
    #     "lxml",
    #     "polars",
    #     "seaborn",
    #     "pyarrow",
    #     "pandas"
    # )


def ensure_venv(version, *libs):
    ver_minor = '.'.join(version.split('.')[0:2])
    util.run(f"python{ver_minor} -m venv ~/venv")
    util.run(f""". ~/venv/bin/activate \
             && pip{ver_minor} install {" ".join(libs)}""")


def compile_and_install_python(ver, password, del_tmp=True):
    ver_minor = '.'.join(ver.split('.')[0:2])

    if util.run(f"python{ver_minor} --version").returncode == 0:
        print(" - already installed")
        return
    util.sudo("apt update", password, 60)
    util.sudo("""apt install -y curl wget python3-pip""", password, 60)

    util.sudo(
        "DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install \
        build-essential libreadline-dev libncursesw5-dev libssl-dev \
        libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev \
        libffi-dev zlib1g-dev",
        password,
        60
    )

    tempdir = tempfile.mkdtemp(prefix="build-")
    print("* Build in ", tempdir)

    util.run(
        f"wget \
        -c https://www.python.org/ftp/python/{ver}/Python-{ver}.tar.xz \
        -O - | tar -Jx",
        tempdir
    )

    py_dir = f"{tempdir}/Python-{ver}"
    util.sudo(
        "./configure --enable-optimizations",
        password,
        300,
        cwd=py_dir
    )
    util.sudo(
        "make altinstall",
        password,
        timeout=None,
        cwd=py_dir
    )

    if del_tmp:
        util.sudo(
            f"rm -rf {tempdir}",
            password,
            5
        )


if __name__ == "__main__":
    main(util.Password())
