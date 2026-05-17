# Contributing to Web Scrapping Suite

Thank you for your interest in contributing! This document provides guidelines and instructions.

## Code of Conduct

We are committed to providing a welcoming and inspiring community. All contributors must adhere to our code of conduct:
- Be respectful and constructive
- Report issues responsibly
- Respect others' time and effort

## Getting Started

### 1. Fork & Clone
```bash
git clone https://github.com/YOUR_USERNAME/Web_Scrapping.git
cd Web_Scrapping
```

### 2. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

### 3. Set Up Development Environment
```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows

pip install -r requirements.txt
pip install flake8 pytest  # Development tools
```

## Development Guidelines

### Code Style
- Follow PEP 8 standards
- Use meaningful variable names
- Keep functions focused and testable
- Add docstrings to functions and classes
- Maximum line length: 100 characters

### Commit Messages
Use semantic commit messages:
```
feat: Add new feature description
fix: Fix bug in module
docs: Update documentation
refactor: Improve code structure
test: Add tests for feature
chore: Update dependencies
```

### Testing
Before submitting a pull request:
```bash
# Run linter
flake8 *.py

# Test your changes
python -m pytest tests/
```

## Submitting Changes

### 1. Make Your Changes
- Write clean, well-documented code
- Test thoroughly
- Keep commits atomic and meaningful

### 2. Push to Your Fork
```bash
git push origin feature/your-feature-name
```

### 3. Create a Pull Request
- Clear title describing the change
- Detailed description of what was changed and why
- Reference any related issues (e.g., "Closes #42")
- Ensure CI passes

## Reporting Issues

When reporting bugs:
1. Use a clear, descriptive title
2. Describe the expected vs. actual behavior
3. Provide minimal code to reproduce
4. Include Python version and OS
5. Attach error messages/logs if applicable

## Feature Requests

When suggesting features:
1. Use a clear title
2. Provide detailed description
3. Explain use case and benefits
4. Provide examples if possible

## Documentation

- Keep README.md updated with new features
- Add docstrings to new functions
- Update CONTRIBUTING.md as needed
- Include inline comments for complex logic

## Licensing

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to open an issue for any questions or discussions.

---

Happy contributing! 🚀
