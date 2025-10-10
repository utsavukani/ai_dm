import re
import json
from typing import List, Dict
from datetime import datetime


class QuestTracker:
    """Automatic quest detection and tracking system"""

    def __init__(self):
        self.active_quests: List[Dict] = []
        self.completed_quests: List[Dict] = []
        self.quest_counter = 0

    def detect_quest(self, ai_response: str, turn_number: int) -> bool:
        """Automatically detect quests from AI responses"""
        quest_patterns = [
            r"(?:find|retrieve|bring|fetch|collect)\s+(?:the\s+)?([^.!?]+)",
            r"(?:defeat|kill|slay|destroy)\s+(?:the\s+)?([^.!?]+)",
            r"(?:deliver|take|carry)\s+(?:this|the)\s+([^.!?\s]+)\s+to\s+([^.!?]+)",
            r"(?:help|assist|aid)\s+([^.!?]+?)(?:\s+with\s+([^.!?]+))?",
            r"(?:quest|task|mission|job):\s*([^.!?]+)",
            r"(?:rescue|save|free)\s+([^.!?]+)",
            r"(?:explore|investigate|search)\s+(?:the\s+)?([^.!?]+)"
        ]

        detected = False
        for pattern in quest_patterns:
            matches = re.finditer(pattern, ai_response, re.IGNORECASE)
            for match in matches:
                quest_description = match.group(1).strip()
                if len(quest_description) > 5 and len(quest_description) < 100:  # Reasonable length
                    if not self._is_duplicate_quest(quest_description):
                        self._add_quest(quest_description, turn_number)
                        detected = True

        return detected

    def _is_duplicate_quest(self, description: str) -> bool:
        """Check if quest already exists"""
        for quest in self.active_quests:
            if self._similarity(quest['description'].lower(), description.lower()) > 0.7:
                return True
        return False

    def _similarity(self, a: str, b: str) -> float:
        """Simple similarity check"""
        words_a = set(a.split())
        words_b = set(b.split())
        intersection = words_a.intersection(words_b)
        union = words_a.union(words_b)
        return len(intersection) / len(union) if union else 0

    def _add_quest(self, description: str, turn_number: int):
        """Add new quest"""
        self.quest_counter += 1
        quest = {
            'id': self.quest_counter,
            'description': description,
            'status': 'active',
            'start_turn': turn_number,
            'created_at': datetime.now().isoformat(),
            'progress': []
        }
        self.active_quests.append(quest)
        print(f"📋 New Quest Detected: {description}")

    def complete_quest(self, quest_id: int, turn_number: int) -> str:
        """Mark quest as completed"""
        for quest in self.active_quests:
            if quest['id'] == quest_id:
                quest['status'] = 'completed'
                quest['completion_turn'] = turn_number
                quest['completed_at'] = datetime.now().isoformat()
                self.completed_quests.append(quest)
                self.active_quests.remove(quest)
                return f"✅ Quest Completed: {quest['description']}"
        return f"Quest {quest_id} not found."

    def add_progress(self, quest_id: int, progress_note: str):
        """Add progress note to quest"""
        for quest in self.active_quests:
            if quest['id'] == quest_id:
                quest['progress'].append({
                    'note': progress_note,
                    'timestamp': datetime.now().isoformat()
                })
                return f"Progress added to quest {quest_id}"
        return f"Quest {quest_id} not found."

    def check_completion(self, ai_response: str, turn_number: int) -> List[str]:
        """Check if any quests might be completed based on AI response"""
        completion_results = []
        completion_keywords = [
            'completed', 'finished', 'done', 'accomplished', 'achieved',
            'successful', 'delivered', 'defeated', 'found', 'rescued'
        ]

        response_lower = ai_response.lower()
        for quest in self.active_quests.copy():  # Copy to avoid modification during iteration
            quest_words = set(quest['description'].lower().split())
            if any(keyword in response_lower for keyword in completion_keywords):
                # Check if quest-related words appear in response
                response_words = set(response_lower.split())
                overlap = quest_words.intersection(response_words)
                if len(overlap) >= 2:  # At least 2 words match
                    result = self.complete_quest(quest['id'], turn_number)
                    completion_results.append(result)

        return completion_results

    def display_quests(self):
        """Display all quests"""
        print(f"\n{'='*40}")
        print(f"QUEST LOG")
        print(f"{'='*40}")

        if self.active_quests:
            print(f"\n🔥 ACTIVE QUESTS ({len(self.active_quests)}):")
            for quest in self.active_quests:
                print(f"  [{quest['id']}] {quest['description']}")
                if quest['progress']:
                    print(f"      Progress: {len(quest['progress'])} updates")
        else:
            print("\n🔥 ACTIVE QUESTS: None")

        if self.completed_quests:
            print(f"\n✅ COMPLETED QUESTS ({len(self.completed_quests)}):")
            for quest in self.completed_quests[-5:]:  # Show last 5
                print(f"  [{quest['id']}] {quest['description']}")

        print(f"{'='*40}")

    def get_stats(self) -> Dict:
        """Get quest statistics"""
        return {
            'active_count': len(self.active_quests),
            'completed_count': len(self.completed_quests),
            'total_quests': self.quest_counter,
            'completion_rate': len(self.completed_quests) / max(1, self.quest_counter) * 100
        }
