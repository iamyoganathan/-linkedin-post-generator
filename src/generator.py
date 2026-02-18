"""
LinkedIn Post Generator using Groq API
"""

import os
from groq import Groq
from dotenv import load_dotenv
from src.prompts import (
    SYSTEM_PROMPT,
    get_post_prompt,
    get_hashtag_prompt,
    get_hook_prompt,
    get_refinement_prompt,
    get_engagement_score_prompt
)

# Load environment variables
load_dotenv()


class LinkedInPostGenerator:
    """Main class for generating LinkedIn posts using Groq API"""
    
    def __init__(self, api_key=None):
        """
        Initialize the generator with Groq API
        
        Args:
            api_key: Groq API key (optional, will use env variable if not provided)
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key or self.api_key == "your_groq_api_key_here":
            raise ValueError("Please set your GROQ_API_KEY in the .env file")
        
        self.client = Groq(api_key=self.api_key)
        self.model = "llama-3.3-70b-versatile"  # Latest model for content generation
        
    def _call_groq_api(self, prompt, system_prompt=SYSTEM_PROMPT, temperature=0.7, max_tokens=1000):
        """
        Internal method to call Groq API
        
        Args:
            prompt: User prompt
            system_prompt: System context prompt
            temperature: Creativity level (0-2)
            max_tokens: Maximum response length
            
        Returns:
            Generated text response
        """
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return chat_completion.choices[0].message.content.strip()
        
        except Exception as e:
            raise Exception(f"Error calling Groq API: {str(e)}")
    
    def generate_post(self, topic, tone="professional", length="medium", post_type="general"):
        """
        Generate a LinkedIn post
        
        Args:
            topic: The main topic or subject
            tone: Tone of the post (professional, casual, motivational, etc.)
            length: Length of post (short, medium, long)
            post_type: Type of post (general, announcement, tips, question, etc.)
            
        Returns:
            Generated post text
        """
        if not topic or topic.strip() == "":
            raise ValueError("Topic cannot be empty")
        
        prompt = get_post_prompt(tone, topic, length, post_type)
        post = self._call_groq_api(prompt, temperature=0.8, max_tokens=1500)
        
        return post
    
    def generate_hashtags(self, topic):
        """
        Generate relevant hashtags for the topic
        
        Args:
            topic: The topic or post content
            
        Returns:
            String of hashtags
        """
        prompt = get_hashtag_prompt(topic)
        hashtags = self._call_groq_api(prompt, temperature=0.6, max_tokens=200)
        
        # Clean up the response
        hashtags = hashtags.strip()
        if not hashtags.startswith("#"):
            # Extract hashtags if the response contains extra text
            words = hashtags.split()
            hashtags = " ".join([word for word in words if word.startswith("#")])
        
        return hashtags
    
    def generate_hooks(self, topic):
        """
        Generate attention-grabbing opening hooks
        
        Args:
            topic: The topic for hooks
            
        Returns:
            List of 3 hooks
        """
        prompt = get_hook_prompt(topic)
        response = self._call_groq_api(prompt, temperature=0.9, max_tokens=300)
        
        # Parse the hooks from response
        hooks = []
        for line in response.split("\n"):
            if line.strip().startswith("Hook"):
                hook_text = line.split(":", 1)[1].strip() if ":" in line else line
                hooks.append(hook_text)
        
        return hooks if hooks else [response]
    
    def refine_post(self, post, refinement_type):
        """
        Refine an existing post
        
        Args:
            post: The original post text
            refinement_type: Type of refinement (make_shorter, make_longer, etc.)
            
        Returns:
            Refined post text
        """
        prompt = get_refinement_prompt(refinement_type, post)
        if not prompt:
            raise ValueError(f"Invalid refinement type: {refinement_type}")
        
        refined_post = self._call_groq_api(prompt, temperature=0.7, max_tokens=1500)
        return refined_post
    
    def generate_variations(self, topic, tone="professional", length="medium", count=3):
        """
        Generate multiple variations of a post
        
        Args:
            topic: The main topic
            tone: Tone of the posts
            length: Length of posts
            count: Number of variations (max 3)
            
        Returns:
            List of post variations
        """
        variations = []
        temperatures = [0.7, 0.85, 0.95]  # Different creativity levels
        
        for i in range(min(count, 3)):
            prompt = get_post_prompt(tone, topic, length)
            post = self._call_groq_api(prompt, temperature=temperatures[i], max_tokens=1500)
            variations.append(post)
        
        return variations
    
    def predict_engagement(self, post):
        """
        Predict engagement score for a post
        
        Args:
            post: The post text to analyze
            
        Returns:
            Dictionary with scores and prediction
        """
        prompt = get_engagement_score_prompt(post)
        response = self._call_groq_api(prompt, temperature=0.3, max_tokens=500)
        
        # Parse the response
        result = {
            "hook": 0,
            "content": 0,
            "readability": 0,
            "cta": 0,
            "authenticity": 0,
            "total": 0,
            "prediction": "Unknown",
            "details": response
        }
        
        try:
            lines = response.split("\n")
            for line in lines:
                line = line.strip()
                if line.startswith("Hook:"):
                    result["hook"] = int(line.split("/")[0].split(":")[-1].strip())
                elif line.startswith("Content:"):
                    result["content"] = int(line.split("/")[0].split(":")[-1].strip())
                elif line.startswith("Readability:"):
                    result["readability"] = int(line.split("/")[0].split(":")[-1].strip())
                elif line.startswith("CTA:"):
                    result["cta"] = int(line.split("/")[0].split(":")[-1].strip())
                elif line.startswith("Authenticity:"):
                    result["authenticity"] = int(line.split("/")[0].split(":")[-1].strip())
                elif line.startswith("Total:"):
                    result["total"] = int(line.split("/")[0].split(":")[-1].strip())
                elif line.startswith("Prediction:"):
                    result["prediction"] = line.split(":", 1)[1].strip()
        except:
            pass
        
        return result
    
    def add_emojis(self, post, topic):
        """
        Suggest relevant emojis for the post
        
        Args:
            post: The post text
            topic: The topic
            
        Returns:
            Post with added emojis
        """
        prompt = f"""Add 2-3 relevant and professional emojis to this LinkedIn post. 
