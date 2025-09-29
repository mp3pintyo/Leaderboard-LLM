"""
Configuration settings for LLM Leaderboard application.
"""

import os
from typing import Dict, Any

# Application settings
DATA_DIR = 'data'
DATABASE = 'results.db'
ALLOWED_EXTENSIONS = ['.xlsx', '.csv']
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

# Flask settings
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'

# Model configurations
MODELS: Dict[str, Dict[str, Any]] = {
    'llm-001': {
        'name': 'Qwen3 Max Preview',
        'api_id': 'qwen3-max-preview',
        'open_source': False,
        'tokenizer': 'unknown',
        'reasoning': False,
        'languages': ['en', 'hu'],
        'tags': ['general'],
        'provider': 'Alibaba Cloud',
        'parameters': 1000,  # Billion parameters
        'context_window': 262,  # Thousand tokens (K)
        'release_date': '2025-09-01',
        'image_input': False,
        'input_price': [{'threshold': '≤128K', 'price': '$1.20'}, {'threshold': '>128K', 'price': '$3.00'}],
        'output_price': [{'threshold': '≤128K', 'price': '$6.00'}, {'threshold': '>128K', 'price': '$15.00'}]
    },
    'llm-002': {
        'name': 'GPT-4o',
        'api_id': 'gpt-4o',
        'open_source': False,
        'tokenizer': 'unknown',  # Javított tokenizer
        'reasoning': False,
        'languages': ['en', 'hu', 'de', 'fr', 'es'],  # Több nyelv
        'tags': ['general', 'multimodal'],  # Több tag
        'provider': 'OpenAI',
        'parameters': 200,  # Billion parameters
        'context_window': 128,  # Thousand tokens (K)
        'release_date': '2025-02-01',
        'image_input': True,
        'input_price': [{'threshold': 'all', 'price': '$2.50'}],
        'output_price': [{'threshold': 'all', 'price': '$10.00'}]
    },
    'llm-003': {
        'name': 'GLM-4.5-106B-A12B Air',
        'api_id': 'glm-4-5-106b-a12b',
        'open_source': True,
        'tokenizer': 'unknown',
        'reasoning': True,
        'languages': ['en'],
        'tags': ['general'],
        'provider': 'Z.ai',
        'parameters': 106,  # Billion parameters
        'context_window': 128,  # Thousand tokens (K)
        'release_date': '2025-07-28',
        'image_input': False,
        'input_price': [{'threshold': 'all', 'price': 'Free'}],
        'output_price': [{'threshold': 'all', 'price': 'Free'}]
    },
    'llm-004': {
        'name': 'GLM-4.5-355B-A32B',
        'api_id': 'glm-4-5-355b-a32b',
        'open_source': True,
        'tokenizer': 'unknown',
        'reasoning': True,
        'languages': ['en'],
        'tags': ['general'],
        'provider': 'Z.ai',
        'parameters': 355,  # Billion parameters
        'context_window': 128,  # Thousand tokens (K)
        'release_date': '2025-07-28',
        'image_input': False,
        'input_price': [{'threshold': 'all', 'price': '$0.40'}],
        'output_price': [{'threshold': 'all', 'price': '$1.60'}]
    },
    'llm-005': {
        'name': 'Kimi K2 0905',
        'api_id': 'kimi-k2-0905',
        'open_source': True,
        'tokenizer': 'unknown',
        'reasoning': True,
        'languages': ['en'],
        'tags': ['general'],
        'provider': 'Moonshot AI',
        'parameters': 1000,  # Billion parameters
        'context_window': 256,  # Thousand tokens (K)
        'release_date': '2025-09-01',
        'image_input': False,
        'input_price': [{'threshold': 'all', 'price': '$0.38'}],
        'output_price': [{'threshold': 'all', 'price': '$1.52'}]
    },
    'llm-006': {
        'name': 'Cogito V2 Preview Deepseek 671B',
        'api_id': 'cogito-v2-preview-deepseek-671b',
        'open_source': True,
        'tokenizer': 'unknown',
        'reasoning': True,
        'languages': ['en'],
        'tags': ['general'],
        'provider': 'Deep Cogito',
        'parameters': 671,  # Billion parameters
        'context_window': 163,  # Thousand tokens (K)
        'release_date': '2025-07-31',
        'image_input': True,
        'input_price': [{'threshold': 'all', 'price': '$1.25'}],
        'output_price': [{'threshold': 'all', 'price': '$1.25'}]
    },
    'llm-007': {
        'name': 'Seed-OSS-36B',
        'api_id': 'seed-oss-36b',
        'open_source': True,
        'tokenizer': 'unknown',
        'reasoning': True,
        'languages': ['en'],
        'tags': ['general'],
        'provider': 'ByteDance',
        'parameters': 36,  # Billion parameters
        'context_window': 512,  # Thousand tokens (K)
        'release_date': '2025-08-20',
        'image_input': False,
        'input_price': [{'threshold': 'all', 'price': '$0.16'}],
        'output_price': [{'threshold': 'all', 'price': '$0.65'}]
    },
    'llm-008': {
        'name': 'Qwen3-Next-80B-A3B-Thinking',
        'api_id': 'qwen3-next-80b-a3b-thinking',
        'open_source': True,
        'tokenizer': 'unknown',
        'reasoning': True,
        'languages': ['en'],
        'tags': ['general'],
        'provider': 'Alibaba Cloud',
        'parameters': 80,  # Billion parameters
        'context_window': 262,  # Thousand tokens (K)
        'release_date': '2025-09-01',
        'image_input': False,
        'input_price': [{'threshold': '≤128K', 'price': '$1.20'}, {'threshold': '>128K', 'price': '$3.00'}],
        'output_price': [{'threshold': '≤128K', 'price': '$2.40'}, {'threshold': '>128K', 'price': '$6.00'}]
    },
    'llm-009': {
        'name': 'Qwen3-Next-80B-A3B-Instruct',
        'api_id': 'qwen3-next-80b-a3b-instruct',
        'open_source': True,
        'tokenizer': 'unknown',
        'reasoning': False,
        'languages': ['en'],
        'tags': ['general'],
        'provider': 'Alibaba Cloud',
        'parameters': 80,  # Billion parameters
        'context_window': 262,  # Thousand tokens (K)
        'release_date': '2025-09-09',
        'image_input': False,
        'input_price': [{'threshold': 'all', 'price': '$0.10'}],
        'output_price': [{'threshold': 'all', 'price': '$0.80'}]
    },
    'llm-010': {
        'name': 'gpt-oss-120b',
        'api_id': 'gpt-oss-120b',
        'open_source': True,
        'tokenizer': 'unknown',
        'reasoning': True,
        'languages': ['en'],
        'tags': ['general'],
        'provider': 'OpenAI',
        'parameters': 120,  # Billion parameters
        'context_window': 131,  # Thousand tokens (K)
        'release_date': '2025-08-04',
        'image_input': False,
        'input_price': [{'threshold': 'all', 'price': '$0.05'}],
        'output_price': [{'threshold': 'all', 'price': '$0.25'}]
    },
    'llm-011': {
        'name': 'Qwen3-235B-A22B-Instruct-2507',
        'api_id': 'qwen3-235b-a22b-instruct-2507',
        'open_source': True,
        'tokenizer': 'unknown',
        'reasoning': False,
        'languages': ['en'],
        'tags': ['general'],
        'provider': 'Alibaba Cloud',
        'parameters': 235,  # Billion parameters
        'context_window': 262,  # Thousand tokens (K)
        'release_date': '2025-07-21',
        'image_input': False,
        'input_price': [{'threshold': 'all', 'price': '$0.09'}],
        'output_price': [{'threshold': 'all', 'price': '$0.60'}]
    },
    'llm-012': {
        'name': 'Grok 4',
        'api_id': 'grok-4',
        'open_source': False,
        'tokenizer': 'unknown',
        'reasoning': True,
        'languages': ['en'],
        'tags': ['general'],
        'provider': 'xAI',
        'parameters': 1700,  # Billion parameters
        'context_window': 256,  # Thousand tokens (K)
        'release_date': '2025-07-09',
        'image_input': True,
        'input_price': [{'threshold': '≤128K', 'price': '$3.00'}, {'threshold': '>128K', 'price': '$6.00'}],
        'output_price': [{'threshold': '≤128K', 'price': '$15.00'}, {'threshold': '>128K', 'price': '$30.00'}]
    },
    'llm-013': {
        'name': 'Kimi K2 0905',
        'api_id': 'kimi-k2',
        'open_source': True,
        'tokenizer': 'unknown',
        'reasoning': False,
        'languages': ['en'],  # Több nyelv
        'tags': ['general'],  # Több tag
        'provider': 'Moonshot AI',
        'parameters': 1000,  # Billion parameters
        'context_window': 256,  # Thousand tokens (K)
        'release_date': '2025-09-01',
        'image_input': False,
        'input_price': [{'threshold': 'all', 'price': '$0.38'}],
        'output_price': [{'threshold': 'all', 'price': '$1.52'}]
    },
    'llm-014': {
        'name': 'DeepSeek-TNG R1T2 Chimera',
        'api_id': 'deepseek-tng-r1t2-chimera',
        'open_source': True,
        'tokenizer': 'unknown',
        'reasoning': True,
        'languages': ['en'],  # Több nyelv
        'tags': ['general'],  # Több tag
        'provider': 'TNG Tech',
        'parameters': 671,  # Billion parameters
        'context_window': 130,  # Thousand tokens (K)
        'release_date': '2025-07-02',
        'image_input': False,
        'input_price': [{'threshold': 'all', 'price': 'Free'}],
        'output_price': [{'threshold': 'all', 'price': 'Free'}]
    },
    'llm-015': {
        'name': 'DeepSeek-R1-0528',
        'api_id': 'deepseek-r1-0528',
        'open_source': True,
        'tokenizer': 'unknown',
        'reasoning': True,
        'languages': ['en'],  # Több nyelv
        'tags': ['general'],  # Több tag
        'provider': 'DeepSeek AI',
        'parameters': 671,  # Billion parameters
        'context_window': 164,  # Thousand tokens (K)
        'release_date': '2025-05-28',
        'image_input': False,
        'input_price': [{'threshold': 'all', 'price': 'Free'}],
        'output_price': [{'threshold': 'all', 'price': 'Free'}]
    },
    'llm-016': {
        'name': 'Magistral Small 1.2',
        'api_id': 'magistral-small-1-2',
        'open_source': True,
        'tokenizer': 'unknown',
        'reasoning': True,
        'languages': ['en'],  # Több nyelv
        'tags': ['general'],  # Több tag
        'provider': 'Mistral AI',
        'parameters': 200,  # Billion parameters
        'context_window': 128,  # Thousand tokens (K)
        'release_date': '2025-02-01',
        'image_input': True,
        'input_price': [{'threshold': 'all', 'price': '$0.50'}],
        'output_price': [{'threshold': 'all', 'price': '$1.50'}]
    },
    'llm-017': {
        'name': 'DeepSeek-V3.1-Terminus',
        'api_id': 'deepseek-v3-1-terminus',
        'open_source': True,
        'tokenizer': 'unknown',
        'reasoning': True,
        'languages': ['en'],  # Több nyelv
        'tags': ['general'],  # Több tag
        'provider': 'DeepSeek AI',
        'parameters': 671,  # Billion parameters
        'context_window': 128,  # Thousand tokens (K)
        'release_date': '2025-09-22',
        'image_input': True,
        'input_price': [{'threshold': 'all', 'price': '$0.27'}],
        'output_price': [{'threshold': 'all', 'price': '$1.00'}]
    },
    'llm-018': {
        'name': 'Grok 4 Fast',
        'api_id': 'grok-4-fast',
        'open_source': False,
        'tokenizer': 'unknown',
        'reasoning': True,
        'languages': ['en'],  # Több nyelv
        'tags': ['general'],  # Több tag
        'provider': 'xAI',
        'parameters': 0,  # Billion parameters
        'context_window': 2000,  # Thousand tokens (K)
        'release_date': '2025-09-19',
        'image_input': True,
        'input_price': [{'threshold': 'all', 'price': 'Free'}],
        'output_price': [{'threshold': 'all', 'price': 'Free'}]
    },
    'llm-019': {
        'name': 'Qwen3 Max Instruct',
        'api_id': 'qwen3-max-instruct',
        'open_source': False,
        'tokenizer': 'unknown',
        'reasoning': False,
        'languages': ['en', 'hu'],
        'tags': ['general'],
        'provider': 'Alibaba Cloud',
        'parameters': 1000,  # Billion parameters
        'context_window': 262,  # Thousand tokens (K)
        'release_date': '2025-09-23',
        'image_input': False,
        'input_price': [{'threshold': '≤128K', 'price': '$1.20'}, {'threshold': '>128K', 'price': '$3.00'}],
        'output_price': [{'threshold': '≤128K', 'price': '$6.00'}, {'threshold': '>128K', 'price': '$15.00'}]
    },
    'llm-020': {
        'name': 'Qwen3-30B-A3B-Instruct-2507',
        'api_id': 'qwen3-30b-a3b-instruct-2507',
        'open_source': True,
        'tokenizer': 'unknown',
        'reasoning': False,
        'languages': ['en'],  # Több nyelv
        'tags': ['general'],  # Több tag
        'provider': 'Alibaba Cloud',
        'parameters': 30,  # Billion parameters
        'context_window': 262,  # Thousand tokens (K)
        'release_date': '2025-07-25',
        'image_input': False,
        'input_price': [{'threshold': 'all', 'price': 'Free'}],
        'output_price': [{'threshold': 'all', 'price': 'Free'}]
    },
    'llm-021': {
        'name': 'Claude Sonnet 4.5',
        'api_id': 'claude-sonnet-4-5',
        'open_source': False,
        'tokenizer': 'unknown',
        'reasoning': True,
        'languages': ['en'],  # Több nyelv
        'tags': ['general'],  # Több tag
        'provider': 'Anthropic',
        'parameters': 0,  # Billion parameters
        'context_window': 1000,  # Thousand tokens (K)
        'release_date': '2025-09-29',
        'image_input': True,
        'input_price': [{'threshold': 'all', 'price': '$3.00'}],
        'output_price': [{'threshold': 'all', 'price': '$15.00'}]
    },
}

