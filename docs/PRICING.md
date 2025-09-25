# Model Pricing Feature Documentation

## Overview

The LLM Leaderboard now supports comprehensive pricing information for language models, including complex tier structures based on context window usage. This feature allows users to compare not just performance, but also cost considerations when selecting models.

## Features

### Pricing Structure Types

The application supports three main pricing structures:

#### 1. Free Models (Open Source)
```python
'input_price': [{'threshold': 'all', 'price': 'Free'}],
'output_price': [{'threshold': 'all', 'price': 'Free'}]
```
- Typically for open-source models
- No usage costs
- Displayed as "Free" in both input and output columns

#### 2. Flat Rate Pricing
```python
'input_price': [{'threshold': 'all', 'price': '$5.00'}],
'output_price': [{'threshold': 'all', 'price': '$15.00'}]
```
- Single price regardless of context window size
- Simple pricing model
- Common for commercial APIs

#### 3. Tiered Pricing (Context-Based)
```python
'input_price': [
    {'threshold': '≤128K', 'price': '$1.20'},
    {'threshold': '>128K', 'price': '$3.00'}
],
'output_price': [
    {'threshold': '≤128K', 'price': '$2.40'},
    {'threshold': '>128K', 'price': '$6.00'}
]
```
- Multiple price tiers based on context window usage
- More expensive for larger contexts
- Reflects actual provider pricing models

### Display Features

#### Leaderboard Table
- **Input Price Column**: Shows all pricing tiers with thresholds
- **Output Price Column**: Displays corresponding output prices
- **Threshold Display**: Format like "≤128K: $1.20" for clarity
- **Responsive Layout**: Adapts to screen size
- **Toggleable**: Can be enabled/disabled in Settings

#### Model Detail Pages
- **Detailed Breakdown**: Complete pricing information
- **Organized Layout**: Input and Output prices in separate sections
- **Per Token Notation**: Includes "/ 1M tokens" for clarity
- **Threshold Labels**: Bold threshold indicators for easy reading
- **Visual Hierarchy**: Clear separation between price tiers

### Configuration

#### Adding Pricing to Models

Edit `config.py` and add pricing information to any model:

```python
MODELS = {
    'example-model': {
        'name': 'Example LLM',
        'provider': 'Example Corp',
        'parameters': 70,
        'context_window': 128,
        # ... other model configuration ...
        
        # Pricing configuration
        'input_price': [
            {'threshold': '≤64K', 'price': '$0.50'},
            {'threshold': '>64K', 'price': '$1.50'}
        ],
        'output_price': [
            {'threshold': '≤64K', 'price': '$1.50'},
            {'threshold': '>64K', 'price': '$4.50'}
        ]
    }
}
```

#### Pricing Field Structure

Each pricing field is an array of threshold objects:

```python
{
    'threshold': str,  # Context window threshold (e.g., '≤128K', '>128K', 'all')
    'price': str      # Price string (e.g., '$1.20', 'Free')
}
```

**Threshold Examples:**
- `'all'` - Single price for all contexts
- `'≤128K'` - Up to 128K tokens
- `'>128K'` - More than 128K tokens
- `'≤64K'` - Up to 64K tokens
- `'>100K'` - More than 100K tokens

### Real-World Examples

#### Commercial High-End Model (Grok 4)
```python
'input_price': [
    {'threshold': '≤100K', 'price': '$2.50'},
    {'threshold': '>100K', 'price': '$7.50'}
],
'output_price': [
    {'threshold': '≤100K', 'price': '$10.00'},
    {'threshold': '>100K', 'price': '$30.00'}
]
```

#### Cost-Effective Model (Kimi K2)
```python
'input_price': [
    {'threshold': '≤64K', 'price': '$0.50'},
    {'threshold': '>64K', 'price': '$1.50'}
],
'output_price': [
    {'threshold': '≤64K', 'price': '$1.50'},
    {'threshold': '>64K', 'price': '$4.50'}
]
```

#### Enterprise Model (Qwen3 Max)
```python
'input_price': [
    {'threshold': '≤128K', 'price': '$1.20'},
    {'threshold': '>128K', 'price': '$3.00'}
],
'output_price': [
    {'threshold': '≤128K', 'price': '$2.40'},
    {'threshold': '>128K', 'price': '$6.00'}
]
```

