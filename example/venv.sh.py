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

VENV=venv; PYTHON=python3
set -eu
cd "$(cd -P -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
if ! test -f $VENV/bin/python; then echo " * Creating ${VENV}" && $PYTHON -m venv $VENV; fi
. $VENV/bin/activate && $PYTHON - $@ <<END_PYTHON
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
from rich.console import Console
console = Console()
console.print("\n[bold]Languages\n")

console.rule('Python', style='blue')
console.print('''Python is a general-purpose, dynamic, object-oriented \
programming language. The design purpose of the Python language \
emphasizes programmer productivity and code readability.''')
console.print()

console.rule('Rust', style='red')
console.print('''Rust is a multi-paradigm, general-purpose programming \
language that emphasizes performance, type safety, and concurrency with \
features including memory ownership model and zero-cost abstractions.''')
console.print()


END_PYTHON