# Task groups and categories
TASK_GROUPS = [
    'language_tasks',      # 1-3: Nyelvi feladatok (országnevek, pangram, haiku)
    'logical_reasoning',   # 4-6: Logikai feladatok (madarak, folyón átkelés, misszionáriusok)
    'context_understanding', # 7-9: Kontextus értelmezés (könyv alapú kérdések)
    'programming',         # 10-14: Programozás (HTML, JS, Python szimulációk)
    'svg_generation',      # 15-17: SVG készítés és animáció
    'research'            # 18: Kutatási feladatok (turizmus jövője)
]

# Special task handling
# Note: research_018 (deep research task) is excluded from quality_score averages
# as many models lack research capabilities and receive 0 scores, which would skew results

# Supported metrics
SUPPORTED_METRICS = [
    'quality_score',  # NEW: Human evaluation 0-10 scale
    'rouge_l',
    'bert_score',
    'exact_match',
    'accuracy',
    'f1_score',
    'semantic_similarity'
]

# Default column mapping for Excel import
DEFAULT_COLUMN_MAPPING = {
    'task_id': 'task_id',                # REQUIRED: Unique task identifier
    'task_name': 'task_name',            # REQUIRED: Descriptive task name  
    'prompt_text': 'prompt_text',        # REQUIRED: The task prompt/input
    'task_group': 'task_group',          # REQUIRED: Category from TASK_GROUPS
    'model_key': 'model_key',            # REQUIRED: Model identifier from MODELS
    'quality_score': 'quality_score',    # REQUIRED: Human evaluation 0-10
    'output_text': 'output_text',        # Optional: Model response
    'tokens': 'tokens',                  # Optional: Token count
    'language': 'language',              # Optional: Language code
    'tags': 'tags'                       # Optional: Comma-separated tags
}

