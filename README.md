# warrior-bot
![Lint](https://github.com/AWS-WSU/warrior-bot/actions/workflows/lint.yml/badge.svg)

Terminal assistant for Wayne State University students.

## Welcome!
If you're here to contribute, skip ahead to [Getting Started](#development). If you just want to try it out, follow the steps below!

## Installation
For now, install and run the program using the following command from the root directory. We hope to come out with our pilot version in the near future which will give you access via `pip`, `uv` and `poetry`.

```bash
pip install -e .
```

## Usage

```bash
warrior-bot where is panda express
warrior-bot what is the wifi name
warrior-bot --help
```

## Requirements
- Python 3.10+
- Access to a terminal
  - Recommended
    - [Ghostty](https://ghostty.org/)
    - [Alacritty](https://alacritty.org/)
    - [Kitty](https://sw.kovidgoyal.net/kitty/binary/)
    - [WezTerm](https://wezterm.org/index.html)
   
If you're on MacOS, we also recommend [iTerm2](https://iterm2.com/)
## Development

### Getting Started
Read the [Contribution Setup and Guidelines](https://aws-wsu.github.io/warrior-bot/CONTRIBUTING/) to get started.

#### Quick Setup
1. Clone the repo
2. Setup and Activate your Virtual Environment
3. ```bash
   pip install pre-commit
   pre-commit install
   ```
4. Create your branch, develop your bug fix, feature or other contribution
5. Open PR and a reviewer will approve your additions or request changes/
6. Optionally, you may run `pre-commit run --all-files` to run checks manually before pushing your changes. 
