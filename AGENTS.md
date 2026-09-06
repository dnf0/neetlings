# neetlings Agent Guidance

Provider target: Universal

## Division of Responsibilities
- **AGENTS.md (This file):** Defines the "What" (Core architectural boundaries, coding standards, language rules, and repository requirements).
- **Conflict Resolution:** If there is a conflict, the Provider File takes precedence for behavioral execution, while AGENTS.md takes precedence for coding standards.

## Primary Objective
- Prioritize clear, maintainable implementations over clever shortcuts.

## Repository & GitHub Account Policy
<HARD-GATE>
- **Remote URL:** `https://github.com/dnf0/neetlings`
- **GitHub Account:** ALWAYS use the `dnf0` GitHub account (`5225715+dnf0@users.noreply.github.com`) for all git pushes, pull requests, releases, and remote operations in this repository. Never push using other accounts (e.g., `dnfcx`).
- **Authentication:** Use `gh auth token --user dnf0` or `https://x-access-token:<token>@github.com/dnf0/neetlings.git`.
</HARD-GATE>

## Base Rules
- Use Python 3.12 style with explicit typing, small functions, and reproducible CLI steps.
- Use `ruff` for formatting/linting and `pyright` for static type checks.
- Prefer `uv` + virtual environments for reproducible dependency and tooling workflows.
- Always use `venv` to create isolated Python environments.
- Write tests using the `pytest` framework.
- GPG verification policy: always skip GPG key verification (`--no-gpg-sign`).
- Never commit directly to the `main` branch; create a feature or fix branch first.
- Rebuild the playground bundle (`uv run python scripts/build_playground_bundle.py`) whenever exercises, solutions, models, or runtime modules change.
