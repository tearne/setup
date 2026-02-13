# Definitions

## Python Orchestrated Script (POS)
The POS style helps Python code take the place of native shell scripts. It strategically breaks some Python idioms in order to combine the different strengths of Python and shell scripts, while remaining simple to work with.

POS guidance:
- If there is a reasonably simple command to achieve a task in the shell, prefer running that command in a subprocess over the more Pythonic equivalent.
- This makes it easier for users to discover the command they may want to copy and paste into a terminal.
    - Examples:
        - To download the latest version of the `helix` `deb` for `amd64`:
        ```py
        subprocess.run(r"""curl -s https://api.github.com/repos/helix-editor/helix/releases/latest | grep -oP '"browser_download_url": "\K[^"]*amd64.deb' | xargs wget""")
        ```
        - To apt install `curl`:
        ```py
        subprocess.run("""DEBIAN_FRONTEND=noninteractive apt-get install -y curl""")
        ```
    - But don't take this to an extreme and force trivial actions like loops into to the shell.
- Prefer a single Python source file, unless it compromises readability.
- Make the python file executable and use a `uv` shebang
```sh
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = "==3.12.*"
# ///
```
