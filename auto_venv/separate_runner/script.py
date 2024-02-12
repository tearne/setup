import importlib, subprocess, sys, os

if os.environ.get('VIRTUAL_ENV') is None:
    exit("Run this script from a venv to avoid polluting your system.")

def ensure(package):
  try: importlib.import_module(package)
  except ImportError:
    print(f" * Installing package: {package}")
    subprocess.check_call([sys.executable,'-m','pip','install',package,'--disable-pip-version-check'])
    importlib.invalidate_caches(); importlib.import_module(package)
ensure("rich")

###########################
# Python user script start
###########################
from rich.console import Console
console = Console()
console.print("\n[bold]Languages\n")

console.rule('Python', style='blue')
console.print('''Python is a general-purpose, dynamicly typed, object-oriented \
programming language that emphasizes productivity and readability.\n''')

console.rule('Rust', style='red')
console.print('''Rust is a multi-paradigm, general-purpose programming \
language that emphasizes performance, type safety, and concurrency.\n''')

