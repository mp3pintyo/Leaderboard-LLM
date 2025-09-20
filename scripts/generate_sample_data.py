"""
Generate sample Excel data for testing the LLM Leaderboard application.
"""

import pandas as pd
import os

def create_sample_data():
    """Create sample Excel file with LLM results data."""
    
    # Sample data representing different tasks and model outputs
    data = {
        'task_id': [
            'reasoning_001', 'reasoning_001', 'reasoning_001',
            'coding_001', 'coding_001', 'coding_001',
            'translation_001', 'translation_001', 'translation_001',
            'summarization_001', 'summarization_001', 'summarization_001',
            'math_001', 'math_001', 'math_001'
        ],
        'task_name': [
            'Logical Reasoning Test', 'Logical Reasoning Test', 'Logical Reasoning Test',
            'Python Code Generation', 'Python Code Generation', 'Python Code Generation',
            'English to French Translation', 'English to French Translation', 'English to French Translation',
            'News Article Summarization', 'News Article Summarization', 'News Article Summarization',
            'Basic Math Word Problem', 'Basic Math Word Problem', 'Basic Math Word Problem'
        ],
        'prompt_text': [
            # Reasoning task
            'If all birds can fly and penguins are birds, can penguins fly? Explain your reasoning.',
            'If all birds can fly and penguins are birds, can penguins fly? Explain your reasoning.',
            'If all birds can fly and penguins are birds, can penguins fly? Explain your reasoning.',
            
            # Coding task
            'Write a Python function that calculates the factorial of a number using recursion.',
            'Write a Python function that calculates the factorial of a number using recursion.',
            'Write a Python function that calculates the factorial of a number using recursion.',
            
            # Translation task
            'Translate the following sentence to French: "The weather is beautiful today and I would like to go for a walk in the park."',
            'Translate the following sentence to French: "The weather is beautiful today and I would like to go for a walk in the park."',
            'Translate the following sentence to French: "The weather is beautiful today and I would like to go for a walk in the park."',
            
            # Summarization task
            'Summarize this article in 2-3 sentences: "Climate change continues to be one of the most pressing issues of our time. Recent studies show that global temperatures have risen by 1.1 degrees Celsius since pre-industrial times. Scientists warn that without immediate action, we could see catastrophic effects including rising sea levels, extreme weather events, and ecosystem collapse. Governments worldwide are implementing various policies to reduce carbon emissions and transition to renewable energy sources."',
            'Summarize this article in 2-3 sentences: "Climate change continues to be one of the most pressing issues of our time. Recent studies show that global temperatures have risen by 1.1 degrees Celsius since pre-industrial times. Scientists warn that without immediate action, we could see catastrophic effects including rising sea levels, extreme weather events, and ecosystem collapse. Governments worldwide are implementing various policies to reduce carbon emissions and transition to renewable energy sources."',
            'Summarize this article in 2-3 sentences: "Climate change continues to be one of the most pressing issues of our time. Recent studies show that global temperatures have risen by 1.1 degrees Celsius since pre-industrial times. Scientists warn that without immediate action, we could see catastrophic effects including rising sea levels, extreme weather events, and ecosystem collapse. Governments worldwide are implementing various policies to reduce carbon emissions and transition to renewable energy sources."',
            
            # Math task
            'Sarah has 24 apples. She gives away 1/3 of them to her friends and then buys 8 more apples. How many apples does Sarah have now?',
            'Sarah has 24 apples. She gives away 1/3 of them to her friends and then buys 8 more apples. How many apples does Sarah have now?',
            'Sarah has 24 apples. She gives away 1/3 of them to her friends and then buys 8 more apples. How many apples does Sarah have now?'
        ],
        'task_group': [
            'reasoning', 'reasoning', 'reasoning',
            'coding', 'coding', 'coding',
            'language_understanding', 'language_understanding', 'language_understanding',
            'language_understanding', 'language_understanding', 'language_understanding',
            'math', 'math', 'math'
        ],
        'model_key': [
            'llm-001', 'llm-002', 'llm-003',
            'llm-001', 'llm-002', 'llm-003',
            'llm-001', 'llm-002', 'llm-003',
            'llm-001', 'llm-002', 'llm-003',
            'llm-001', 'llm-002', 'llm-003'
        ],
        'output_text': [
            # Reasoning outputs
            'No, penguins cannot fly despite being birds. While the statement "all birds can fly" is presented as a premise, it is actually false in reality. Penguins are birds that have evolved to be flightless, instead using their wings for swimming. This is an example of how logical reasoning must consider real-world facts.',
            'This is a classic logical fallacy. The premise "all birds can fly" is incorrect. Penguins are indeed birds, but they cannot fly. They are flightless birds that have adapted for aquatic life. The logical structure would only work if the premise were true.',
            'Based on the given premises, if we accept that "all birds can fly" and "penguins are birds," then logically penguins should be able to fly. However, this conclusion conflicts with reality, as penguins are flightless birds. This demonstrates the importance of accurate premises in logical reasoning.',
            
            # Coding outputs
            'def factorial(n):\n    if n == 0 or n == 1:\n        return 1\n    else:\n        return n * factorial(n - 1)\n\n# Example usage:\nprint(factorial(5))  # Output: 120',
            'Here\'s a recursive factorial function:\n\ndef factorial(n):\n    # Base case\n    if n <= 1:\n        return 1\n    # Recursive case\n    return n * factorial(n - 1)\n\n# Test the function\nresult = factorial(6)\nprint(f"6! = {result}")  # 6! = 720',
            'def factorial(n):\n    """Calculate factorial using recursion"""\n    if n < 0:\n        raise ValueError("Factorial not defined for negative numbers")\n    if n == 0:\n        return 1\n    return n * factorial(n - 1)\n\n# Usage example\nfor i in range(6):\n    print(f"{i}! = {factorial(i)}")',
            
            # Translation outputs
            'Le temps est magnifique aujourd\'hui et j\'aimerais aller me promener dans le parc.',
            'Il fait beau aujourd\'hui et je voudrais aller faire une promenade dans le parc.',
            'Le temps est beau aujourd\'hui et j\'aimerais faire une promenade dans le parc.',
            
            # Summarization outputs
            'Climate change remains a critical global issue with temperatures rising 1.1°C since pre-industrial times. Scientists warn of catastrophic consequences including rising sea levels and extreme weather without immediate action. Governments are responding by implementing policies to reduce emissions and promote renewable energy.',
            'Global temperatures have increased by 1.1 degrees Celsius due to climate change, making it one of today\'s most urgent challenges. Without prompt intervention, we face severe consequences like rising sea levels and ecosystem collapse. International governments are working to address this through carbon reduction policies and renewable energy initiatives.',
            'Climate change is a pressing global concern, with temperatures rising 1.1°C above pre-industrial levels. Scientists caution that delayed action could result in rising seas, extreme weather, and ecological collapse. Worldwide governments are implementing carbon reduction and renewable energy policies in response.',
            
            # Math outputs
            'Sarah starts with 24 apples. She gives away 1/3 of them: 24 × 1/3 = 8 apples given away. She has 24 - 8 = 16 apples left. Then she buys 8 more: 16 + 8 = 24 apples. Sarah has 24 apples now.',
            'Starting with 24 apples, Sarah gives away 1/3: 24 ÷ 3 = 8 apples given away. Remaining: 24 - 8 = 16 apples. After buying 8 more: 16 + 8 = 24 apples total.',
            'Initial apples: 24. Given away: 24 × (1/3) = 8 apples. Remaining: 24 - 8 = 16 apples. After purchasing 8 more: 16 + 8 = 24 apples. Final answer: 24 apples.'
        ],
        'tokens': [
            95, 78, 102,    # Reasoning
            65, 88, 95,     # Coding
            18, 20, 19,     # Translation
            68, 85, 72,     # Summarization
            78, 65, 58      # Math
        ],
        'length': [
            456, 398, 512,  # Reasoning
            201, 234, 287,  # Coding
            89, 95, 91,     # Translation
            398, 456, 387,  # Summarization
            234, 198, 176   # Math
        ],
        'quality_score': [
            8.5, 7.2, 9.1,  # Reasoning: Llama excellent, GPT good, Claude excellent
            7.8, 9.3, 8.7,  # Coding: Llama good, GPT excellent, Claude very good
            6.9, 8.1, 8.8,  # Translation: Llama fair, GPT good, Claude very good
            8.2, 8.9, 8.4,  # Summarization: all perform well
            7.5, 8.7, 9.2   # Math: increasing quality
        ]
    }
    
    return pd.DataFrame(data)


def main():
    """Generate and save sample Excel file."""
    # Create sample data
    df = create_sample_data()
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Save to Excel file
    output_file = os.path.join('data', 'sample.xlsx')
    df.to_excel(output_file, index=False)
    
    print(f"Sample data created successfully!")
    print(f"File: {output_file}")
    print(f"Rows: {len(df)}")
    print(f"Tasks: {df['task_id'].nunique()}")
    print(f"Models: {df['model_key'].nunique()}")
    print("\nTask groups:")
    for group in df['task_group'].unique():
        count = df[df['task_group'] == group]['task_id'].nunique()
        print(f"  - {group}: {count} tasks")


if __name__ == "__main__":
    main()