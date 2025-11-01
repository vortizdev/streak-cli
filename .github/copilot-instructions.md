## Streak CLI — Quick AI guidance

This file gives focused, actionable guidance for an AI coding agent to be immediately productive in this repository.

Highlights
- Project is a small CLI habit-tracker. Key code lives in `src/streak/`.
- Tests drive expected behaviour (see `tests/`). Integration tests run the module as `-m src.streak`.
- Python requirement: >= 3.12 (see `pyproject.toml`). Dependency: `rich`.

Quick dev commands
- Install: `pip install -r requirements.txt` (use a venv).
- Run unit tests: `python -m pytest -v`.
- Run integration CLI locally: from project root set env var `STREAK DATA` (note the space) and run:
  - `python -m src.streak add "My Task"`
  - `python -m src.streak list`

Important repository-specific patterns and conventions
- Package/module path: code is located under `src/streak/` and is invoked as `src.streak` in tests and CLI (i.e. `-m src.streak`). Prefer editing files under `src/streak/`.
- Entry point inconsistency: `pyproject.toml` declares an installed script `streak = "streak.__main__:main"`, but local development and tests use `src.streak` — prefer using `python -m src.streak` for local runs and tests.
- Data persistence: `data.json` is plain JSON in the project root by default. The code reads/writes a JSON list of objects via `src/streak/storage.py`.
- Environment control: the CLI reads the data path from the environment variable named exactly `STREAK DATA` (with a space). Integration tests set this env var; follow that convention when running locally or in CI.

Key files and what they show (jump-to examples)
- `src/streak/__main__.py` — CLI argument parsing (argparse), table output using `rich`, default data path resolution, and how commands are invoked.
- `src/streak/commands.py` — business logic: `add_habit`, `mark_done`, `get_habits`, `list_habits`. Note: `mark_done` updates `last_done`, `done`, and `streak`.
- `src/streak/storage.py` — simple `load_data`/`save_data` wrappers around JSON file IO. Tests expect `load_data` to create the file if missing.
- `tests/` — unit & integration tests demonstrate expected CLI behaviour and useful examples (tmp_path usage, simulating dates by editing stored JSON).

Implementation notes & gotchas to preserve
- Tests run the package as `-m src.streak` and import `src.streak.*`. When changing import paths, update tests accordingly.
- Watch for small inconsistencies that tests rely on:
  - Environment variable is `STREAK DATA` (space) — use the exact name.
  - `commands.list_habits` returns a string joined using `"/n"` (typo) — tests check for substrings so be conservative when changing behaviour; prefer fixing only if tests are updated.
  - `__main__.py` imports `from src.streak import commands, __version__` — keep relative import style used across files.

How to add a new CLI command (example)
1. Add a new subparser in `src/streak/__main__.py` (follow argparse subparsers pattern).
2. Implement the operation in `src/streak/commands.py` and call `storage.load_data`/`save_data` as needed.
3. Add unit tests in `tests/` using `tmp_path` or update integration test to exercise `python -m src.streak` with `STREAK DATA` env var.

Testing & validation
- Use pytest for unit tests. Integration tests spawn subprocesses and expect a working `python -m src.streak` invocation from project root.
- After changes, run: `python -m pytest -q` and fix failures. CI (if added) should mimic the `STREAK DATA` env var usage.

When unsure
- Prefer small, test-driven edits. Use the tests in `tests/` as the source of truth for behaviour.
- If changing the package import layout (e.g., moving to `streak` instead of `src.streak`), update `pyproject.toml` and all tests together.

If you modify persistent formats (JSON keys), update tests that read/write `data.json` (they may directly mutate `last_done` and `streak`).

Ask for clarification if any intended behaviour is unclear (for example, desired handling of marking the same day twice or resetting streaks).
