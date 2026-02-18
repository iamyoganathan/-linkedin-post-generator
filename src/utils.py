"""
Utility functions for LinkedIn Post Generator
"""

import re
from datetime import datetime
from typing import List
import io


def count_words(text: str) -> int:
    """
    Count words in text
    
    Args:
        text: Input text
        
    Returns:
        Number of words
    """
    if not text:
        return 0
    return len(text.split())


def count_characters(text: str, include_spaces: bool = True) -> int:
    """
    Count characters in text
    
    Args:
        text: Input text
        include_spaces: Whether to include spaces in count
        
    Returns:
        Number of characters
    """
    if not text:
        return 0
    if include_spaces:
        return len(text)
    return len(text.replace(" ", ""))


def estimate_read_time(text: str, words_per_minute: int = 200) -> int:
    """
    Estimate reading time in seconds
    
    Args:
        text: Input text
        words_per_minute: Average reading speed
        
    Returns:
        Estimated reading time in seconds
    """
    word_count = count_words(text)
    minutes = word_count / words_per_minute
    return int(minutes * 60)


def format_timestamp(timestamp: str, format: str = "%B %d, %Y at %I:%M %p") -> str:
    """
    Format timestamp string
    
    Args:
        timestamp: Timestamp string from database
        format: Desired output format
        
    Returns:
        Formatted timestamp string
    """
    try:
        dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        return dt.strftime(format)
    except:
        return timestamp


def get_relative_time(timestamp: str) -> str:
    """
    Get relative time (e.g., "2 hours ago")
    
    Args:
        timestamp: Timestamp string from database
        
    Returns:
        Relative time string
    """
    try:
        dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        diff = now - dt
        
        seconds = diff.total_seconds()
        
        if seconds < 60:
            return "just now"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif seconds < 86400:
            hours = int(seconds / 3600)
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif seconds < 604800:
            days = int(seconds / 86400)
            return f"{days} day{'s' if days != 1 else ''} ago"
        else:
            weeks = int(seconds / 604800)
            return f"{weeks} week{'s' if weeks != 1 else ''} ago"
    except:
        return "unknown"


def extract_hashtags(text: str) -> List[str]:
    """
    Extract hashtags from text
    
    Args:
        text: Input text
        
    Returns:
        List of hashtags (without #)
    """
    hashtags = re.findall(r'#(\w+)', text)
    return hashtags


def clean_text(text: str) -> str:
    """
    Clean and normalize text
    
    Args:
        text: Input text
        
    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove leading/trailing whitespace
    text = text.strip()
    return text


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to specified length
    
    Args:
        text: Input text
        max_length: Maximum length
        suffix: Suffix to append if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)].rstrip() + suffix


def format_post_preview(content: str, max_lines: int = 3) -> str:
    """
    Create a preview of post content
    
    Args:
        content: Full post content
        max_lines: Maximum number of lines to show
        
    Returns:
        Preview text
    """
    lines = content.split('\n')
    if len(lines) <= max_lines:
        return content
    
    preview_lines = lines[:max_lines]
    preview = '\n'.join(preview_lines)
    return preview + "\n..."


def add_line_breaks(text: str, max_line_length: int = 80) -> str:
    """
    Add line breaks for better readability
    
    Args:
        text: Input text
        max_line_length: Maximum characters per line
        
    Returns:
        Text with line breaks
    """
    words = text.split()
    lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        word_length = len(word) + 1  # +1 for space
        if current_length + word_length > max_line_length and current_line:
            lines.append(' '.join(current_line))
            current_line = [word]
            current_length = len(word)
        else:
            current_line.append(word)
            current_length += word_length
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return '\n'.join(lines)


def validate_post_content(content: str, min_length: int = 10, max_length: int = 3000) -> tuple:
    """
    Validate post content
    
    Args:
        content: Post content to validate
        min_length: Minimum character length
        max_length: Maximum character length
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not content or content.strip() == "":
        return False, "Post content cannot be empty"
    
    content_length = len(content)
    
    if content_length < min_length:
        return False, f"Post is too short (minimum {min_length} characters)"
    
    if content_length > max_length:
        return False, f"Post is too long (maximum {max_length} characters)"
    
    return True, ""


def count_hashtags(text: str) -> int:
    """
    Count number of hashtags in text
    
    Args:
        text: Input text
        
    Returns:
        Number of hashtags
    """
    return len(extract_hashtags(text))


def export_to_text(posts: List[dict], filename: str = "posts_export.txt") -> str:
    """
    Export posts to text file
    
    Args:
        posts: List of post dictionaries
        filename: Output filename
        
    Returns:
        File content as string
    """
    content = "LinkedIn Posts Export\n"
    content += "=" * 50 + "\n\n"
    
    for i, post in enumerate(posts, 1):
        content += f"Post #{i}\n"
        content += f"Topic: {post.get('topic', 'N/A')}\n"
        content += f"Tone: {post.get('tone', 'N/A')}\n"
        content += f"Created: {post.get('created_at', 'N/A')}\n"
        content += f"\nContent:\n{post.get('content', '')}\n"
        
        if post.get('hashtags'):
            content += f"\nHashtags: {post['hashtags']}\n"
        
        content += "\n" + "-" * 50 + "\n\n"
    
    return content