# Metric computation settings
METRICS_CONFIG = {
    'enable_external_apis': False,  # Set to True to enable real BERTScore, etc.
    'mock_metrics': True,  # Generate mock metrics if external APIs disabled
    'bert_score_model': 'microsoft/deberta-xlarge-mnli',  # For real BERTScore
    'rouge_metrics': ['rouge1', 'rouge2', 'rougeL'],
}

# Leaderboard display settings
LEADERBOARD_COLUMNS = {
    'rank': {'label': 'Rank', 'enabled': True, 'order': 1},
    'model': {'label': 'Model', 'enabled': True, 'order': 2},
    'provider': {'label': 'Provider', 'enabled': True, 'order': 3},
    'open_source': {'label': 'Open Source', 'enabled': True, 'order': 4},
    'tags': {'label': 'Tags', 'enabled': False, 'order': 5},
    'tasks': {'label': 'Tasks', 'enabled': False, 'order': 6},
    'avg_tokens': {'label': 'Avg Tokens', 'enabled': False, 'order': 7},
    'quality_score': {'label': 'Quality Score', 'enabled': True, 'order': 8},
    'rouge_l': {'label': 'ROUGE-L', 'enabled': False, 'order': 9},
    'bert_score': {'label': 'BERTScore', 'enabled': False, 'order': 10},
    'reasoning': {'label': 'Reasoning', 'enabled': True, 'order': 11},
    'parameters': {'label': 'Parameters', 'enabled': True, 'order': 12},
    'context_window': {'label': 'Context', 'enabled': True, 'order': 13},
    'image_input': {'label': 'Image Input', 'enabled': True, 'order': 14},
    'release_date': {'label': 'Release Date', 'enabled': False, 'order': 15},
    'input_price': {'label': 'Input Price', 'enabled': False, 'order': 16},
    'output_price': {'label': 'Output Price', 'enabled': False, 'order': 17},
    'actions': {'label': 'Actions', 'enabled': True, 'order': 18}
}

# Filter Settings Configuration
FILTER_SETTINGS = {
    'provider': {'label': 'Provider', 'enabled': True, 'order': 1},
    'open_source': {'label': 'Open Source', 'enabled': True, 'order': 2},
    'reasoning': {'label': 'Reasoning', 'enabled': False, 'order': 3},
    'image_input': {'label': 'Image Input', 'enabled': False, 'order': 4},
    'task_group': {'label': 'Task Group', 'enabled': True, 'order': 5},
    'language': {'label': 'Language', 'enabled': False, 'order': 6},
    'tag': {'label': 'Tag', 'enabled': False, 'order': 7},
    'parameters': {'label': 'Parameters Range', 'enabled': False, 'order': 8},
    'context_window': {'label': 'Context Window Range', 'enabled': False, 'order': 9},
    'release_date': {'label': 'Release Date Range', 'enabled': False, 'order': 10}
}