Python scripts are often best run in virtual environments, especially if they require a Python version or packages which might interact with the OS managed Python.

This folder contains two examples which ensure the Python runs in a venv, by creating it, installing dependencies, and only then running the script.

 - `all_in_one.py.sh` is a shell script with the Python embedded in a heredoc.
 - `separate_runner/` contains a separate shell script runner and Python scirpt file.  The script contains an additional check to ensure it's only in a venv. 

The benefits of the separate runner are that:
 - You don't get a mess of syntax warnings due to a mish-mash of shell and Python in one file.
 - Error line numbers in the Python code are correct, rather than offset due to use of a heredoc.

The code in both examples do the same thing:
1. Build the venv as required. 
1. Start Python in it.
1. Ensure pip dependencies are installed.
1. Run the user script.

