# school-notes

## One-time setup

Run `.\setup.ps1` from the repo root. It creates `.venv`, installs the
Python packages `tools/` needs, and runs the example checks to confirm
everything works.

```
.\setup.ps1
```

If PowerShell blocks the script, run it once with:

```
powershell -ExecutionPolicy Bypass -File setup.ps1
```

After setup, run any tool in this repo as `.venv/Scripts/python <script>`
(not plain `python`, and no need to activate the venv).
