import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class ContentGenerator:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None

    def generate_post(self, topic=None):
        if not self.model:
            return "Error: No API key provided for Gemini."
        
        target_topic = topic or os.getenv("POST_TOPIC", "AcreetionOS")
        
        try:
            # Phase 1: Brainstorming
            brainstorm_prompt = (
                f"You are a visionary tech expert. Brainstorm 3 groundbreaking, futuristic features "
                f"for {target_topic}. Focus on innovation, speed, and user sovereignty."
            )
            ideas = self.model.generate_content(brainstorm_prompt).text
            
            # Phase 2: Refinement (The "Talk to itself" part)
            refinement_prompt = (
                f"You are a critical tech reviewer. Review these {topic} feature ideas:\n{ideas}\n\n"
                f"Pick the single most 'viral' and impressive feature and explain why it's better than current OS standards."
            )
            refined_focus = self.model.generate_content(refinement_prompt).text
            
            # Phase 3: Final Post Creation
            final_prompt = (
                f"Based on this refined concept: {refined_focus}\n\n"
                f"Write a high-energy, futuristic social media post about {topic}. "
                f"Include 3-5 hashtags, emojis, and a call to action. Keep it under 280 characters for Twitter compatibility."
            )
            response = self.model.generate_content(final_prompt)
            return response.text.strip()
            
        except Exception as e:
            return f"Error generating content: {str(e)}"
