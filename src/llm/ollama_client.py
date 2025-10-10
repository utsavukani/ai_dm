import requests
import json

class OllamaClient:
    """Interface for Ollama LLM API"""
    def __init__(self, base_url="http://localhost:11434", model="llama3.2"):
        self.base_url = base_url
        self.model = model
    
    def generate_response(self, prompt: str, system_prompt: str = None) -> str:
        """Generate response from Ollama"""
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": system_prompt or self.get_default_system_prompt(),
            "stream": False,
            "options": {
                "temperature": 0.8,
                "top_p": 0.9,
                "max_tokens": 500
            }
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            
            result = response.json()
            return result.get('response', 'Error generating response')
            
        except requests.RequestException as e:
            return f"Error connecting to Ollama: {e}"
    
    def get_default_system_prompt(self) -> str:
        return """You are an AI Dungeon Master for a tabletop RPG. You must:
1. Maintain narrative consistency across all interactions
2. Remember and reference past events appropriately
3. Create immersive, engaging story responses
4. Keep responses concise but descriptive
5. Always ask what the player wants to do next
6. Never contradict established story elements"""

class PromptManager:
    """Enhanced prompt management with better consistency prompts"""
    
    @staticmethod
    def build_enhanced_game_prompt(player_input: str, context: str, turn_number: int) -> str:
        """Build enhanced prompt for better consistency"""
        prompt = f"""
{context}

=== Current Turn {turn_number} ===
Player Action: {player_input}

CRITICAL INSTRUCTIONS for the Dungeon Master:
1. CONSISTENCY: Always refer to established facts from the context above
2. MEMORY: Reference past events, characters, and locations when relevant
3. NPCS: If mentioning characters, use their established names and relationships
4. CONTINUITY: Make sure your response flows logically from recent events
5. ENGAGEMENT: Ask what the player wants to do next
6. CONCISENESS: Keep responses focused and under 200 words

As the Dungeon Master, provide a response that:
- Acknowledges the player's action appropriately
- Describes realistic consequences based on established story elements
- Maintains absolute consistency with all past events mentioned above
- References relevant NPCs and their known relationships/traits
- Sets up the next scene or choice for the player
- Ends by asking what the player wants to do next

Your Response:"""
        
        return prompt
    
    @staticmethod
    def build_game_prompt(player_input: str, context: str) -> str:
        """Backward compatibility method"""
        return PromptManager.build_enhanced_game_prompt(player_input, context, 1)