def get_emoji_suggestions(topic: str) -> dict:
    """
    Get emoji suggestions based on topic keywords
    
    Args:
        topic: Post topic
        
    Returns:
        Dictionary of category: emoji list
    """
    topic_lower = topic.lower()
    
    emoji_map = {
        "success": ["🎉", "🚀", "💪", "🏆", "⭐", "✨"],
        "learning": ["📚", "🎓", "💡", "🧠", "📖", "✍️"],
        "tech": ["💻", "⚡", "🔧", "🛠️", "🤖", "🌐"],
        "business": ["💼", "📈", "💰", "📊", "🎯", "💹"],
        "motivation": ["💪", "🔥", "⚡", "✨", "🌟", "💫"],
        "team": ["👥", "🤝", "👏", "🙌", "💚", "❤️"],
        "thinking": ["🤔", "💭", "🧐", "❓", "💡", "🎯"],
        "celebration": ["🎊", "🎉", "🥳", "🎈", "🍾", "✨"],
        "warning": ["⚠️", "🚨", "❗", "⚡", "🔴", "📢"],
        "time": ["⏰", "⏱️", "📅", "🕐", "⌛", "⏳"]
    }
    
    suggestions = {}
    
    # Check for keywords
    keywords = {
        "success": ["success", "achievement", "win", "accomplish"],
        "learning": ["learn", "education", "study", "knowledge", "skill"],
        "tech": ["technology", "software", "coding", "ai", "digital", "tech"],
        "business": ["business", "startup", "company", "growth", "revenue"],
        "motivation": ["motivat", "inspir", "passion", "drive", "goal"],
        "team": ["team", "collaboration", "together", "colleague", "partner"],
        "thinking": ["think", "idea", "question", "wonder", "curious"],
        "celebration": ["celebrat", "happy", "excit", "announce", "launch"],
        "warning": ["warning", "alert", "important", "urgent", "critical"],
        "time": ["time", "deadline", "schedule", "today", "now"]
    }
    
    for category, words in keywords.items():
        for word in words:
            if word in topic_lower:
                suggestions[category] = emoji_map[category]
                break
    
    # Default suggestions if no match
    if not suggestions:
        suggestions["general"] = ["✨", "💡", "🚀", "💪", "🎯"]
    
    return suggestions


def calculate_engagement_factors(content: str) -> dict:
    """
    Calculate factors that affect engagement
    
    Args:
        content: Post content
        
    Returns:
        Dictionary with engagement factors
    """
    has_question = "?" in content
    has_cta = any(word in content.lower() for word in [
        "comment", "share", "thoughts", "think", "agree", "what do you"
    ])
    has_emojis = bool(re.search(r'[\U0001F300-\U0001F9FF]', content))
    has_hashtags = bool(re.search(r'#\w+', content))
    
    word_count = count_words(content)
    line_count = len(content.split('\n'))
    
    # Optimal ranges
    optimal_words = 50 <= word_count <= 150
    good_formatting = line_count >= 3
    
    return {
        "has_question": has_question,
        "has_cta": has_cta,
        "has_emojis": has_emojis,
        "has_hashtags": has_hashtags,
        "word_count": word_count,
        "optimal_length": optimal_words,
        "good_formatting": good_formatting,
        "line_count": line_count
    }


def format_hashtags(hashtags: str) -> str:
    """
    Format hashtags string consistently
    
    Args:
        hashtags: Hashtags string (may or may not have #)
        
    Returns:
        Formatted hashtags string
    """
    if not hashtags:
        return ""
    
    # Split and clean
    tags = hashtags.replace(',', ' ').split()
    
    # Ensure each tag starts with #
    formatted_tags = []
    for tag in tags:
        tag = tag.strip()
        if tag and not tag.startswith('#'):
            tag = '#' + tag
        if tag:
            formatted_tags.append(tag)
    
    return ' '.join(formatted_tags)


def get_post_statistics(content: str) -> dict:
    """
    Get comprehensive statistics for a post
    
    Args:
        content: Post content
        
    Returns:
        Dictionary with various statistics
    """
    return {
        "character_count": count_characters(content, include_spaces=True),
        "character_count_no_spaces": count_characters(content, include_spaces=False),
        "word_count": count_words(content),
        "line_count": len(content.split('\n')),
        "sentence_count": len(re.split(r'[.!?]+', content)) - 1,
        "hashtag_count": count_hashtags(content),
        "read_time_seconds": estimate_read_time(content),
        "has_emojis": bool(re.search(r'[\U0001F300-\U0001F9FF]', content)),
        "has_urls": bool(re.search(r'https?://', content))
    }


if __name__ == "__main__":
    # Test utilities
    test_text = "This is a test post about #AI and #MachineLearning. What do you think? 🚀"
    
    print("Testing utility functions:")
    print(f"✓ Word count: {count_words(test_text)}")
    print(f"✓ Character count: {count_characters(test_text)}")
    print(f"✓ Hashtags: {extract_hashtags(test_text)}")
    print(f"✓ Statistics: {get_post_statistics(test_text)}")
    print(f"✓ Engagement factors: {calculate_engagement_factors(test_text)}")
