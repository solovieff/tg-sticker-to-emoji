# Contributing to Sticker to Emoji Converter

First off, thank you for considering contributing! 🎉

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce**
- **Expected vs actual behavior**
- **Screenshots** (if applicable)
- **Environment details** (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear title and description**
- **Use case** - why would this be useful?
- **Possible implementation** (if you have ideas)

### Pull Requests

1. **Fork** the repo
2. **Create a branch** from `main`
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Test thoroughly**
5. **Commit** with clear messages
   ```bash
   git commit -m "Add amazing feature"
   ```
6. **Push** to your fork
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/tg-sticker-to-emoji.git
cd tg-sticker-to-emoji

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Add your credentials to .env
```

## Coding Guidelines

### Python Style

- Follow [PEP 8](https://peps.python.org/pep-0008/)
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and small

### Code Quality

- **Type hints** where appropriate
- **Error handling** - catch and handle exceptions properly
- **Logging** - use appropriate log levels
- **Comments** - explain *why*, not *what*

### Testing

Before submitting:

```bash
# Test your changes
python -m sticker_to_emoji TestPackName -l 5

# Check for common issues
python -m py_compile src/sticker_to_emoji/*.py
```

## Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- First line: brief summary (50 chars or less)
- Reference issues: "Fixes #123" or "Closes #456"

Examples:
```
Add support for WEBM animated stickers
Fix SSL certificate verification error
Update README with installation steps
```

## Project Structure

```
tg-sticker-to-emoji/
├── src/
│   └── sticker_to_emoji/
│       ├── __init__.py
│       ├── __main__.py
│       └── converter.py
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── setup.py
```

## What to Contribute

### Good First Issues

Look for issues labeled `good first issue`:
- Documentation improvements
- Adding examples
- Fixing typos
- Improving error messages

### Areas for Improvement

- **Performance** - optimize image processing
- **Features** - support for video stickers
- **UX** - better progress indicators
- **Tests** - add unit tests
- **Documentation** - improve guides and examples

## Questions?

- 💬 Open a [discussion](https://github.com/yourusername/tg-sticker-to-emoji/discussions)
- 🐛 Check [existing issues](https://github.com/yourusername/tg-sticker-to-emoji/issues)
- 📧 Contact maintainers

## Code of Conduct

Be respectful, inclusive, and considerate. We're all here to build something cool together! 🚀

---

Thank you for contributing! 🙏
