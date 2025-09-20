# Settings Functionality

The LLM Leaderboard now includes a customizable settings page that allows users to control which columns are displayed on the main leaderboard.

## Features

### Column Customization
- **Navigate to Settings**: Click the "Settings" link in the navigation bar or visit `/settings`
- **Toggle Columns**: Use the switches to enable/disable specific columns
- **Required Columns**: Some columns (Rank, Model, Actions) are always enabled and cannot be disabled
- **Preview Changes**: See how your leaderboard will look with the selected columns
- **Save Settings**: Settings are saved automatically and persist during your session

### Filter Display Customization
- **Toggle Filters**: Control which filter controls appear on the leaderboard
- **Default Enabled**: Provider, Open Source, and Task Group filters are enabled by default
- **Custom Configuration**: Choose from 10 different filter types
- **Session Persistence**: Filter visibility settings are saved for your session

### Available Columns

| Column | Description | Required |
|--------|-------------|----------|
| Rank | Position in leaderboard | ✓ |
| Model | Model name and key | ✓ |
| Provider | Model provider/company | |
| Open Source | Whether model is open source | |
| Tags | Model tags (instruction, reasoning, etc.) | |
| Tasks | Number of completed tasks | |
| Avg Tokens | Average tokens per output | |
| Quality Score | Human evaluation score (0-10) | |
| ROUGE-L | ROUGE-L metric score | |
| BERTScore | BERTScore metric | |
| Reasoning | Whether model supports reasoning | |
| Parameters | Model parameter count | |
| Context Window | Maximum context length | |
| Image Input | Whether model accepts images | |
| Release Date | Model release date | |
| Actions | Detail and compare buttons | ✓ |

### Default Configuration

The default visible columns are:
- Rank
- Model  
- Provider
- Open Source
- Quality Score
- Reasoning
- Parameters
- Context Window
- Image Input
- Actions

Note: Tags and Release Date columns are available but disabled by default.

### Available Filters

| Filter | Description | Default |
|--------|-------------|---------|
| Provider | Model provider/company selection | ✓ |
| Open Source | Filter by open source availability | ✓ |
| Reasoning | Filter by reasoning capability | |
| Image Input | Filter by image input support | |
| Task Group | Filter by task categories | ✓ |
| Language | Filter by language support | |
| Tag | Filter by model tags | |
| Parameters Range | Filter by parameter count (min/max) | |
| Context Window Range | Filter by context window size | |
| Release Date Range | Filter by release date | |

### API Endpoints

#### Save Column Settings
```
POST /api/settings/columns
Content-Type: application/json

{
    "enabled_columns": ["rank", "model", "provider", "quality_score", "actions"]
}
```

#### Save Filter Settings
```
POST /api/settings/filters
Content-Type: application/json

{
    "enabled_filters": ["provider", "open_source", "task_group"]
}
```

#### Reset to Default
```
POST /api/settings/columns/reset
POST /api/settings/filters/reset
```

### Session Storage

Column preferences are stored in the user's session and will persist until:
- The session expires
- The browser is closed
- Settings are reset to default

### Future Enhancements

Planned features for the settings page:
- Default sorting preferences
- Items per page configuration
- Theme customization
- Export format options
- User accounts with persistent settings

### Implementation Details

The settings functionality is implemented through:

1. **Configuration**: `LEADERBOARD_COLUMNS` in `config.py` defines all available columns
2. **Session Management**: User preferences stored in Flask session
3. **Dynamic Templates**: `index.html` renders columns based on user settings
4. **API Endpoints**: RESTful API for saving/loading preferences
5. **JavaScript**: Interactive settings page with live preview

### Usage Example

1. Visit the leaderboard at `http://localhost:5000/`
2. Click "Customize Columns" or go to Settings
3. Toggle off columns you don't want to see (e.g., "Avg Tokens", "ROUGE-L")
4. Click "Save Settings"
5. Return to leaderboard to see your customized view
6. Use "Reset to Default" to restore all columns

The settings provide a personalized experience while maintaining the core functionality of the leaderboard for comparing LLM performance.