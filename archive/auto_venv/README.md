Python scripts are often best run in virtual environments, especially if they require a Python version or packages which might interact with the OS managed Python.

This folder contains two examples which ensure the script runs in a venv, by first creating it, installing dependencies, and only then running the script.

- `all_in_one.py.sh` is a shell script with the Python embedded in a heredoc.
- `separate_runner/` contains a separate (BASH) runner and Python scirpt file.  The script also contains an additional check to ensure it only runs in a venv. 

Benefits of each approach include:

|`all_in_one.py.sh`|`separate_runner/`|
|-|-|
|A single file, ideal for target audiences who aren't interested in how it works.|You don't get a mess of syntax warnings due to a mish-mash of shell and Python in one file.|
|Demonstrates a dynamic way to install Python packages while it's running, which is useful in some circumstances.|A more idiomatic approach, with separate Python source file and  `requirements.txt` file.|
||Error line numbers in Python are correct, rather than offset due to use of a heredoc.|


Both examples do the same things:
1. Build the venv, if required. 
1. Start Python in it.
1. Ensure pip dependencies are installed.
1. Run the user script.

