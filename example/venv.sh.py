#!/bin/bash

# This example script:
# (a) Builds its own python venv as required. 
# (b) Starts Python in it.
# (c) Ensures pip dependencies are installed.
# (d) Runs the user code.
#
# - It's terse to get to the user code quicker.
# - The heredoc can make line error reporting messy.
#   An alternative is importing another script from file.

VENV_NAME=venv; PYTHON=python3.11
set -eu
cd "$(cd -P -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
if ! test -f $VENV_NAME/bin/python; then
  echo " * Creating virtual environment: ${VENV_NAME}"
  $PYTHON -m venv $VENV_NAME
fi
. $VENV_NAME/bin/activate
$PYTHON - $@ <<END_PYTHON
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