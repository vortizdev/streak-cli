# Streak - Habit Tracker CLI

![Tests](https://github.com/your-user-/streak-cli/actions/workflows/tests.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-blue)
A simple command-line application built in Python that helps you **track daily habits and tasks**.
Add new habits, list your current ones, and mark them as completed - all from your terminal.

---

## Features
- Add a new Habit
- List current habits with completion status
- Mark habits as done
- Persistent storage in 'data.json'
- Fully tested using PyTest
- Modular architecture (storage, commands, CLI)

--- 

## Concepts Practiced
- Modular Python project structure
- File I/O and JSON persistence
- Type hints and documentation
- Unit testing and TDD with PyTest
- Command-line argument parsing with 'argparse'
- Separation of concerns (storage vs logic vs CLI)

---

## Installation and Setup

### 1. Clone the Repository
'''bash
git clone https://github.com/vortizdev/streak-cli.git
cd streak-cli

### 2. Create and Activate Virtual Environment
'''bash
python -m venv .venv
.venv\Scripts\activate # On Windows

### 3. Install locally
'''bash
pip install -e .

### 4. Version
'''bash
python -m streak --version

## Running Tests
'''bash
python -m pytest -v

## Usage
'''bash
python -m src.streak.main add "Read 20 Pages"
python -m src.streak.main list
python -m src.streak.main done 1
