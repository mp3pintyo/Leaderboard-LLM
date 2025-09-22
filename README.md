# LLM Leaderboard

[![GitHub](https://img.shields.io/badge/GitHub-mp3pintyo%2FLeaderboard--LLM-blue)](https://github.com/mp3pintyo/Leaderboard-LLM)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

A Flask-based web application for comparing Large Language Model (LLM) performance across different tasks with side-by-side output comparison and comprehensive leaderboard views.

## Features

- 🏆 **Interactive Leaderboard** - Compare models across multiple metrics with filtering
- ⚙️ **Customizable Columns** - Personalize leaderboard view with column selection settings
- 🔄 **Side-by-Side Comparison** - View model outputs for the same task simultaneously  
- 📊 **Detailed Analytics** - Per-model and per-task performance breakdowns
- � **Task Group Performance Charts** - Visual comparison charts on model detail pages
- �📁 **Excel Import** - Easy data import from Excel/CSV files with configurable mapping
- 🔍 **Advanced Filtering** - Filter by open source, task groups, languages, metrics, and more
- 📈 **Quality Score System** - Human evaluation scoring (0-10) with research task exclusion
- 🌐 **REST API** - Full API access for programmatic usage
- 📱 **Responsive UI** - Modern Bootstrap-based interface

## Quick Start

### Prerequisites

- Python 3.10 or higher
- PowerShell (Windows) or bash (Linux/macOS)

### Installation & Setup

1. **Clone the repository**
```bash
git clone https://github.com/mp3pintyo/Leaderboard-LLM.git
cd Leaderboard-LLM
```

2. **Create and activate virtual environment**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```powershell
pip install -r requirements.txt
```

4. **Initialize the database**
```powershell
python database.py
```

5. **Import sample data (optional)**
```powershell
python scripts\import_excel.py data\sample.xlsx
```

6. **Start the application**
```powershell
$env:FLASK_APP = "app.py"
flask run --host=0.0.0.0 --port=5000
```

7. **Open in browser**
```
http://localhost:5000
```

## Project Structure

```
d:\AI\Leaderboard-LLM-v2\
├── app.py                     # Main Flask application
├── database.py                # Database schema and operations
├── config.py                  # Configuration settings
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── pytest.ini                # Test configuration
├── data/
│   ├── mapping.json          # Column mapping for Excel import
│   ├── sample.xlsx           # Sample data file
│   └── results.db            # SQLite database (created on init)
├── scripts/
│   ├── import_excel.py       # Excel/CSV import script
│   └── generate_sample_data.py # Sample data generator
├── templates/
│   ├── base.html             # Base template
│   ├── index.html            # Main leaderboard page
│   ├── side_by_side.html     # Comparison page
│   └── model.html            # Model details page
├── static/                   # Static assets (CSS, JS, images)
├── eval/
│   └── compute_metrics.py    # Metrics computation (mock/real)
└── tests/
    ├── test_app.py           # Unit tests
    └── requirements-test.txt # Test dependencies
```

## Usage Guide

### 1. Database Operations

**Initialize database and populate with default models:**
```powershell
python database.py
```

**Check database status:**
```powershell
python -c "from database import DatabaseManager; db = DatabaseManager(); print('Models:', len(db.get_models())); print('Tasks:', len(db.get_tasks()))"
```

### 2. Data Import

**Import Excel/CSV data:**
```powershell
# Basic import with metrics computation
python scripts\import_excel.py data\sample.xlsx

# Dry run (validation only)
python scripts\import_excel.py data\sample.xlsx --dry-run

# Skip metrics computation
python scripts\import_excel.py data\sample.xlsx --no-metrics

# Custom column mapping
python scripts\import_excel.py your_data.xlsx --mapping data\custom_mapping.json
```

**Column mapping format (mapping.json):**
```json
{
  "task_id": "task_id",
  "task_name": "task_name", 
  "prompt_text": "prompt_text",
  "task_group": "task_group",
  "model_key": "model_key",
  "output_text": "output_text",
  "tokens": "tokens",
  "length": "length"
}
```

### 3. Web Interface

**Main Pages:**
- `/` - Leaderboard with filtering options
- `/side-by-side` - Side-by-side model comparison  
- `/settings` - Customize leaderboard column display
- `/model/<model_key>` - Detailed model performance with task group charts

**Column Customization:**
The Settings page allows you to:
- Toggle columns on/off (Rank, Model, Actions are required)
- Preview your customized leaderboard layout
- Save preferences for your session
- Reset to default column configuration

**Available Columns:**
- Model information (Provider, Open Source, Parameters, Release Date)
- Performance metrics (Quality Score, ROUGE-L, BERTScore)
- Capabilities (Reasoning, Image Input, Context Window, Tags)
- Statistics (Tasks completed, Average tokens)

**Filtering Options:**
- Open Source (Yes/No)
- Provider selection
- Task Group (reasoning, coding, language_understanding, etc.)
- Language support (English, Hungarian, German, French, Spanish)
- Tag filtering (instruction, reasoning, general, coding, multimodal)
- Reasoning capability (Yes/No)
- Image Input support (Yes/No)
- Parameter count ranges (min/max B)
- Context window ranges
- Release date ranges
- Sort by different metrics

### 4. API Endpoints

**Model Information:**
```powershell
# Get all models
curl http://localhost:5000/api/models

# Filter models
curl "http://localhost:5000/api/models?open_source=true&tag=instruction"

# Get specific model details
curl http://localhost:5000/api/model/llm-001
```

**Leaderboard Data:**
```powershell
# Get leaderboard
curl http://localhost:5000/api/leaderboard

# With filters
curl "http://localhost:5000/api/leaderboard?task_group=reasoning&sort_by=avg_bleu"
```

**Task Data:**
```powershell
# Get all tasks
curl http://localhost:5000/api/tasks

# Get task outputs
curl "http://localhost:5000/api/task/reasoning_001/outputs?models=llm-001,llm-002"
```

**Import Data:**
```powershell
# Upload and import file
curl -X POST -F "file=@data\sample.xlsx" -F "compute_metrics=true" http://localhost:5000/api/import
```

**Statistics:**
```powershell
# Get application statistics
curl http://localhost:5000/api/stats
```

**Settings:**
```powershell
# Save column preferences
curl -X POST -H "Content-Type: application/json" \
  -d '{"enabled_columns":["rank","model","provider","quality_score","actions"]}' \
  http://localhost:5000/api/settings/columns

# Reset to default columns  
curl -X POST http://localhost:5000/api/settings/columns/reset
```

### 5. Testing

**Run all tests:**
```powershell
pip install -r tests\requirements-test.txt
pytest
```

**Run specific test categories:**
```powershell
pytest tests\test_app.py::TestDatabaseManager -v
pytest tests\test_app.py::TestAPIEndpoints -v
pytest tests\test_app.py::TestExcelImporter -v
```

### 6. Development

**Development mode with auto-reload:**
```powershell
$env:FLASK_DEBUG = "True"
$env:FLASK_APP = "app.py"
flask run --host=0.0.0.0 --port=5000
```

**Generate new sample data:**
```powershell
python scripts\generate_sample_data.py
```

**Enable real metrics (optional):**

1. Install additional dependencies:
```powershell
# Uncomment lines in requirements.txt:
# nltk==3.8.1
# rouge-score==0.1.2
# bert-score==0.3.13
# transformers==4.33.2
# torch==2.0.1

pip install nltk rouge-score bert-score transformers torch
```

2. Update config.py:
```python
METRICS_CONFIG = {
    'enable_external_apis': True,
    'mock_metrics': False,
    # ... other settings
}
```

## Configuration

### Model Configuration

Edit `config.py` to add/modify models:

```python
MODELS = {
    'your-model': {
        'name': 'Your Model Name',
        'api_id': 'your-model-api-id',
        'open_source': True,
        'tokenizer': 'your-tokenizer',
        'reasoning': True,
        'languages': ['en', 'hu'],
        'tags': ['instruction', 'general'],
        'provider': 'Your Organization',
        'parameters': '7B'
    }
}
```

### Database Configuration

```python
# Database settings
DATA_DIR = 'data'
DATABASE = 'results.db'
ALLOWED_EXTENSIONS = ['.xlsx', '.csv']
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
```

### Task Groups

Supported task groups (configurable in `config.py`):
- `reasoning` - Logical reasoning tasks
- `coding` - Code generation and programming
- `language_understanding` - Translation, summarization
- `creative_writing` - Creative text generation
- `math` - Mathematical problem solving
- `knowledge_qa` - Knowledge-based Q&A
- `instruction_following` - Following complex instructions

## Data Schema

### Database Tables

**models**: Model metadata
- `id` (INTEGER PRIMARY KEY)
- `model_key` (TEXT UNIQUE) 
- `name` (TEXT)
- `meta` (JSON) - Configuration from config.py

**tasks**: Task definitions
- `task_id` (TEXT PRIMARY KEY)
- `task_name` (TEXT)
- `prompt_text` (TEXT)
- `task_group` (TEXT)

**outputs**: Model responses
- `id` (INTEGER PRIMARY KEY)
- `task_id` (TEXT, FK)
- `model_key` (TEXT, FK)
- `output_text` (TEXT)
- `tokens` (INTEGER)
- `length` (INTEGER)
- `created_at` (TIMESTAMP)

**metrics**: Performance metrics
- `id` (INTEGER PRIMARY KEY)
- `output_id` (INTEGER, FK)
- `metric_name` (TEXT)
- `metric_value` (REAL)

**imports**: Import history
- `id` (INTEGER PRIMARY KEY)
- `source_file` (TEXT)
- `imported_at` (TIMESTAMP)
- `notes` (TEXT)

### Required Excel Columns

Minimum required columns for import:
- `task_id` - Unique task identifier
- `model_key` - Model identifier (must match config.py)
- `output_text` - Model's response/output

Optional columns:
- `task_name` - Human-readable task name
- `prompt_text` - Input prompt/question
- `task_group` - Task category
- `tokens` - Token count
- `length` - Character/word length

## Metrics

The application supports the following metrics:

### Mock Metrics (Default)
- **BLEU** - N-gram overlap based scoring
- **ROUGE-L** - Longest common subsequence
- **BERTScore** - Semantic similarity (simulated)
- **Exact Match** - Binary exact match
- **Semantic Similarity** - Word overlap based
- **Length Ratio** - Output/reference length ratio

### Real Metrics (Optional)
When enabled via configuration:
- **Real BLEU** - Using nltk/sacrebleu
- **Real ROUGE** - Using rouge-score library  
- **Real BERTScore** - Using BERT embeddings
- Custom metrics can be added in `eval/compute_metrics.py`

## Database Management

### Model Configuration Updates

**Adding new models:**
Edit `config.py` and add to the `MODELS` dictionary:

```python
MODELS = {
    'new-model': {
        'name': 'Model Name',
        'open_source': True/False,
        'tokenizer': 'tokenizer-type',
        'reasoning': True/False,
        'languages': ['en', 'hu'],
        'tags': ['tag1', 'tag2'],
        'provider': 'Company Name',
        'parameters': '7B',
        'context_window': '128K',
        'release_date': '2024-01-01',
        'image_input': True/False
    }
}
```

**Update database with new/modified models:**
```powershell
python database.py
```

### Database Reset and Backup

**1. Create Database Backup:**
```powershell
# Create timestamped backup
python backup_restore.py backup

# List available backups
python backup_restore.py list

# Restore from backup
python backup_restore.py restore backup_filename.db
```

**2. Complete Database Reset (⚠️ Deletes Everything):**
```powershell
# Nuclear option - deletes entire database
Remove-Item data\results.db -Force
python database.py
```

**3. Tasks-Only Reset (Keeps Models):**
```powershell
# Interactive reset - keeps models, deletes tasks/outputs/metrics
python reset_tasks.py
```

**4. Selective Task Management:**
```powershell
# Interactive menu for selective deletion
python manage_tasks.py
```

**5. Safe Reset Workflow with Automatic Backup:**
```powershell
# Guided reset process with backup protection
python backup_restore.py
```

### Reset Comparison Table

| Method | Tasks | Outputs | Metrics | Models | Imports | Use Case |
|--------|-------|---------|---------|--------|---------|----------|
| **Complete Reset** | ❌ | ❌ | ❌ | ❌→✅ | ❌ | Fresh start |
| **Tasks Reset** | ❌ | ❌ | ❌ | ✅ | ❌ | New dataset |
| **Selective Delete** | Partial | Partial | Partial | ✅ | ✅ | Fine-tuning |
| **Backup Restore** | ⬅️ | ⬅️ | ⬅️ | ⬅️ | ⬅️ | Undo changes |

### Common Database Operations

**Check database status:**
```powershell
python -c "from database import DatabaseManager; db = DatabaseManager(); models = db.get_models(); tasks = db.get_tasks(); print(f'Models: {len(models)}, Tasks: {len(tasks)}')"
```

**Reimport data after reset:**
```powershell
# After any reset, reimport your data
python scripts\import_excel.py data\sample.xlsx
```

**Verify model configurations:**
```powershell
python -c "from database import DatabaseManager; db = DatabaseManager(); [print(f'{m[\"model_key\"]}: {m[\"name\"]} - Context: {m.get(\"context_window\", \"N/A\")}') for m in db.get_models()]"
```

## Troubleshooting

### Common Issues

**Database locked error:**
```powershell
# Option 1: Use backup system
python backup_restore.py backup
python reset_tasks.py

# Option 2: Complete reset (nuclear option)
Remove-Item data\results.db -Force
python database.py
```

**Import fails with column errors:**
- Check your Excel file has required columns: `task_id`, `model_key`, `output_text`
- Verify `model_key` values match those in `config.py`
- Update `data\mapping.json` if column names differ

**Web interface shows no data:**
```powershell
# Check if data exists
python -c "from database import DatabaseManager; db = DatabaseManager(); print(f'Models: {len(db.get_models())}, Tasks: {len(db.get_tasks())}')"

# If no tasks, import sample data
python scripts\import_excel.py data\sample.xlsx
```

**Model not appearing in lists:**
```powershell
# Update models after config.py changes
python database.py

# Verify model was added
python -c "from database import DatabaseManager; db = DatabaseManager(); models = db.get_models(); print([m['model_key'] for m in models])"
```

**Import is slow or hangs:**
- Use the improved import with progress feedback
- Check database isn't locked by another process
- Use `--dry-run` first to validate data

**VS Code showing template errors:**
- Template errors in `side_by_side.html` are normal (Jinja2 syntax in JavaScript)
- Functionality works correctly despite editor warnings

**Need to start over completely:**
```powershell
# Safe complete reset workflow
python backup_restore.py
# Choose option 'a' for complete reset
```

**Missing dependencies:**
```powershell
pip install --upgrade -r requirements.txt
```

**Port already in use:**
```powershell
# Use different port
flask run --host=0.0.0.0 --port=5001
```

### Performance Tips

- For large datasets, consider chunked imports
- Use `--no-metrics` flag for faster imports during development
- Enable database indexing for large-scale deployments
- Consider using PostgreSQL for production environments

## Contributing

### Adding New Metrics

1. Add metric computation to `eval/compute_metrics.py`
2. Update `config.py` SUPPORTED_METRICS list
3. Add database migration if needed
4. Update templates to display new metric

### Adding New Model Support

1. Add model configuration to `config.py` MODELS dict
2. Run `python database.py` to update model records
3. Import data with new model_key

### Testing

Before submitting changes:
```powershell
# Run full test suite
pytest

# Run import test with sample data
python scripts\import_excel.py data\sample.xlsx --dry-run

# Verify API endpoints
curl http://localhost:5000/api/stats
```

## Quick Reference Commands

### Essential Commands
```powershell
# Initialize project
pip install -r requirements.txt
python database.py

# Start application  
$env:FLASK_APP = 'app.py'
flask run --host=0.0.0.0

# Import data
python scripts\import_excel.py data\sample.xlsx

# Verify setup
python verify_setup.py
```

### Database Management Commands
```powershell
# Backup database
python backup_restore.py backup

# Reset everything safely (with backup)
python backup_restore.py

# Reset only tasks (keep models)
python reset_tasks.py

# Selective task management
python manage_tasks.py

# Update models after config changes
python database.py

# Check database status
python -c "from database import DatabaseManager; db = DatabaseManager(); models = db.get_models(); tasks = db.get_tasks(); print(f'Models: {len(models)}, Tasks: {len(tasks)}')"
```

### Import and Data Commands
```powershell
# Dry run import (validation only)
python scripts\import_excel.py your_data.xlsx --dry-run

# Import without metrics (faster)
python scripts\import_excel.py your_data.xlsx --no-metrics

# Import with custom mapping
python scripts\import_excel.py your_data.xlsx --mapping custom_mapping.json

# Generate new sample data
python scripts\generate_sample_data.py
```

### Utility Scripts Created
- `backup_restore.py` - Database backup and restore operations
- `reset_tasks.py` - Reset tasks while keeping models  
- `manage_tasks.py` - Interactive task management and selective deletion
- `verify_setup.py` - Complete setup verification

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on:

- Setting up the development environment
- Code style and standards  
- Submitting pull requests
- Reporting issues

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues or questions:
- **Issues**: [GitHub Issues](https://github.com/mp3pintyo/Leaderboard-LLM/issues)
- **Discussions**: [GitHub Discussions](https://github.com/mp3pintyo/Leaderboard-LLM/discussions)
- **Documentation**: Check the `docs/` folder for detailed guides
- **Troubleshooting**: Review the test suite for usage examples
- **API Testing**: Use the provided curl examples
- **Database**: Use the database management utilities for reset/backup operations

## Acknowledgments

- Built with Flask and Bootstrap for modern web experience
- Supports multiple LLM evaluation metrics
- Designed for ease of use and extensibility

---

**LLM Leaderboard v1.0** - A comprehensive solution for comparing language model performance across diverse tasks.