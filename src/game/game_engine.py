from game.quest_tracker import QuestTracker
from game.character_sheet import CharacterSheet
from llm.ollama_client import OllamaClient, PromptManager
from memory.memory_manager import EnhancedMemoryManager
import sys
import os
import time
import json
from typing import Dict
import re

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))


class UltimateGameEngine:
    """Ultimate AI Dungeon Master with all features"""

    def __init__(self):
        self.memory_manager = EnhancedMemoryManager()
        self.llm_client = OllamaClient()
        self.prompt_manager = PromptManager()
        self.character_sheet = CharacterSheet()
        self.quest_tracker = QuestTracker()
        self.game_started = False
        self.game_stats = {
            'total_turns': 0,
            'avg_response_time': 0,
            'memory_retrievals': 0,
            'npc_interactions': 0,
            'quests_detected': 0,
            'items_found': 0,
            'combat_encounters': 0
        }

    def start_game(self):
        """Initialize enhanced game session"""
        print("=== ULTIMATE AI DUNGEON MASTER ===")
        print("🗡️  Advanced Features Loaded:")
        print("   • Persistent Memory & NPC Relationships")
        print("   • Automatic Quest Tracking")
        print("   • Character Sheet & Progression")
        print("   • Combat & Inventory System")
        print("   • 30+ Turn Stability Testing")
        print("\nStarting your epic adventure...")

        initial_prompt = """Create an exciting fantasy RPG opening that:
1. Sets a vivid, immersive location
2. Introduces the player as an adventurer with basic equipment
3. Presents an initial quest or challenge
4. Mentions NPCs the player can interact with
5. Gives 3-4 clear action options
Keep it engaging but under 200 words."""

        start_time = time.time()
        initial_response = self.llm_client.generate_response(initial_prompt)
        response_time = time.time() - start_time

        print(f"\nDM: {initial_response}")
        print(f"\n[Game initialized in {response_time:.2f}s]")

        # Process initial response
        self.memory_manager.process_turn("", initial_response)
        self.quest_tracker.detect_quest(initial_response, 1)
        self._process_character_updates(initial_response)
        self.game_started = True

        return initial_response

    def process_player_action(self, player_input: str) -> str:
        """Enhanced action processing with all systems"""
        if not self.game_started:
            return "Please start the game first!"

        start_time = time.time()

        # Get context using faster method if available
        if hasattr(self.memory_manager, 'get_context_for_llm_fast'):
            context = self.memory_manager.get_context_for_llm_fast(
                player_input)
        else:
            context = self.memory_manager.get_context_for_llm(player_input)

        self.game_stats['memory_retrievals'] += 1

        # Enhanced prompt with character context
        character_context = self._get_character_context()
        enhanced_context = f"{context}\n{character_context}"

        prompt = self.prompt_manager.build_enhanced_game_prompt(
            player_input, enhanced_context, self.memory_manager.turn_counter
        )

        # Generate response
        ai_response = self.llm_client.generate_response(prompt)

        # Process all systems
        response_time = time.time() - start_time
        self._update_stats(ai_response, response_time)
        self.memory_manager.process_turn(player_input, ai_response)

        # Quest system
        if self.quest_tracker.detect_quest(ai_response, self.memory_manager.turn_counter):
            self.game_stats['quests_detected'] += 1

        completions = self.quest_tracker.check_completion(
            ai_response, self.memory_manager.turn_counter)
        for completion in completions:
            print(f"🎉 {completion}")

        # Character system updates
        self._process_character_updates(ai_response)

        print(
            f"[Turn {self.memory_manager.turn_counter} | {response_time:.1f}s]")

        return ai_response

    def _get_character_context(self) -> str:
        """Get character sheet context for AI"""
        return f"""
=== Character Status ===
Level {self.character_sheet.stats['level']} {self.character_sheet.stats['name']}
Health: {self.character_sheet.stats['health']}/{self.character_sheet.stats['max_health']}
Gold: {self.character_sheet.stats['gold']}
Items: {', '.join(self.character_sheet.inventory[:3])}{'...' if len(self.character_sheet.inventory) > 3 else ''}
Active Quests: {len(self.quest_tracker.active_quests)}
"""

    def _process_character_updates(self, ai_response: str):
        """Process character updates from AI response"""
        response_lower = ai_response.lower()

        # Experience gain
        if any(word in response_lower for word in ['battle', 'victory', 'defeated', 'solved', 'completed']):
            xp = 25
            result = self.character_sheet.gain_experience(xp)
            if 'Level up' in result:
                print(f"🎊 {result}")

        # Item detection
        item_patterns = [
            r"(?:find|discover|pick up|take|grab|obtain|receive)\s+(?:a |an |the )?([a-zA-Z\s]{3,20})",
            r"(?:gives? you|hands? you|offers? you)\s+(?:a |an |the )?([a-zA-Z\s]{3,20})"
        ]

        for pattern in item_patterns:
            matches = re.finditer(pattern, ai_response, re.IGNORECASE)
            for match in matches:
                item = match.group(1).strip().title()
                if len(item) > 2 and not any(word in item.lower() for word in ['damage', 'health', 'you', 'yourself']):
                    result = self.character_sheet.add_item(item)
                    if 'Added' in result:
                        print(f"🎒 {result}")
                        self.game_stats['items_found'] += 1

        # Gold detection
        gold_match = re.search(
            r'(?:gain|earn|find|receive|get)\s+(\d+)\s+(?:gold|coins?)', response_lower)
        if gold_match:
            amount = int(gold_match.group(1))
            self.character_sheet.stats['gold'] += amount
            print(
                f"💰 Gained {amount} gold! Total: {self.character_sheet.stats['gold']}")

        # Damage detection
        damage_match = re.search(
            r'(?:take|suffer|lose)\s+(\d+)\s+(?:damage|health)', response_lower)
        if damage_match:
            damage = int(damage_match.group(1))
            result = self.character_sheet.take_damage(damage)
            print(f"💔 {result}")

    def _update_stats(self, ai_response: str, response_time: float):
        """Update game statistics"""
        self.game_stats['total_turns'] += 1
        self.game_stats['avg_response_time'] = (
            (self.game_stats['avg_response_time'] * (self.game_stats['total_turns'] - 1) + response_time) /
            self.game_stats['total_turns']
        )

        # NPC detection
        if any(name[0].isupper() for name in ai_response.split() if len(name) > 2):
            self.game_stats['npc_interactions'] += 1

        # Combat detection
        combat_words = ['attack', 'fight', 'battle',
                        'combat', 'sword', 'weapon', 'enemy']
        if any(word in ai_response.lower() for word in combat_words):
            self.game_stats['combat_encounters'] += 1

    def get_detailed_stats(self) -> dict:
        """Get comprehensive statistics"""
        quest_stats = self.quest_tracker.get_stats()

        return {
            'game_stats': self.game_stats,
            'character_stats': {
                'level': self.character_sheet.stats['level'],
                'health': f"{self.character_sheet.stats['health']}/{self.character_sheet.stats['max_health']}",
                'gold': self.character_sheet.stats['gold'],
                'items': len(self.character_sheet.inventory),
                'abilities': len(self.character_sheet.abilities)
            },
            'quest_stats': quest_stats,
            'memory_stats': {
                'turn_count': self.memory_manager.turn_counter,
                'working_memory_size': len(self.memory_manager.working_memory.get_memory())
            }
        }

    def run_stability_test(self, num_turns: int = 30) -> dict:
        """Enhanced stability test"""
        print(f"\n🧪 Running {num_turns}-Turn Stability Test...")

        test_actions = [
            "I explore the surrounding area carefully",
            "I search for any interesting items or clues",
            "I approach and talk to any NPCs I see",
            "I examine my equipment and inventory",
            "I look for enemies or dangers nearby",
            "I try to find shelter or a safe place to rest",
            "I listen for any sounds or conversations",
            "I check for tracks or signs of passage",
            "I investigate any notable landmarks or features",
            "I attempt to gather information about quests"
        ]

        start_test_time = time.time()
        test_results = {
            'completed_turns': 0,
            'errors': 0,
            'avg_response_time': 0,
            'total_test_time': 0,
            'quests_found': 0,
            'items_found': 0,
            'npcs_met': 0,
            'responses': []
        }

        initial_quests = len(self.quest_tracker.active_quests)
        initial_items = len(self.character_sheet.inventory)

        for i in range(num_turns):
            try:
                action = test_actions[i % len(test_actions)]
                turn_start = time.time()

                response = self.process_player_action(action)
                response_time = time.time() - turn_start

                test_results['completed_turns'] += 1
                test_results['avg_response_time'] += response_time
                test_results['responses'].append({
                    'turn': i + 1,
                    'action': action,
                    'response': response[:150] + "..." if len(response) > 150 else response,
                    'response_time': response_time
                })

                print(
                    f"Test Turn {i + 1}/{num_turns} ✓ ({response_time:.1f}s)")

            except Exception as e:
                test_results['errors'] += 1
                print(f"❌ Error on turn {i + 1}: {str(e)[:100]}")

        # Calculate final results
        total_test_time = time.time() - start_test_time
        test_results['total_test_time'] = total_test_time
        test_results['avg_response_time'] = test_results['avg_response_time'] / \
            max(1, test_results['completed_turns'])
        test_results['quests_found'] = len(
            self.quest_tracker.active_quests) - initial_quests
        test_results['items_found'] = len(
            self.character_sheet.inventory) - initial_items

        # Display results
        print(f"\n{'='*50}")
        print(f"🧪 STABILITY TEST RESULTS")
        print(f"{'='*50}")
        print(
            f"Completed: {test_results['completed_turns']}/{num_turns} turns")
        print(f"Errors: {test_results['errors']}")
        print(
            f"Success Rate: {(test_results['completed_turns']/num_turns)*100:.1f}%")
        print(
            f"Average Response Time: {test_results['avg_response_time']:.2f}s")
        print(f"Total Test Duration: {total_test_time/60:.1f} minutes")
        print(f"Quests Discovered: {test_results['quests_found']}")
        print(f"Items Found: {test_results['items_found']}")
        print(f"{'='*50}")

        return test_results


