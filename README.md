# Claude Certified Exam Prep Demos

This repo contains the demos shown during my LinkedIn Live Claude Certification exam prep sessions.

## Claude Certified Architect — Foundations

| Demo | Topic | How to run it |
|---|---|---|
| [demo1](ccar-f-demos/demo1/agent_loop.ipynb) | Anthropic SDK: manually managed agent loop | Notebook — needs the venv and an API key |
| [demo2](ccar-f-demos/demo2/hooks.ipynb) | Claude Agent SDK: `PreToolUse` and `PostToolUse` hooks | Notebook — needs the venv and an API key |
| [demo3](ccar-f-demos/demo3/tool_choice.ipynb) | Anthropic SDK: `tool_choice` | Notebook — needs the venv and an API key |
| [demo4](ccar-f-demos/demo4/README.md) | Path-scoped rules with `.claude/rules/` | Claude Code in VS Code — no setup |
| [demo5](ccar-f-demos/demo5/README.md) | Skill frontmatter: `context: fork`, `allowed-tools`, `argument-hint` | Claude Code in VS Code — no setup |
| [demo6](ccar-f-demos/demo6/structured_outputs.ipynb) | Anthropic SDK: enforcing a JSON schema with structured outputs | Notebook — needs the venv and an API key |

Demos 1–3 and 6 are Jupyter notebooks — follow the setup below to setup the execution environment.

Demos 4 and 5 run in a Claude Code session in VS Code and need no Python environment and no API key. Each has its own README with the steps to follow.

## VS Code Jupyter environment setup

It is reccomended to run all demos using VS Code. For the demos which use Jupyter notebooks, follow the steps below to setup your environment.

1. Create a Python virtual environment (venv) to use as the execution environment for the notebooks:
   * I reccomend using `uv` as its fast and neat solution — if you do not have `uv` installed, follow the instructions here: https://docs.astral.sh/uv/getting-started/installation/
   * Once `uv` is installed, open a Terminal window in VS Code and ensure you are in the repo directory (`claude-exam-prep-sample-code`) and run `uv venv --python 3.13` (which is the version of Python I used when writing these notebooks, as it's proven, stable, and there are no package issues)

2. Open any of the Jupyter notebooks. To keep things simple, you might want to start with [demo1](ccar-f-demos/demo1/agent_loop.ipynb)

3. Execute the first Python cell (which does the `uv pip install`)
    * If you do not already have the Python + Jupyter VS Code extensions installed, a prompt will appear in the the VS Code Command Center at the top of the screen (i.e. the search text field in the middle of the top of the window) asking you to install the extension.

4. Re-run the first Python cell in the notebook. In the VS Code Command Center select **Python Environments** and choose the venv which you created — it should be called something like `claude-exam-prep-sample-code (3.13.9) (Python 3.13.9) .venv/bin/python`
    * You'll probably also be asked to install `ipykernel` and `pip` — go ahead and install those

5. We're almost done. Finally, create a `.env` file in the root of the repo and specify your Anthropic API key.
    * You can find an example `.env.sample` file in the root of the repo.
    * Note, an Anthropic API key is totally separate to a consumer Claude AI subscription. You need to sign-up for a key (and submit billing information) at the Claude Platform: https://platform.claude.com

6. Have fun :)