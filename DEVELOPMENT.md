# Development

## I use

- VS Code as IDE
- GitBash as terminal

## Run locally

### Setup poetry

- make sure to have poetry installed (`pip install poetry`)
- run `poetry install` while being in the root of this repository

### Start from console

```bash
poetry run python movenue/app.py
```

### Start with VS Code Debugger

Select poetry environment as interpreter (bottom right if you have any py file open)

Create `.vscode/launch.json` with below content

```json
{
  // Use IntelliSense to learn about possible attributes.
  // Hover to view descriptions of existing attributes.
  // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug App",
      "type": "debugpy",
      "request": "launch",
      "program": "movenue/ui/app.py",
      "console": "integratedTerminal"
    }
  ]
}
```

Use "Debug and Run" tab on the left of your screen
