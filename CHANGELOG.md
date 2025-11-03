# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- (placeholder) Add anything merged to main that isn't released yet.

## [0.1.0] -  2025-11-03
### Added
- Initial CLI with 'add', 'list', 'done' commands.
- JSON persistence ('storage.py') using 'pathlib' and 'json'.
- Streak tracking with 'datetime' and 'last_done'/'streak' fields
- Rich-powered table output (ASCII-safe for windows).
- 'STREAK_DATA' env override for tests.
- Packaging via 'pyproject.toml' with console script: 'streak'.
- '--version' flag sourced from 'streak.__init__.__version__'.
- Unit and integration tests with pytest.
- README setup and usage instructions.

### Fixed
- Windows console emoji UnicodeEncondeError by removing emojis and disabling 'Console(emoji=False)'.