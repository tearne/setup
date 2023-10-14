#!/bin/bash
# 1. Starts as a BASH script, ensuring working dir is script location
# 2. Creates a virtual environment, if it doesn't already exist
# 3. Starts Python from the venv, to avoid system pollution
# 4. Defines minimal `ensure` fn to install package(s) with pip
# 5. Runs user Python script
VENV_NAME=venv

set -e
cd "$(cd -P -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
if ! test -f $VENV_NAME/bin/python; then
  echo " * Creating virtual environment: ${VENV_NAME}"
  python3 -m venv $VENV_NAME
fi

export PIP_DISABLE_PIP_VERSION_CHECK=1
echo " * Starting Python"


$VENV_NAME/bin/python <<END_PYTHON
import importlib, subprocess, sys
def ensure(package):
  try: importlib.import_module(package)
  except ImportError:
    print(f" * Installing package: {package}")
    subprocess.check_call([sys.executable,'-m','pip','install',package])
    importlib.invalidate_caches()
    importlib.import_module(package)

ensure("rich")
###########################
# Python user script start
###########################

from rich import print
print("[bold green]Hello[/bold green], [bold blue]World[/bold blue]!", ":globe_showing_europe-africa:")

END_PYTHON