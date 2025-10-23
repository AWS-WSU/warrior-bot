# warrior-bot

Terminal assistant for Wayne State University students.

## Install

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

Python 3.10+

## Structure

```
warrior_bot/
  __init__.py
  cli.py
```

## Development

### Getting Started

1. Clone the repository
2. Create a virtual environment: `python3 -m venv venv`
3. Activate it: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
4. Install in editable mode: `pip install -e .`
5. Run: `warrior-bot <your query>`

### Project Structure

```
warrior-bot/
├── warrior_bot/           # Main package
│   ├── __init__.py       # Package metadata
│   └── cli.py            # CLI entry point
├── setup.py              # Package configuration
├── pyproject.toml        # Modern Python packaging
├── requirements.txt      # Dependencies
└── README.md            # This file
```

### Extending

Add new modules in `warrior_bot/`:
- Create your feature modules (e.g., `data.py`, `search.py`, etc.)
- Import and use them in `cli.py`
- Keep it simple and readable following best coding practices and conventions.

## Submitting Changes

1. Create a new branch: `git checkout -b feature/your-feature`
2. Make your changes and commit them: `git commit -m 'Add your feature'`
3. Push to the branch: `git push origin feature/your-feature`
4. Open a pull request

## Running Locally

After installing with `pip install -e .`, any changes to the code will be reflected immediately—no reinstall needed.
