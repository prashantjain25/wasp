# Contributing to wasp

wasp is an open source project under the MIT License. We welcome contributions from the community.

## Contributor License Agreement

By submitting a pull request, you agree to the following terms:

- Your contributions are submitted under the MIT License that covers this project.
- You grant the project maintainers the right to use, modify, and distribute your contributions as part of wasp.
- You represent that you have the legal authority to grant these rights.

If this is your first contribution, you will need to acknowledge these terms when the pull request is created.

## Getting Started

1. Fork the repository.
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/wasp.git
   ```
3. Set up the development environment:
   ```bash
   cd wasp
   python3 -m pytest tests/
   ```
4. Create a branch for your changes:
   ```bash
   git checkout -b my-feature
   ```

## Code Conventions

- **Single file philosophy.** The main CLI (`wasp`) is a single Python file. New features should be self-contained before extracting to separate modules.
- **String concatenation** over f-strings for user-facing messages to avoid shell escaping issues.
- **Arrow-key menus** for all interactive selection. No fzf, no external pickers.
- **Exception safety.** Every error path must be caught. The REPL never crashes.
- **Tests** accompany all new commands and features.

## Testing

Run the test suite before submitting:

```bash
python3 -m pytest tests/ -v
```

All tests must pass. Add tests for new functionality.

## Commit Guidelines

- Use present tense ("Add feature" not "Added feature").
- Keep commits focused on a single change.
- Reference issues when applicable.

## Pull Request Process

1. Ensure all tests pass.
2. Update the README.md if your change affects usage.
3. Keep the diff minimal - no unrelated formatting changes.
4. A maintainer will review your submission within a reasonable timeframe.

## Code of Conduct

Be respectful, constructive, and professional. Harassment or abusive behavior will not be tolerated.

## Questions?

Open a GitHub Issue for questions, bug reports, or feature requests.
