"""
AI-powered task extraction service.
Uses OpenAI API when available, falls back to rule-based extraction.
"""
import os
import re
from typing import List, Tuple
from datetime import datetime

from ..models import Task, Thought

# Try to import OpenAI
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


def extract_tasks_from_thought(thought: Thought) -> Tuple[List[Task], bool]:
    """
    Extract tasks from a thought.
    Returns (tasks, used_ai) tuple.
    """
    # Try OpenAI first if available and configured
    if OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
        try:
            tasks = _extract_with_openai(thought)
            if tasks:
                return tasks, True
        except Exception as e:
            print(f"OpenAI extraction failed: {e}")
    
    # Fall back to rule-based extraction
    tasks = _extract_with_rules(thought)
    return tasks, False


def _extract_with_openai(thought: Thought) -> List[Task]:
    """Extract tasks using OpenAI API."""
    client = OpenAI()
    
    prompt = f"""Analyze the following text and extract any tasks, to-dos, or action items.
For each task found, provide just the task description in a simple, actionable format.
If no tasks are found, return an empty list.

Text: {thought.content}

Return the tasks as a JSON array of strings, like:
["Task 1", "Task 2", "Task 3"]

If there are no tasks, return: []
"""
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts tasks and action items from text. Return only valid JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_tokens=500
    )
    
    content = response.choices[0].message.content.strip()
    
    # Parse the JSON response
    import json
    try:
        # Try to extract JSON from the response
        if content.startswith("["):
            task_titles = json.loads(content)
        else:
            # Try to find JSON array in the response
            match = re.search(r'\[.*?\]', content, re.DOTALL)
            if match:
                task_titles = json.loads(match.group())
            else:
                return []
    except json.JSONDecodeError:
        return []
    
    # Create Task objects
    tasks = []
    for title in task_titles:
        if title and isinstance(title, str) and len(title.strip()) > 0:
            task = Task(
                title=title.strip(),
                created_at=thought.timestamp,
                thought_id=thought.id
            )
            tasks.append(task)
    
    return tasks


def _extract_with_rules(thought: Thought) -> List[Task]:
    """Extract tasks using rule-based approach."""
    content = thought.content
    tasks = []
    seen_titles = set()  # For deduplication
    
    # Task indicator keywords
    task_indicators = [
        'need to', 'must', 'should', 'todo', 'to do', 'task', 'buy',
        'remember to', "don't forget", 'have to', 'get', 'pickup', 'pick up',
        'call', 'email', 'contact', 'schedule', 'meet', 'appointment', 'deadline',
        'finish', 'complete', 'start', 'begin', 'send', 'pay', 'make', 'plan',
        'check', 'review', 'update', 'organize', 'clean', 'fix', 'prepare',
        'go to', 'visit', 'work on', 'look at', 'find', 'search', 'apply',
        'figure out', 'talk', 'discuss', 'follow up', 'arrange', 'order'
    ]
    
    # Check for list items (bullets, numbers)
    list_items = _extract_list_items(content)
    if list_items:
        for item in list_items:
            if item.lower() not in seen_titles:
                seen_titles.add(item.lower())
                tasks.append(Task(
                    title=item,
                    created_at=thought.timestamp,
                    thought_id=thought.id
                ))
        if tasks:
            return tasks
    
    # For short content, treat the whole thing as a task
    if len(content) < 100:
        tasks.append(Task(
            title=content.strip(),
            created_at=thought.timestamp,
            thought_id=thought.id
        ))
        return tasks
    
    # Check if content contains task indicators
    content_lower = content.lower()
    has_task_indicator = any(indicator in content_lower for indicator in task_indicators)
    
    if not has_task_indicator:
        # For longer content without indicators, still try to extract sentences
        sentences = _extract_sentences(content)
        for sentence in sentences:
            if len(sentence) > 5 and len(sentence) < 150:
                if sentence.lower() not in seen_titles:
                    seen_titles.add(sentence.lower())
                    tasks.append(Task(
                        title=sentence,
                        created_at=thought.timestamp,
                        thought_id=thought.id
                    ))
        if not tasks:
            # If still no tasks, use the whole content
            tasks.append(Task(
                title=content[:150] + ("..." if len(content) > 150 else ""),
                created_at=thought.timestamp,
                thought_id=thought.id
            ))
        return tasks
    
    # Split by delimiters and process
    delimiters = ['. ', '.\n', ', ', '; ', '\n', ' and ', ' then ', ' also ']
    best_delimiter = _find_best_delimiter(content, delimiters)
    
    if best_delimiter:
        parts = content.split(best_delimiter)
    else:
        parts = [content]
    
    for part in parts:
        part = part.strip()
        if len(part) < 3:
            continue
        
        # Capitalize first letter
        if part:
            part = part[0].upper() + part[1:] if len(part) > 1 else part.upper()
        
        # Remove trailing periods
        if part.endswith('.'):
            part = part[:-1]
        
        if part and part.lower() not in seen_titles:
            seen_titles.add(part.lower())
            tasks.append(Task(
                title=part,
                created_at=thought.timestamp,
                thought_id=thought.id
            ))
    
    return tasks


def _extract_list_items(text: str) -> List[str]:
    """Extract list items from text (bullets, numbers, etc.)."""
    items = []
    
    # Match numbered list items
    numbered_pattern = re.compile(r'(?:^|\n)\s*\d+[.)]\s+(.+)', re.MULTILINE)
    for match in numbered_pattern.finditer(text):
        item = match.group(1).strip()
        if item:
            items.append(item)
    
    # Match bulleted list items
    bullet_pattern = re.compile(r'(?:^|\n)\s*[-–•*+]\s+(.+)', re.MULTILINE)
    for match in bullet_pattern.finditer(text):
        item = match.group(1).strip()
        if item:
            items.append(item)
    
    return items


def _extract_sentences(text: str) -> List[str]:
    """Extract sentences from text."""
    sentences = []
    sentence_regex = re.compile(r'([^.!?]+[.!?]+)')
    
    for match in sentence_regex.finditer(text):
        sentence = match.group(1).strip()
        # Filter out very short sentences
        if len(sentence.split()) > 2:
            sentences.append(sentence)
    
    # If no sentences found, return the whole text
    if not sentences and text.strip():
        sentences.append(text.strip())
    
    return sentences


def _find_best_delimiter(text: str, delimiters: List[str]) -> str:
    """Find the best delimiter for splitting text."""
    best_delimiter = ""
    best_score = 0
    
    for delimiter in delimiters:
        if delimiter in text:
            parts = text.split(delimiter)
            parts = [p.strip() for p in parts if p.strip()]
            
            if len(parts) > 1:
                avg_length = sum(len(p) for p in parts) // len(parts)
                score = len(parts) * 10
                
                if 5 <= avg_length <= 100:
                    score += 50
                else:
                    score -= 20
                
                if score > best_score:
                    best_score = score
                    best_delimiter = delimiter
    
    return best_delimiter

