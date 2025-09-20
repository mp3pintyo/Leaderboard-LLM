# Contributing to LLM Leaderboard

Thank you for your interest in contributing to the LLM Leaderboard project! This document provides guidelines for contributing to the project.

## Development Setup

### Prerequisites
- Python 3.10 or higher
- Git
- Virtual environment (recommended)

### Local Development
1. **Clone the repository**
   ```bash
   git clone https://github.com/mp3pintyo/Leaderboard-LLM.git
   cd Leaderboard-LLM
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database**
   ```bash
   python database.py
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   Open http://localhost:5000 in your browser

## Contributing Guidelines

### Code Style
- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise

### Commit Messages
- Use clear, descriptive commit messages
- Start with a capital letter
- Use present tense ("Add feature" not "Added feature")
- Include context in the body if needed

Example:
```
Add filter persistence to session storage

- Store filter preferences in Flask session
- Update templates to use session-based filter state
- Add API endpoints for filter settings management
```

### Pull Requests
1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Test your changes**
   ```bash
   pytest
   ```
5. **Commit your changes**
6. **Push to your fork**
7. **Create a Pull Request**

### Testing
- Add tests for new functionality
- Ensure all existing tests pass
- Run tests before submitting PR:
  ```bash
  pip install -r tests/requirements-test.txt
  pytest
  ```

## Project Structure

```
Leaderboard-LLM/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── database.py           # Database operations
├── requirements.txt      # Python dependencies
├── data/                 # Sample data and templates
├── docs/                 # Documentation
├── eval/                 # Metrics computation
├── scripts/              # Utility scripts
├── templates/            # HTML templates
├── tests/                # Test files
└── README.md            # Project documentation
```

## Feature Areas

### Current Features
- **Leaderboard Display**: Customizable column views
- **Advanced Filtering**: Provider, task group, language, etc.
- **Settings Management**: Column and filter preferences
- **Side-by-Side Comparison**: Model output comparison
- **Data Import**: Excel/CSV import functionality
- **Quality Score System**: 0-10 human evaluation scoring

### Areas for Contribution
- **New Metrics**: Additional evaluation metrics
- **UI Improvements**: Enhanced user interface
- **Export Features**: Data export capabilities
- **API Enhancements**: Additional API endpoints
- **Performance**: Optimization and caching
- **Documentation**: Tutorials and guides
- **Testing**: Increased test coverage

## Issue Reporting

When reporting issues, please include:
- **Environment**: Python version, OS, browser
- **Steps to reproduce**: Clear reproduction steps
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Screenshots**: If applicable
- **Error messages**: Full error text

## Questions and Support

- **Issues**: Use GitHub Issues for bugs and feature requests
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: Check the README.md and docs/ folder

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project.

Thank you for contributing! 🚀