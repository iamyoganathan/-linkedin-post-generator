"""
Prompt templates for LinkedIn post generation
"""

# System prompt for general context
SYSTEM_PROMPT = """You are an expert LinkedIn content creator with years of experience in crafting 
engaging, professional posts that drive high engagement. You understand LinkedIn's algorithm, 
best practices for professional networking, and how to write compelling content that resonates 
with professionals across various industries."""

# Post generation prompts based on tone
POST_GENERATION_PROMPTS = {
    "professional": """Create a professional LinkedIn post about: {topic}

Requirements:
- Length: {length} (Short: 2-4 lines, Medium: 5-8 lines, Long: 10-15 lines)
- Tone: Professional, authoritative, and insightful
- Include relevant industry terminology
- Start with a strong hook
- End with a thought-provoking question or call-to-action
- Use line breaks for readability
- NO hashtags in the main text

Write the post now:""",

    "casual": """Create a casual but professional LinkedIn post about: {topic}

Requirements:
- Length: {length} (Short: 2-4 lines, Medium: 5-8 lines, Long: 10-15 lines)
- Tone: Friendly, conversational, relatable
- Use simple language and personal anecdotes
- Start with a relatable hook
- Add 1-2 relevant emojis (use sparingly)
- End with an engaging question
- Use line breaks for readability
- NO hashtags in the main text

Write the post now:""",

    "motivational": """Create an inspiring, motivational LinkedIn post about: {topic}

Requirements:
- Length: {length} (Short: 2-4 lines, Medium: 5-8 lines, Long: 10-15 lines)
- Tone: Uplifting, inspiring, encouraging
- Include a powerful message or lesson
- Use storytelling elements
- Start with an attention-grabbing statement
- End with an inspiring call-to-action
- Use line breaks for readability
- Add 1-2 relevant emojis
- NO hashtags in the main text

Write the post now:""",

    "educational": """Create an educational LinkedIn post about: {topic}

Requirements:
- Length: {length} (Short: 2-4 lines, Medium: 5-8 lines, Long: 10-15 lines)
- Tone: Informative, authoritative, helpful
- Share valuable insights or knowledge
- Use bullet points or numbered lists if appropriate
- Include actionable tips or key takeaways
- Start with a value proposition
- End with an invitation to discuss or share
- Use line breaks for readability
- NO hashtags in the main text

Write the post now:""",

    "storytelling": """Create a compelling story-based LinkedIn post about: {topic}

Requirements:
- Length: {length} (Short: 2-4 lines, Medium: 5-8 lines, Long: 10-15 lines)
- Tone: Narrative, engaging, personal
- Follow a story arc (beginning, middle, end)
- Include specific details and emotions
- Make it relatable and authentic
- Start with a hook that draws readers in
- End with a lesson or reflection
- Use line breaks for readability
- Add 1-2 relevant emojis
- NO hashtags in the main text

Write the post now:""",

    "thought-leadership": """Create a thought-leadership LinkedIn post about: {topic}

Requirements:
- Length: {length} (Short: 2-4 lines, Medium: 5-8 lines, Long: 10-15 lines)
- Tone: Authoritative, visionary, intellectually stimulating
- Share unique insights or perspectives
- Challenge conventional thinking
- Use data or trends if relevant
- Start with a bold statement or question
- End with a forward-looking perspective
- Use line breaks for readability
- NO hashtags in the main text

Write the post now:"""
}

# Hashtag generation prompt
HASHTAG_PROMPT = """Generate 8-10 relevant and trending LinkedIn hashtags for this post topic: {topic}

Requirements:
- Mix of popular hashtags (100k+ followers) and niche hashtags (10k-50k followers)
- Relevant to the topic and professional context
- Include industry-specific hashtags
- Format: Return ONLY the hashtags separated by spaces, starting with #
- Example format: #Marketing #DigitalMarketing #ContentStrategy

Generate hashtags now:"""

# Hook generation prompt
HOOK_GENERATION_PROMPT = """Generate 3 attention-grabbing opening hooks for a LinkedIn post about: {topic}

Each hook should be:
- Maximum 1-2 lines
- Immediately engaging
- Use one of these techniques: question, bold statement, surprising fact, or personal confession
- Professional yet captivating

Format:
Hook 1: [first hook]
Hook 2: [second hook]
Hook 3: [third hook]

Generate hooks now:"""

