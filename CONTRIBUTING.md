# Contributing to MD Lakehouse Template

Thank you for your interest in improving this course template!

## How to Contribute

### Reporting Issues

- Use GitHub Issues for bug reports
- Provide clear reproduction steps
- Include environment details (OS, Python version)

### Proposing Enhancements

- Open a GitHub Discussion first to discuss the idea
- Get feedback before implementing
- Ensure alignment with educational goals

### Code Contributions

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`make test`)
6. Run linting (`make lint`)
7. Commit with clear messages
8. Push and create a Pull Request

### Code Standards

- Follow PEP 8 style guide
- Use type hints where appropriate
- Add docstrings to public functions
- Keep functions focused and modular
- Write tests for new code (aim for >70% coverage)

### Testing

```bash
# Run all tests
make test

# Run specific test file
pytest tests/test_generator_reproducible.py -v

# Check coverage
pytest --cov=src/md_lakehouse --cov-report=html
```

### Documentation

- Update README if adding features
- Update docstrings for API changes
- Add examples for new functionality
- Keep documentation clear and concise

## Areas for Contribution

High-value contributions:

1. **Additional Models**: New ML use cases (recommendations, fraud detection)
2. **Improved Generators**: More realistic business logic
3. **Better Visualizations**: Enhanced notebooks with better plots
4. **Performance**: Optimization of Spark jobs
5. **Documentation**: Tutorials, examples, translations
6. **Testing**: More comprehensive test coverage

## Questions?

- GitHub Discussions for general questions
- GitHub Issues for bugs
- Email course maintainer for academic questions

Thank you for contributing! 🎓
