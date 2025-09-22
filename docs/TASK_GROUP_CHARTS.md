# Task Group Performance Charts

## Overview

Every model detail page now includes interactive performance comparison charts for the first 5 task groups. These charts provide visual insights into how a model performs relative to similar models across different categories.

## Features

### Visual Comparison
- **Bar Charts**: Interactive Chart.js visualizations
- **5 Task Groups**: Shows performance for the first 5 categories defined in `TASK_GROUPS`
- **Relative Performance**: Compares target model with 2-3 similar-performing models
- **Responsive Design**: Charts adapt to screen size

### Task Groups Displayed
1. **Language Tasks** - Basic language understanding (countries, pangrams, haiku)
2. **Logical Reasoning** - Logic puzzles and reasoning challenges  
3. **Context Understanding** - Reading comprehension and context analysis
4. **Programming** - Code generation and technical tasks
5. **SVG Generation** - Visual and creative content creation

### Chart Details
- **Target Model**: Highlighted in red for easy identification
- **Comparison Models**: Shown in blue, selected based on similar overall performance
- **Score Range**: Y-axis spans 0-10 (Quality Score scale)
- **Tooltips**: Hover to see full model names and task counts
- **Truncated Labels**: Long model names are shortened with "..." for better display

## Technical Implementation

### Database Query
The `get_task_group_performance()` method:
- Excludes `research_018` task (consistent with main scoring)
- Groups results by task category
- Sorts models by average score within each group
- Selects 2-3 models before and after target model for comparison

### Frontend Rendering
- **Chart.js Library**: Modern, responsive chart rendering
- **Dynamic Data**: Charts are generated from Flask template data
- **Color Coding**: Consistent color scheme across all charts
- **Interactive Elements**: Tooltips and responsive design

### Example Chart Data Structure
```javascript
{
  "language_tasks": {
    "models": [
      {"name": "GPT-4", "avg_score": 8.5, "task_count": 3},
      {"name": "Target Model", "avg_score": 8.2, "task_count": 3},
      {"name": "Claude-3", "avg_score": 7.9, "task_count": 3}
    ],
    "target_model": {"name": "Target Model", ...},
    "target_index": 1
  }
}
```

## Usage

### Accessing Charts
1. Navigate to any model detail page: `/model/<model_key>`
2. Scroll to "Task Group Performance Comparison" section
3. View up to 5 interactive charts
4. Hover over bars for detailed information

### Interpreting Results
- **Red Bar**: Your selected model's performance
- **Blue Bars**: Similar-performing models for context
- **Height**: Represents average Quality Score (0-10)
- **Missing Charts**: Appear only if model has data for that task group

## Benefits

### For Users
- **Quick Insights**: Immediately see relative strengths/weaknesses
- **Context**: Understand performance compared to similar models
- **Visual Learning**: Charts are easier to interpret than raw numbers
- **Category-Specific**: See performance breakdown by task type

### For Analysis
- **Benchmarking**: Compare models within specific domains
- **Pattern Recognition**: Identify consistent performers across categories
- **Decision Making**: Choose models based on task-specific requirements
- **Performance Trends**: Understand model capabilities across different areas

## Future Enhancements

### Planned Features
- **More Task Groups**: Expand beyond first 5 categories
- **Chart Types**: Add line charts for performance trends
- **Export Options**: Download charts as images
- **Comparison Controls**: Select which models to compare against
- **Historical Data**: Show performance changes over time

### Configuration Options
- **Chart Settings**: Customize colors, scales, and display options
- **Group Selection**: Choose which task groups to display
- **Model Pool**: Control which models are included in comparisons

The task group performance charts provide valuable insights into model capabilities and help users make informed decisions based on visual, comparative data across different AI task categories.