# Agents

Use these project-specific defaults when making future changes:

- Run tests with `pytest`.
- Use `tox` to run the full test matrix across supported Python versions.
- Keep `core-requirements.txt` for runtime dependencies and `requirements.in` for test and development dependencies.
- Regenerate `requirements.txt` from `requirements.in` with `tox -e compile`. Use `tox -e compile -- --upgrade` to upgrade dependencies to the latest compatible versions.
- When changing supported Python versions, keep `tox.toml`, the GitHub Actions workflow, `setup.py` trove classifiers, and `.python-version` in sync.
- Keep `.python-version` set to the lowest supported Python version so Dependabot and single-version tooling pick it up correctly.
- Keep `base_python` in the `compile` environment in `tox.toml` set to the lowest supported Python version so that `tox -e compile` works correctly.
- When changing supported Python versions, recompile `requirements.txt` with `tox -e compile -- --upgrade` to ensure compatible dependency versions are used.
