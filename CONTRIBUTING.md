# Contributing to OmniPack

Thank you for your interest in contributing to OmniPack! We welcome contributions from the community.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone git@github.com:your-username/ulauncher-omnipack.git`
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test thoroughly
6. Commit with clear messages: `git commit -m "feature: description of changes"`
7. Push to your fork and submit a pull request

## Code Standards

### Python Code
- Follow PEP 8 style guidelines
- Use type hints for all function signatures
- Document public methods with Google-style docstrings
- Format code with Black
- Lint with Flake8

### Example Function
```python
def example_function(param: str) -> str:
    """Brief description of function.
    
    Args:
        param: Description of parameter
        
    Returns:
        Description of return value
    """
    return param
```

## Best Practices

- Handle exceptions gracefully - never crash the extension
- Use `extension.preferences['key']` to access user settings
- Avoid blocking I/O in event handlers
- Use `os.path.dirname(__file__)` instead of hardcoding paths
- Use logging module instead of print statements
- Check for external tool availability with `shutil.which()`

## Testing

- Write unit tests for new features
- Test with different input types (empty, special characters, etc.)
- Verify error handling works as expected
- Test with various Ulauncher versions if possible

## Commit Guidelines

- Keep commits atomic and self-contained
- Use lowercase commit messages unless otherwise needed
- Reference issues when applicable
- Follow the format: `type: description`
  - `feature:` for new features
  - `fix:` for bug fixes
  - `docs:` for documentation
  - `refactor:` for code refactoring

## Pull Request Process

1. Ensure your code follows the standards above
2. Update README.md if adding new features
3. Add tests for new functionality
4. Provide a clear description of changes
5. Link related issues if applicable

## Reporting Issues

When reporting bugs, please include:
- Ulauncher version
- Python version
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error logs if available

## Questions?

Feel free to open an issue for questions or discussions about the project.

Thank you for contributing!
