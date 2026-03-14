# Personal Finance Tracker

A CLI tool to track your income and expenses from the terminal.

## Installation
```bash
git clone https://github.com/Bedran0/personal-finance.git
cd personal-finance
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

## Usage
```bash
# Add a record
finance add

# Show balance
finance summary

# Spending by category
finance categories
finance categories --type income

# Monthly breakdown
finance monthly
```

## Project Structure
```
src/finance/
├── tracker.py   # Core logic
└── cli.py       # CLI interface
tests/
└── test_tracker.py
```

## Tech Stack

- [Typer](https://typer.tiangolo.com/) — CLI framework
- [Rich](https://rich.readthedocs.io/) — terminal formatting
- [pytest](https://pytest.org/) — testing
