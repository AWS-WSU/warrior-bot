# Contributing to `warrior-bot`

Thank you for your interest in contributing to `warrior-bot`. This project is currently maintained by Stefan Barbu and supervised by Akrm Al-Hakimi.

This guide will steer you through the typical process of contributing to any project, as well as some specifics to `warrior-bot`.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Pre-requisite Knowledge](#pre-requisite-knowledge)
- [How to Contribute](#how-to-contribute)
- [Setting Up Your Environment](#setting-up-your-environment)
- [Development Workflow](#development-workflow)
- [Style and Quality Standards](#style-and-quality-standards)
- [Testing](#testing)
- [Commit Messages](#commit-messages)
- [Pull Requests](#pull-requests)
- [Getting Help](#getting-help)

# Code of Conduct
All contributors are expected to follow our [Code of Conduct](./CODE_OF_CONDUCT.md). Keep interactions respectful and professional.

**_Note: AI is fine and in some cases encouraged but we will outright reject any low effort, clearly slop code changes. 
Please ensure you put effort into changes made to this project, even if you used AI to help write them._**

## Pre-requisite Knowledge
While this project is welcoming to anyone curious or eager to be involved in a given project, it is still expected to 
understand a short list of concepts/skills in order to comfortably contribute to `warrior-bot`.

- Basic programming concepts (Python and Shell are the only two languages that will be used in `warrior-bot` for now)
  - You should know how to write for loops, if statements, conditionals, etc. 
  - Debugging is a non-starter. You should know how to setup your own environment, run your code, and make changes based off of the output of that code.
  - You should know how to use an IDE and when working on `warrior-bot`, you should definitely get comfortable with using the terminal.
- Basic Git and Github knowledge 
  - You should know the following with little to no help:
    - **Git**
      - How to clone a repository 
      - How to pull, push and rebase/fetch changes from a branch 
      - How to open a new branch and push it to the repo's upstream
      - How to checkout branches
      - How to commit changes and write clean commit messages (see [Commit Messages](#commit-messages))
    - **GitHub**
      - How to Open a PR (Pull Request) 
      - How to link a PR or Commit to an issue (Not mandatory, but helpful)
      - How to submit an issue 

These are skills I would probabaly expect a Sophomore/Junior to be comfortable with, but even if you aren't, it takes very little 
discipline and time to learn them. Thus, why this project is open to developers of all experience levels.


## How to Contribute

You can contribute by:
- Reporting bugs
- Suggesting enhancements
- Improving documentation
- Submitting code changes

Before starting work on an issue:
1. Check open issues
2. Comment on an issue to ask if it’s available.
3. Wait for a maintainer to confirm or assign it.


## Setting Up Your Environment

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/<your-username>/warrior-bot.git
   cd warrior-bot
   ```
2. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:

   ```bash
   pip install -e .
   pip install -r requirements.txt
   ```
4. Install pre-commit hooks -> This is important for running checks automatically before pushing changes:

   ```bash
   pip install pre-commit
   pre-commit install
   ```
   - You can optionally decide to manually run checks using `pre-commit run --all-files`


## Development Workflow

We use a simplified GitHub Flow:

1. Create a new branch:

   ```bash
   git checkout -b feature/short-title
   ```
2. Make your changes; example:
   ```python
   # warrior_bot/cli.py

   import click

   @click.command()
   def hello():
     """Simple test command"""
     click.echo("Hello from Warrior-Bot!")
   ```
3. Test your changes
    ```bash 
    warrior-bot hello 
    ```
4. Commit with a clear message:

   ```bash
   git commit -m "feat: short summary of change"
   ```
5. Push your branch and open a pull request on GitHub to `master`.

## Style and Quality Standards

* Follow [PEP 8](https://peps.python.org/pep-0008/).
* Use `black` for formatting and `isort` for import order.
* Run `flake8` to check for style issues.
* Include docstrings for public functions and modules.

These checks also run automatically via GitHub Actions and pre-commit. If you wanted to run them manually, you can use the following commands:

```bash
  black .            # runs formatting on all files 
  isort .            # sorts imports 
  flake8 warrior_bot # style checks 
```


## Testing

Use `pytest` for testing:

```bash
pytest
```

All tests must pass before a pull request is merged. Any changes to a existing feature require that the tests still pass or new ones are made based on your changes. 
Most new features require unit tests for any major components. 

## Commit Messages

Use conventional commit types:

* `feat:` for new features
* `fix:` for bug fixes
* `docs:` for documentation changes
* `refactor:` for code improvements
* `test:` for test-related updates
* `chore:` for maintenance or config updates

Example:

```
feat: add campus events command
```

## Pull Requests

Pull requests should:

* Target the `master` branch.
* Pass all linting and test checks.
* Contain clear, descriptive commit messages.
* Be scoped to a single feature or fix.

Maintainers will review PRs and may request changes before merging.


# Getting Help

If you need help:

* Open a issue on GitHub or contact the maintainers directly (Stefan Barbu and Akrm Al-Hakimi).
* Utilize your own resources to teach yourself any processses or concepts you aren't familiar with.