def main():
    """Ultimate game interface"""
    game = UltimateGameEngine()

    print("🎮 ULTIMATE AI DUNGEON MASTER")
    print("Commands:")
    print("  'quit' - Exit game")
    print("  'stats' - Show detailed statistics")
    print("  'character' - View character sheet")
    print("  'quests' - View quest log")
    print("  'inventory' - View inventory")
    print("  'test' - Run 30-turn stability test")
    print("  'help' - Show commands")
    print()

    # Start the ultimate adventure
    game.start_game()

    while True:
        try:
            player_input = input("\n🎭 You: ").strip()

            if player_input.lower() == 'quit':
                print("Thanks for playing the Ultimate AI Dungeon Master!")
                break

            elif player_input.lower() == 'stats':
                stats = game.get_detailed_stats()
                print(f"\n📊 GAME STATISTICS")
                print(f"Turns Played: {stats['game_stats']['total_turns']}")
                print(
                    f"Avg Response Time: {stats['game_stats']['avg_response_time']:.1f}s")
                print(f"NPCs Met: {stats['game_stats']['npc_interactions']}")
                print(
                    f"Combat Encounters: {stats['game_stats']['combat_encounters']}")
                print(f"Character Level: {stats['character_stats']['level']}")
                print(f"Items Collected: {stats['character_stats']['items']}")
                print(f"Active Quests: {stats['quest_stats']['active_count']}")
                print(
                    f"Completed Quests: {stats['quest_stats']['completed_count']}")

            elif player_input.lower() == 'character':
                game.character_sheet.display_sheet()

            elif player_input.lower() == 'quests':
                game.quest_tracker.display_quests()

            elif player_input.lower() == 'inventory':
                print(
                    f"\n🎒 INVENTORY ({len(game.character_sheet.inventory)} items):")
                for i, item in enumerate(game.character_sheet.inventory, 1):
                    print(f"  {i}. {item}")

            elif player_input.lower() == 'test':
                game.run_stability_test(30)

            elif player_input.lower() == 'help':
                print("Commands: quit, stats, character, quests, inventory, test, help")
                print("Just type your action to continue the adventure!")

            else:
                response = game.process_player_action(player_input)
                print(f"\n🎭 DM: {response}")

        except KeyboardInterrupt:
            print("\n\nAdventure interrupted! Thanks for playing!")
            break
        except Exception as e:
            print(f"⚠️ Error: {e}")
            print("The adventure continues...")


if __name__ == "__main__":
    main()
