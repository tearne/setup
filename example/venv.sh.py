#!/bin/bash

# This example demonstrates a single Python script file which 
# (a) runs in it's own virtual environment, creating it if necessary,
# (b) installs dependencies with pip

VENV_NAME=venv

set -e
cd "$(cd -P -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
if ! test -f $VENV_NAME/bin/python; then
  echo " * Creating virtual environment: ${VENV_NAME}"
  python3 -m venv $VENV_NAME
fi

$VENV_NAME/bin/python <<END_PYTHON
import importlib, subprocess, sys
def ensure(package):
  try: importlib.import_module(package)
  except ImportError:
    print(f" * Installing package: {package}")
    subprocess.check_call([sys.executable,'-m','pip','install',package,'--disable-pip-version-check'])
    importlib.invalidate_caches()
    importlib.import_module(package)
ensure("rich")
###########################
# Python user script start
###########################

from rich import print
print("[bold green]Hello[/bold green], [bold blue]World[/bold blue]!", ":globe_showing_europe-africa:")

END_PYTHON