## Implementation Details

### Database Integration

Pricing information is stored in the model metadata JSON field:

```sql
-- Models table structure
CREATE TABLE models (
    id INTEGER PRIMARY KEY,
    model_key TEXT UNIQUE,
    name TEXT,
    meta TEXT  -- JSON containing pricing and other metadata
);
```

### Template Rendering

#### Leaderboard Display (index.html)
```jinja2
{% elif col_key == 'input_price' %}
<td>
    {% if model.meta.get('input_price') %}
        {% for tier in model.meta.input_price %}
            <div class="small">
                {% if tier.threshold != 'all' %}{{ tier.threshold }}: {% endif %}
                <strong>{{ tier.price }}</strong>
            </div>
        {% endfor %}
    {% else %}
        <span class="text-muted">N/A</span>
    {% endif %}
</td>
```

#### Model Detail Display (model.html)
```jinja2
{% if model.meta.get('input_price') %}
<p><strong>Input Price:</strong></p>
<ul class="list-unstyled">
    {% for tier in model.meta.input_price %}
    <li class="small">
        {% if tier.threshold != 'all' %}<strong>{{ tier.threshold }}:</strong> {% endif %}
        <span class="text-primary">{{ tier.price }}</span>
        {% if not tier.price.startswith('Free') %} / 1M tokens{% endif %}
    </li>
    {% endfor %}
</ul>
{% endif %}
```

### Settings Integration

Pricing columns are configurable through the Settings page:

```python
# config.py
LEADERBOARD_COLUMNS = {
    'input_price': {'label': 'Input Price', 'enabled': False, 'order': 16},
    'output_price': {'label': 'Output Price', 'enabled': False, 'order': 17},
}
```

Users can:
- Enable/disable pricing columns via Settings page
- View pricing information on model detail pages regardless of column settings
- See live preview of leaderboard with/without pricing columns

## User Experience

### Workflow
1. **Administrator** adds pricing information to model configurations
2. **User** enables pricing columns in Settings if desired
3. **Leaderboard** displays pricing tiers for easy comparison
4. **Model Details** show complete pricing breakdown
5. **Decision Making** informed by both performance and cost

### Benefits
- **Cost Awareness**: Users can factor in pricing when selecting models
- **Comparison**: Side-by-side cost comparison across models
- **Transparency**: Clear pricing structure display
- **Flexibility**: Support for various pricing models
- **Real-World Usage**: Reflects actual provider pricing structures

## Future Enhancements

### Planned Features
- **Cost Calculator**: Estimate costs based on usage patterns
- **Price History**: Track pricing changes over time
- **Currency Support**: Multi-currency display options
- **Bulk Pricing**: Support for volume discounts
- **Custom Metrics**: Cost per quality point calculations

### API Extensions
- **Pricing Endpoints**: Dedicated APIs for pricing information
- **Cost Estimation**: Calculate costs for given input/output sizes
- **Price Comparison**: Compare costs across multiple models
- **Alerts**: Notify when pricing changes

## Migration Guide

### Adding Pricing to Existing Models

1. **Edit config.py**:
```python
# Add pricing fields to existing model
'existing-model': {
    # ... existing configuration ...
    'input_price': [{'threshold': 'all', 'price': '$2.00'}],
    'output_price': [{'threshold': 'all', 'price': '$6.00'}]
}
```

2. **Update Database**:
```bash
python database.py  # Regenerates model metadata
```

3. **Enable Columns** (optional):
   - Visit Settings page
   - Enable "Input Price" and "Output Price" columns
   - Save settings

### Bulk Configuration

For multiple models with similar pricing:

```python
# Common pricing structure
STANDARD_PRICING = {
    'input_price': [{'threshold': 'all', 'price': '$1.00'}],
    'output_price': [{'threshold': 'all', 'price': '$3.00'}]
}

# Apply to multiple models
MODELS = {
    'model-1': {**MODEL_1_CONFIG, **STANDARD_PRICING},
    'model-2': {**MODEL_2_CONFIG, **STANDARD_PRICING},
    # ...
}
```

The pricing feature provides comprehensive cost visibility while maintaining the application's focus on performance comparison, enabling users to make informed decisions based on both capability and cost considerations.