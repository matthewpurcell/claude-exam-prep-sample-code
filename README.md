# claude-exam-prep-sample-code

## Demos

| Demo | Topic | How to run it |
|---|---|---|
| [demo1](ccar-f-demos/demo1/agent_loop.ipynb) | Anthropic SDK: manually managed agent loop | Notebook — needs the venv and an API key |
| [demo2](ccar-f-demos/demo2/hooks.ipynb) | Claude Agent SDK: `PreToolUse` and `PostToolUse` hooks | Notebook — needs the venv and an API key |
| [demo3](ccar-f-demos/demo3/tool_choice.ipynb) | Anthropic SDK: `tool_choice` | Notebook — needs the venv and an API key |
| [demo4](ccar-f-demos/demo4/README.md) | Path-scoped rules with `.claude/rules/` | Claude Code in VS Code — no setup |
| [demo5](ccar-f-demos/demo5/README.md) | Skill frontmatter: `context: fork`, `allowed-tools`, `argument-hint` | Claude Code in VS Code — no setup |
| [demo6](ccar-f-demos/demo6/README.md) | Anthropic SDK: enforcing a JSON schema with structured outputs | Notebook — needs the venv and an API key |

Demos 1, 3 and 6 use the Anthropic SDK directly against the Messages API. Demo 2
uses the Claude Agent SDK — the Claude Code harness as a library. Demos 4 and 5
are the Claude Code harness itself. Three layers, six demos.

Demos 1–3 and 6 are Jupyter notebooks — follow the setup below. Demos 4 and 5 run
in a Claude Code session in VS Code and need no Python environment and no API key;
each has its own README with the steps.

## How to run

It is reccomended to run these notebooks in VS Code.

1. Open the notebook that you want to run.

2. Execute the first Python cell.
    * If you do not already have the Python + Jupyter extensions installed, a prompt will appear in the the Command Center at the top of the screen (i.e. the search looking text field in the middle of the top of the window). Install these extensions.

4. It is reccomended to run the notebooks in an isolated Python environment to make it more sane to manage the dependencies which will be installed.
    * I reccomend using `uv` as its fast and a much neater solution
    * If you do not have `uv` installed, follow the instructions here: https://docs.astral.sh/uv/getting-started/installation/
    * Once `uv` is installed, open a Terminal window in VS Code and ensure you are in the repo directory (`claude-exam-prep-sample-code`) and run `uv venv --python 3.13` (which is the version of Python I used when writing these notebooks, as it's proven and stable)

5. Re-run the Python cell in the notebook and in the Command Center select **Python Environments** > and choose the venv, it should be called something like `claude-exam-prep-sample-code (3.13.9) (Python 3.13.9) .venv/bin/python`
    * You'll probably be asked to install the ipykernel and pip, so go ahead and install those

6. Create a `.env` file in the root of the repo and specify your Anthropic API key

7. You should be good to go