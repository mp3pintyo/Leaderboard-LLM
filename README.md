# LLM Lea## Features

- 🏆 **Interactive Leaderboard** - Compare models across multiple metrics with filtering
- ⚙️ **Customizable Columns** - Personalize leaderboard view with column selection settings
- 🔄 **Side-by-Side Comparison** - View model outputs for the same task simultaneously with visual performance context
- 📊 **Detailed Analytics** - Per-model and per-task performance breakdowns
- 📈 **Task Group Performance Charts** - Visual comparison charts on model detail pages showing 8 models (target + 7 others)
- 🎯 **Task Performance Overview** - Interactive Chart.js visualization on comparison pages showing up to 12 models
- 📁 **Excel Import** - Easy data import from Excel/CSV files with configurable mapping
- 🔍 **Advanced Filtering** - Filter by open source, task groups, languages, metrics, and more
- 🔢 **Quality Score System** - Human evaluation scoring (0-10) with research task exclusion
- 🌐 **REST API** - Full API access for programmatic usage
- 📱 **Responsive UI** - Modern Bootstrap-based interface with Chart.js visualizations[![GitHub](https://img.shields.io/badge/GitHub-mp3pintyo%2FLeaderboard--LLM-blue)](https://github.com/mp3pintyo/Leaderboard-LLM)
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
├── database.py                # Database schema and operations with task performance analysis
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
│   ├── side_by_side.html     # Comparison page with Chart.js visualizations
│   └── model.html            # Model details page with task group charts
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
- `/side-by-side` - Side-by-side model comparison with task performance chart visualization
- `/settings` - Customize leaderboard column display
- `/model/<model_key>` - Detailed model performance with task group charts (8 models comparison)

**Side-by-Side Comparison Features:**
- **Task Performance Overview Chart** - Interactive Chart.js visualization showing up to 12 top performing models
- **Selected Model Highlighting** - Chosen models displayed in red, other top performers in blue
- **Interactive Tooltips** - Hover for detailed metrics (Quality Score, Tokens, ROUGE-L, BERTScore)
- **Visual Context** - Performance comparison before detailed output analysis
- **Responsive Design** - Charts adapt to screen size with proper model name truncation

**Task Group Performance Charts:**
- Available on individual model detail pages (`/model/<model_key>`)
- Shows performance across 5 main task groups: Language tasks, Logical reasoning, Context understanding, Programming, SVG generation
- Displays target model plus 7 similar-performing models (8 total)
- Intelligent model selection algorithm: 3-4 models before/after target model
- Interactive tooltips with task counts and performance metrics

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

# Get task outputs with performance data
curl "http://localhost:5000/api/task/reasoning_001/outputs?models=llm-001,llm-002"

# Get task performance comparison data (for charts)
curl "http://localhost:5000/api/task/logical_reasoning_005/performance?models=llm-001,llm-003"
```

**Visual Analytics:**
```powershell
# Access model detail pages with task group charts
curl http://localhost:5000/model/llm-001

# Access side-by-side comparison with task performance visualization
curl "http://localhost:5000/side-by-side?task_id=logical_reasoning_005&models=llm-001&models=llm-003"
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

### Visualization Configuration

Chart.js visualizations can be customized:

```javascript
// Task performance charts (side-by-side page)
const taskPerformanceConfig = {
    chart_height: '400px',
    max_models: 12,
    selected_color: 'rgba(220, 53, 69, 0.8)',  // Red for selected
    other_color: 'rgba(54, 162, 235, 0.8)',    // Blue for others
    model_name_truncate: 15
};

// Task group charts (model detail pages)  
const taskGroupConfig = {
    chart_height: '350px',
    models_per_chart: 8,
    target_highlight_color: 'rgba(220, 53, 69, 0.8)',
    comparison_color: 'rgba(54, 162, 235, 0.8)',
    model_name_truncate: 12
};
```

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

## Visualization Features

### Task Performance Charts (Side-by-Side Comparison)

The side-by-side comparison page (`/side-by-side`) includes interactive performance visualization:

**Features:**
- **Interactive Bar Charts** - Chart.js powered visualizations
- **Up to 12 Models** - Shows top performing models for the selected task
- **Color Coding** - Selected models in red, other top performers in blue
- **Rich Tooltips** - Hover for Quality Score, Tokens, ROUGE-L, BERTScore details
- **Responsive Design** - Adapts to screen size with proper scaling

**Usage:**
1. Select a task from the dropdown menu
2. Choose 2-4 models to compare
3. View the performance chart above detailed output comparison
4. Use the chart to understand relative performance before analyzing outputs

### Task Group Performance Charts (Model Detail Pages)

Individual model pages (`/model/<model_key>`) feature comprehensive task group analysis:

**Features:**
- **5 Task Groups** - Language tasks, Logical reasoning, Context understanding, Programming, SVG generation
- **8 Model Comparison** - Target model + 7 similar performers per chart
- **Intelligent Selection** - Algorithm selects 3-4 models before/after target based on performance
- **Adaptive Layout** - Responsive grid layout (2 charts per row on desktop)
- **Interactive Tooltips** - Task count and performance metrics on hover

**Chart Generation Algorithm:**
1. Sorts all models by performance in each task group
2. Finds target model position in sorted list
3. Selects 3-4 models before and 3-4 models after target
4. Adapts selection when fewer models available on one side
5. Highlights target model in red, comparison models in blue

### Chart Configuration

**Default Settings:**
```javascript
// Task Performance Chart (side-by-side)
{
    type: 'bar',
    height: '400px',
    max_models: 12,
    selected_color: '#dc3545',      // Bootstrap danger (red)
    other_color: '#0d6efd',         // Bootstrap primary (blue)
    responsive: true,
    tooltips: true
}

// Task Group Charts (model detail)
{
    type: 'bar', 
    height: '350px',
    models_per_chart: 8,
    target_color: '#dc3545',        // Red for target model
    comparison_color: '#0d6efd',    // Blue for comparison models
    grid_layout: 'col-lg-6 col-md-12'
}
```

**Customization:**
Charts can be customized by modifying the Chart.js configuration in:
- `templates/side_by_side.html` - Task performance charts
- `templates/model.html` - Task group comparison charts

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

**Chart not displaying:**
```powershell
# Check if Chart.js is loaded
# Open browser developer tools (F12) and check console for errors
# Verify task has data: visit /api/task/<task_id>/outputs

# If charts don't appear, clear browser cache and reload
```

**Performance charts show wrong models:**
```powershell
# Update database model selection algorithm
python -c "from database import DatabaseManager; db = DatabaseManager(); print('Task group data:', db.get_task_group_performance('llm-001'))"

# Ensure models have performance data for the task
python -c "from database import DatabaseManager; db = DatabaseManager(); print('Task performance:', db.get_task_performance('logical_reasoning_005'))"
```

**Side-by-side comparison missing chart:**
- Ensure task_id parameter is provided in URL
- Check that selected models have data for the task
- Verify Chart.js CDN is accessible (check network tab in browser dev tools)

**Model detail charts showing empty:**
- Verify model exists: `/api/model/<model_key>`
- Check if model has task group performance data
- Ensure task groups are properly configured in config.py

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

### Adding New Features

**Adding custom task performance metrics:**
1. Add metric computation to `eval/compute_metrics.py`
2. Update `database.py` get_task_performance() method
3. Modify chart configuration in templates
4. Update API endpoints for new metric exposure

**Customizing chart appearance:**
1. Edit Chart.js configuration in `templates/side_by_side.html` 
2. Modify color schemes in chart data generation
3. Adjust responsive breakpoints and sizing
4. Update tooltip formatting and content

**Adding new task group categories:**
1. Update `config.py` TASK_GROUPS list
2. Modify `database.py` get_task_group_performance() method
3. Import data with new task_group values
4. Charts will automatically include new categories

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