Place them naturally where they enhance the message. Don't overdo it.

Topic: {topic}
Post:
{post}

Return the post with emojis added:"""
        
        post_with_emojis = self._call_groq_api(prompt, temperature=0.6, max_tokens=1500)
        return post_with_emojis
    
    def generate_cta(self, topic):
        """
        Generate call-to-action suggestions
        
        Args:
            topic: The topic
            
        Returns:
            List of CTA suggestions
        """
        prompt = f"""Generate 3 engaging call-to-action (CTA) statements for a LinkedIn post about: {topic}

Each CTA should:
- Encourage engagement (comments, shares, discussion)
- Be natural and not pushy
- Be 1 line

Format:
1. [CTA 1]
2. [CTA 2]
3. [CTA 3]"""
        
        response = self._call_groq_api(prompt, temperature=0.7, max_tokens=300)
        
        # Parse CTAs
        ctas = []
        for line in response.split("\n"):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith("-")):
                cta = line.split(".", 1)[1].strip() if "." in line else line.strip("- ")
                ctas.append(cta)
        
        return ctas if ctas else [response]


# Utility function to test API connection
def test_api_connection(api_key=None):
    """
    Test if Groq API connection works
    
    Args:
        api_key: Optional API key to test
        
    Returns:
        Boolean indicating success
    """
    try:
        generator = LinkedInPostGenerator(api_key)
        # Try a simple generation
        test_response = generator._call_groq_api(
            "Say 'API connection successful'",
            system_prompt="You are a test assistant.",
            max_tokens=50
        )
        return True, "Connection successful!"
    except Exception as e:
        return False, f"Connection failed: {str(e)}"


if __name__ == "__main__":
    # Test the generator
    try:
        generator = LinkedInPostGenerator()
        print("✓ Generator initialized successfully")
        
        # Test post generation
        test_post = generator.generate_post(
            topic="The importance of continuous learning in tech",
            tone="professional",
            length="medium"
        )
        print("\n✓ Test post generated:")
        print(test_post)
        
    except Exception as e:
        print(f"✗ Error: {e}")
