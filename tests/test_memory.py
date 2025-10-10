import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.memory.memory_manager import MemoryManager

class TestMemorySystem(unittest.TestCase):
    
    def setUp(self):
        self.memory_manager = MemoryManager()
    
    def test_working_memory(self):
        """Test working memory functionality"""
        # Add some turns
        for i in range(7):  # More than max_turns (5)
            self.memory_manager.process_turn(
                f"Player input {i}", 
                f"AI response {i}"
            )
        
        # Should only keep last 5
        working_memory = self.memory_manager.working_memory.get_memory()
        self.assertEqual(len(working_memory), 5)
        
        # Should be the most recent ones
        self.assertIn("Player input 6", working_memory[-1]['player_input'])
    
    def test_persistent_memory(self):
        """Test persistent memory storage and retrieval"""
        self.memory_manager.process_turn("I attack the dragon", "The dragon roars!")
        self.memory_manager.process_turn("I cast fireball", "Flames engulf the dragon!")
        
        # Test retrieval
        relevant = self.memory_manager.persistent_memory.retrieve_relevant_turns("dragon")
        self.assertGreater(len(relevant), 0)
    
    def test_context_building(self):
        """Test context building for LLM"""
        self.memory_manager.process_turn("Hello", "Welcome to the adventure!")
        self.memory_manager.process_turn("I explore the forest", "You find a clearing!")
        
        context = self.memory_manager.get_context_for_llm("What do I see?")
        self.assertIn("Welcome to the adventure", context)
        self.assertIn("forest", context)

if __name__ == '__main__':
    unittest.main()
