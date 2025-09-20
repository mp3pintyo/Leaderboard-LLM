"""
Generate a sample Excel template for LLM leaderboard data import.
Shows the recommended column order and example data.
"""

import pandas as pd
import os

def create_sample_excel():
    """Create a sample Excel file with the correct structure and example data."""
    
    # Sample data following the new task groups and structure
    sample_data = [
        # Language Tasks (1-3)
        {
            'task_id': 'language_tasks_001',
            'task_name': 'Countries ending in "lia"',
            'prompt_text': 'Name the countries whose names end in "lia" in English. Also name the capitals of the countries.',
            'task_group': 'language_tasks',
            'model_key': 'llm-001',
            'quality_score': 8.5,
            'output_text': 'Countries ending in "lia": Australia (capital: Canberra), Somalia (capital: Mogadishu), Mongolia (capital: Ulaanbaatar)...',
            'tokens': 150,
            'language': 'en',
            'tags': 'geography,knowledge,facts'
        },
        {
            'task_id': 'language_tasks_001',
            'task_name': 'Countries ending in "lia"',
            'prompt_text': 'Name the countries whose names end in "lia" in English. Also name the capitals of the countries.',
            'task_group': 'language_tasks',
            'model_key': 'llm-002',
            'quality_score': 9.2,
            'output_text': 'The countries whose names end in "lia" are: 1. Australia - Capital: Canberra, 2. Somalia - Capital: Mogadishu...',
            'tokens': 180,
            'language': 'en',
            'tags': 'geography,knowledge,facts'
        },
        {
            'task_id': 'language_tasks_002',
            'task_name': 'English pangram without x,y,z',
            'prompt_text': 'Write an English pangram that uses every letter of the alphabet exactly once except: x,y,z',
            'task_group': 'language_tasks',
            'model_key': 'llm-001',
            'quality_score': 0,  # Example of 0 score for poor response
            'output_text': 'The quick brown jug vefd mph.',
            'tokens': 45,
            'language': 'en',
            'tags': 'creative,wordplay,pangram'
        },
        {
            'task_id': 'language_tasks_003',
            'task_name': 'Haiku with "Simple" acrostic',
            'prompt_text': 'Write a haiku where the second letter of each word when put together spells "Simple"',
            'task_group': 'language_tasks',
            'model_key': 'llm-002',
            'quality_score': 7.9,
            'output_text': 'Silent morning dew\nRipples on quiet water\nLoud birds sing sweetly',
            'tokens': 65,
            'language': 'en',
            'tags': 'creative,poetry,haiku,wordplay'
        },
        
        # Logical Reasoning (4-6)
        {
            'task_id': 'logical_reasoning_004',
            'task_name': 'Birds on tree riddle',
            'prompt_text': '15 birds are sitting on a tree. One is shot with a rifle. How many birds remain on the tree? I ask for all possible solutions.',
            'task_group': 'logical_reasoning',
            'model_key': 'llm-003',
            'quality_score': 9.1,
            'output_text': 'Possible answers: 0 birds (others flew away from gunshot), 14 birds (assuming others stay), 15 birds (if missed)...',
            'tokens': 220,
            'language': 'en',
            'tags': 'logic,riddle,lateral_thinking'
        },
        {
            'task_id': 'logical_reasoning_005',
            'task_name': 'River crossing for peaches',
            'prompt_text': 'You are standing on one side of a river, on the other side there is a peach tree with peaches. You have a boat. How do you get to the other side in the summer to eat peaches from the tree? How do you get to the other side in the winter and eat peaches from the tree? The river is frozen in the winter, so you can\'t go by boat. Describe it in detail.',
            'task_group': 'logical_reasoning',
            'model_key': 'llm-001',
            'quality_score': 8.3,
            'output_text': 'Summer: Use the boat to row across the river, dock on the other side, and pick peaches. Winter: Walk across the frozen river...',
            'tokens': 195,
            'language': 'en',
            'tags': 'logic,problem_solving,seasonal'
        },
        
        # Programming (10-14)
        {
            'task_id': 'programming_010',
            'task_name': 'HTML confetti button',
            'prompt_text': 'Create an HTML page with a button that explodes confetti when you click it. You can use CSS & JS as well.',
            'task_group': 'programming',
            'model_key': 'llm-002',
            'quality_score': 8.7,
            'output_text': '<!DOCTYPE html><html><head><style>/* CSS styles */</style></head><body><button onclick="explodeConfetti()">Click me!</button><script>function explodeConfetti(){...}</script></body></html>',
            'tokens': 450,
            'language': 'en',
            'tags': 'programming,html,javascript,css'
        },
        {
            'task_id': 'programming_013',
            'task_name': 'Python bouncing balls simulation',
            'prompt_text': 'Write a single-file Python program that simulates 20 bouncing balls confined within a rotating heptagon...',
            'task_group': 'programming',
            'model_key': 'llm-003',
            'quality_score': 9.5,
            'output_text': 'import tkinter as tk\nimport math\nimport numpy as np\nfrom dataclasses import dataclass\nfrom typing import List\n\n@dataclass\nclass Ball:...',
            'tokens': 850,
            'language': 'en',
            'tags': 'programming,python,simulation,physics'
        },
        
        # SVG Generation (15-17)
        {
            'task_id': 'svg_generation_015',
            'task_name': 'Butterfly SVG',
            'prompt_text': 'Generate the SVG code for a butterfly',
            'task_group': 'svg_generation',
            'model_key': 'llm-001',
            'quality_score': 7.4,
            'output_text': '<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg"><path d="M100,100 Q80,80 60,100 Q80,120 100,100 Q120,80 140,100 Q120,120 100,100" fill="orange"/></svg>',
            'tokens': 120,
            'language': 'en',
            'tags': 'svg,graphics,creative,vector'
        },
        
        # Research (18)
        {
            'task_id': 'research_018',
            'task_name': 'Hungarian tourism future',
            'prompt_text': 'A magyar turizmus jövője',
            'task_group': 'research',
            'model_key': 'llm-002',
            'quality_score': 8.9,
            'output_text': 'A magyar turizmus jövője számos tényezőtől függ, beleértve a fenntartható fejlesztést, digitalizációt és a kulturális örökség megőrzését...',
            'tokens': 320,
            'language': 'hu',
            'tags': 'research,tourism,hungary,future'
        }
    ]
    
    # Create DataFrame with proper column order
    column_order = [
        # REQUIRED columns first
        'task_id',
        'task_name', 
        'prompt_text',
        'task_group',
        'model_key',
        'quality_score',
        # OPTIONAL columns after
        'output_text',
        'tokens',
        'language',
        'tags'
    ]
    
    df = pd.DataFrame(sample_data)
    df = df[column_order]  # Reorder columns
    
    # Save to Excel
    output_file = 'sample_import_template.xlsx'
    df.to_excel(output_file, index=False, engine='openpyxl')
    
    print(f"✅ Sample Excel template created: {output_file}")
    print(f"📊 Contains {len(df)} rows with {len(df.columns)} columns")
    print(f"📋 Column order: {', '.join(column_order)}")
    print(f"🎯 Shows examples from all task groups:")
    print(f"   - language_tasks (2 examples)")
    print(f"   - logical_reasoning (2 examples)")  
    print(f"   - programming (2 examples)")
    print(f"   - svg_generation (1 example)")
    print(f"   - research (1 example)")
    
    return output_file

if __name__ == "__main__":
    create_sample_excel()