# Post refinement prompts
REFINEMENT_PROMPTS = {
    "make_shorter": """Rewrite this LinkedIn post to be shorter while keeping the core message:

Original post:
{post}

Requirements:
- Cut length by 30-40%
- Keep the main message and impact
- Maintain readability
- NO hashtags

Shortened post:""",

    "make_longer": """Expand this LinkedIn post with more details and depth:

Original post:
{post}

Requirements:
- Add relevant details, examples, or insights
- Increase length by 40-50%
- Maintain flow and engagement
- NO hashtags

Expanded post:""",

    "add_storytelling": """Rewrite this LinkedIn post using storytelling elements:

Original post:
{post}

Requirements:
- Add narrative structure
- Include personal or relatable elements
- Make it more engaging
- Maintain the core message
- NO hashtags

Rewritten post:""",

    "more_professional": """Make this LinkedIn post more professional and polished:

Original post:
{post}

Requirements:
- Elevate the language
- Add industry credibility
- Remove overly casual elements
- Maintain authenticity
- NO hashtags

Professional version:""",

    "add_cta": """Add a compelling call-to-action to this LinkedIn post:

Original post:
{post}

Requirements:
- Add an engaging CTA at the end
- Encourage comments, shares, or discussion
- Make it feel natural
- NO hashtags

Post with CTA:"""
}

# Post type templates
POST_TYPE_PROMPTS = {
    "announcement": """Create a LinkedIn announcement post about: {topic}

This should announce news, updates, or achievements in a professional and exciting way.
Length: {length}
Tone: {tone}

Include:
- Clear announcement
- Key details
- Why it matters
- Call to action

NO hashtags in the main text.
Write the post:""",

    "tips": """Create a LinkedIn tips/advice post about: {topic}

Share actionable tips or best practices.
Length: {length}
Tone: {tone}

Format as:
- Introduction
- 3-5 numbered tips
- Quick summary
- Engagement question

NO hashtags in the main text.
Write the post:""",

    "question": """Create a LinkedIn discussion post with a thought-provoking question about: {topic}

Length: {length}
Tone: {tone}

Include:
- Brief context (2-3 lines)
- Main question that sparks discussion
- Why this matters
- Invitation to share thoughts

NO hashtags in the main text.
Write the post:""",

    "achievement": """Create a LinkedIn post celebrating an achievement related to: {topic}

Length: {length}
Tone: {tone}

Include:
- The achievement
- Brief journey/context
- Gratitude or lesson learned
- Humble brag done right

NO hashtags in the main text.
Write the post:""",

    "industry_insight": """Create a LinkedIn post sharing industry insights about: {topic}

Length: {length}
Tone: {tone}

Include:
- Current trend or observation
- Your analysis or perspective
- What it means for professionals
- Engaging question

NO hashtags in the main text.
Write the post:"""
}

# Engagement predictor criteria prompt
ENGAGEMENT_SCORE_PROMPT = """Analyze this LinkedIn post and provide an engagement prediction score:

Post:
{post}

Evaluate based on:
1. Hook quality (0-25 points): Is the opening line attention-grabbing?
2. Content value (0-25 points): Does it provide value, insights, or entertainment?
3. Readability (0-20 points): Line breaks, length, structure
4. Call-to-action (0-15 points): Does it encourage engagement?
5. Authenticity (0-15 points): Does it feel genuine and relatable?

Respond in this format only:
Hook: [score]/25 - [brief reason]
Content: [score]/25 - [brief reason]
Readability: [score]/20 - [brief reason]
CTA: [score]/15 - [brief reason]
Authenticity: [score]/15 - [brief reason]
Total: [total]/100
Prediction: [Poor/Fair/Good/Excellent]"""


def get_post_prompt(tone, topic, length, post_type="general"):
    """
    Get the appropriate prompt based on parameters
    
    Args:
        tone: The tone of the post (professional, casual, etc.)
        topic: The topic of the post
        length: Desired length (short, medium, long)
        post_type: Type of post (general, announcement, tips, etc.)
    
    Returns:
        Formatted prompt string
    """
    if post_type != "general" and post_type in POST_TYPE_PROMPTS:
        return POST_TYPE_PROMPTS[post_type].format(
            topic=topic,
            length=length,
            tone=tone
        )
    
    if tone.lower() in POST_GENERATION_PROMPTS:
        return POST_GENERATION_PROMPTS[tone.lower()].format(
            topic=topic,
            length=length
        )
    
    # Default to professional if tone not found
    return POST_GENERATION_PROMPTS["professional"].format(
        topic=topic,
        length=length
    )


def get_hashtag_prompt(topic):
    """Get hashtag generation prompt"""
    return HASHTAG_PROMPT.format(topic=topic)


def get_hook_prompt(topic):
    """Get hook generation prompt"""
    return HOOK_GENERATION_PROMPT.format(topic=topic)


def get_refinement_prompt(refinement_type, post):
    """Get refinement prompt"""
    if refinement_type in REFINEMENT_PROMPTS:
        return REFINEMENT_PROMPTS[refinement_type].format(post=post)
    return None


def get_engagement_score_prompt(post):
    """Get engagement scoring prompt"""
    return ENGAGEMENT_SCORE_PROMPT.format(post=post)
