# API Documentation

## Overview

This document provides comprehensive API documentation for the AI Dungeon Master system, including class descriptions, method documentation, database schema, and configuration options.

---

## Core Classes

### EnhancedGameEngine

**Location**: `src/game/game_engine.py`

The main orchestrator class that manages all game systems including memory, AI client, character progression, and quest tracking.

#### Constructor
```python
def __init__(self):
    """Initialize the enhanced game engine with all subsystems"""
```

#### Key Methods

##### `start_game() -> str`
Initializes a new game session with AI-generated opening scene.

**Returns**: Initial story response from AI
**Side Effects**: 
- Creates initial memory entry
- Sets `game_started = True`
- Processes any initial quests or character updates

##### `process_player_action(player_input: str) -> str`
Processes a single player action through the complete game pipeline.

**Parameters**:
- `player_input`: Natural language player action

**Returns**: AI-generated story response
**Side Effects**:
- Updates all memory systems
- Processes quest detection/completion
- Updates character sheet
- Increments turn counter

##### `get_detailed_stats() -> Dict`
Returns comprehensive game statistics.

**Returns**: Dictionary containing:
- `game_stats`: Turn count, response times, interactions
- `character_stats`: Level, health, inventory count
- `quest_stats`: Active/completed quest counts
- `memory_stats`: Memory system metrics

##### `run_stability_test(num_turns: int = 30) -> Dict`
Executes automated stability testing with predefined actions.

**Parameters**:
- `num_turns`: Number of test turns to execute

**Returns**: Test results including success rate, performance metrics

---

### EnhancedMemoryManager

**Location**: `src/memory/memory_manager.py`

Manages the triple-layered memory system providing consistent story context.

#### Sub-Components

##### WorkingMemory
Short-term memory buffer maintaining last 5 turns with summarization.

**Key Methods**:
- `add_turn(player_input, ai_response, context)`: Add new turn to buffer
- `get_recent_context()`: Build context string from recent turns
- `_extract_key_events(player_input, ai_response)`: Extract important events

##### NPCMemoryManager  
Individual NPC relationship and personality tracking system.

**Database Tables**: `npcs`, `npc_interactions`

**Key Methods**:
- `add_or_update_npc(name, turn_number, context)`: Create or update NPC
- `get_npc_memory(name)`: Retrieve complete NPC profile
- `add_npc_interaction(npc_id, turn, action, response)`: Log interaction

##### EnhancedPersistentMemory
Long-term memory with smart retrieval and importance scoring.

**Database Tables**: `game_turns`, `story_summaries`

**Key Methods**:
- `store_turn(turn_data, turn_number)`: Store turn with metadata
- `retrieve_relevant_turns(query, limit)`: Smart context retrieval
- `_calculate_importance(input, response)`: Score turn importance

#### Main Methods

##### `process_turn(player_input: str, ai_response: str, context: Dict = None)`
Processes a turn through all memory subsystems.

**Parameters**:
- `player_input`: Player's action text
- `ai_response`: AI's story response  
- `context`: Optional additional context

**Side Effects**:
- Updates working memory buffer
- Stores in persistent memory with importance scoring
- Processes NPCs mentioned in response
- Increments turn counter

##### `get_context_for_llm(current_input: str) -> str`
Builds optimized context string for AI generation.

**Parameters**:
- `current_input`: Current player input for relevance matching

**Returns**: Context string containing:
- Recent working memory turns
- Relevant historical events
- Applicable NPC relationship data

---

### OllamaClient

**Location**: `src/llm/ollama_client.py`

Handles communication with local Ollama AI server with error handling and optimization.

#### Constructor
```python
def __init__(self, base_url="http://localhost:11434", model="llama3.2"):
    """Initialize Ollama client with server connection"""
```

#### Key Methods

##### `generate_response(prompt: str, system_prompt: str = None) -> str`
Generates AI response with retry logic and optimization.

**Parameters**:
- `prompt`: Complete prompt including context and player action
- `system_prompt`: Optional system instructions (uses default if None)

**Returns**: AI-generated story response
**Features**:
- 3-attempt retry with progressive fallback
- Connection reuse via requests.Session  
- Optimized parameters for speed/quality balance

---

### CharacterSheet

**Location**: `src/game/character_sheet.py`

Manages player character statistics, inventory, and progression.

#### Attributes
```python
stats = {
    'name': str,
    'level': int, 
    'health': int,
    'max_health': int,
    'experience': int,
    'gold': int,
    'strength': int,
    'intelligence': int, 
    'charisma': int
}
inventory: List[str]
abilities: List[str]
status_effects: List[str]
```

#### Key Methods

##### `add_item(item: str) -> str`
Adds item to inventory if not duplicate.

##### `gain_experience(xp: int) -> str` 
Adds XP and handles automatic level-ups.

##### `take_damage(damage: int) -> str`
Applies damage with health bounds checking.

##### `display_sheet()`
Outputs formatted character information.

---

### QuestTracker

**Location**: `src/game/quest_tracker.py`

Automatically detects, tracks, and manages quest progression.

#### Quest Data Structure
```python
quest = {
    'id': int,
    'description': str,
    'status': str,  # 'active' or 'completed'
    'start_turn': int,
    'created_at': str,
    'progress': List[Dict]
}
```

#### Key Methods

##### `detect_quest(ai_response: str, turn_number: int) -> bool`
Scans AI response for quest-giving language patterns.

**Patterns Detected**:
- "find/retrieve/bring/fetch X"
- "defeat/kill/slay X" 
- "deliver X to Y"
- "help/assist X"
- "rescue/save/free X"

##### `check_completion(ai_response: str, turn_number: int) -> List[str]`
Analyzes response for quest completion indicators.

##### `display_quests()`
Shows organized quest log with active and completed sections.

---

## Database Schema

### SQLite Database: `data/memory.db`

#### Table: `game_turns`
Stores all game turns with metadata and smart retrieval features.

```sql
CREATE TABLE game_turns (
    id TEXT PRIMARY KEY,
    timestamp TEXT,
    turn_number INTEGER,
    player_input TEXT,
    ai_response TEXT, 
    context TEXT,
    importance_score REAL DEFAULT 1.0,
    summary TEXT,
    key_entities TEXT
);
```

**Indexes**: `turn_number`, `importance_score`

#### Table: `story_summaries`  
Periodic story summaries for long-term memory compression.

```sql
CREATE TABLE story_summaries (
    id TEXT PRIMARY KEY,
    turn_range TEXT,
    summary TEXT,
    key_events TEXT,
    timestamp TEXT
);
```

#### Table: `npcs`
Individual NPC profiles and relationship tracking.

```sql
CREATE TABLE npcs (
    npc_id TEXT PRIMARY KEY,
    name TEXT,
    first_met_turn INTEGER,
    personality_traits TEXT,
    relationship_status TEXT DEFAULT 'neutral',
    last_interaction_turn INTEGER,
    memory_summary TEXT,
    interaction_count INTEGER DEFAULT 0
);
```

#### Table: `npc_interactions`
Detailed log of all NPC interactions.

```sql
CREATE TABLE npc_interactions (
    id TEXT PRIMARY KEY,
    npc_id TEXT,
    turn_number INTEGER,
    player_action TEXT,
    npc_response TEXT,
    relationship_change TEXT,
    timestamp TEXT,
    FOREIGN KEY (npc_id) REFERENCES npcs (npc_id)
);
```

---

## Configuration Options

### Ollama Client Configuration

#### Server Settings
```python
OllamaClient(
    base_url="http://localhost:11434",  # Ollama server URL
    model="llama3.2"                    # AI model name
)
```

#### Generation Parameters
```python
"options": {
    "num_predict": 200,        # Max tokens to generate
    "temperature": 0.7,        # Randomness (0.0-1.0)
    "top_p": 0.9,             # Nucleus sampling threshold
    "num_ctx": 2048,          # Context window size
    "num_batch": 512,         # Batch size for processing
    "num_thread": 8           # CPU threads to use
}
```

### Memory System Configuration

#### Working Memory Settings
```python
WorkingMemory(
    max_turns=5              # Buffer size for recent turns
)
```

#### Persistent Memory Settings
```python
EnhancedPersistentMemory(
    db_path="data/memory.db" # Database file location
)
```

#### Importance Scoring Weights
```python
# High importance keywords (+2.0 points)
high_importance_words = [
    'fight', 'battle', 'death', 'quest', 'treasure', 
    'magic', 'dragon', 'king', 'princess'
]

# Medium importance keywords (+1.0 points)  
medium_importance_words = [
    'npc', 'character', 'item', 'place', 
    'meet', 'find', 'discover'
]
```

### Character System Configuration

#### Starting Stats
```python
default_stats = {
    'name': 'Adventurer',
    'level': 1,
    'health': 100,
    'max_health': 100,
    'experience': 0,
    'gold': 50,
    'strength': 10,
    'intelligence': 10,
    'charisma': 10
}
```

#### Level Progression
```python
# XP required for next level
xp_required = current_level * 100

# Stat gains per level
health_gain = 20
attribute_gain = 2  # strength, intelligence
charisma_gain = 1
```

### Quest Detection Configuration  

#### Detection Patterns
```python
quest_patterns = [
    r"(?:find|retrieve|bring|fetch|collect)\s+(?:the\s+)?([^.!?]+)",
    r"(?:defeat|kill|slay|destroy)\s+(?:the\s+)?([^.!?]+)", 
    r"(?:deliver|take|carry)\s+(?:this|the)\s+([^.!?\s]+)\s+to\s+([^.!?]+)",
    r"(?:help|assist|aid)\s+([^.!?]+?)(?:\s+with\s+([^.!?]+))?",
    r"(?:quest|task|mission|job):\s*([^.!?]+)",
    r"(?:rescue|save|free)\s+([^.!?]+)",
    r"(?:explore|investigate|search)\s+(?:the\s+)?([^.!?]+)"
]
```

#### Completion Detection
```python
completion_keywords = [
    'completed', 'finished', 'done', 'accomplished', 'achieved',
    'successful', 'delivered', 'defeated', 'found', 'rescued'
]
```

---

## Performance Tuning

### Response Time Optimization

#### Client-Side Optimizations
- Connection pooling via `requests.Session`
- Reduced context window size (`num_ctx: 2048`)
- Optimized token limits (`num_predict: 200`)
- Multi-threading (`num_thread: 8`)

#### Memory System Optimizations
- Context truncation for long histories
- Smart retrieval limiting to 2-3 most relevant turns
- Working memory buffer size optimization
- Periodic summarization to prevent memory bloat

#### Database Optimizations
- SQLite indexes on frequently queried columns
- PRAGMA settings for performance:
  ```sql
  PRAGMA journal_mode=WAL;
  PRAGMA synchronous=NORMAL;
  PRAGMA temp_store=MEMORY;
  ```

### Memory Usage Optimization

#### Context Management
- Automatic context truncation at 1500 characters
- Selective memory inclusion based on relevance
- NPC context filtering to current interaction

#### Database Management  
- Automatic cleanup of old story summaries
- NPC interaction history limits
- Periodic database VACUUM operations

---

## Error Handling

### Common Error Patterns

#### Connection Errors
```python
except requests.exceptions.ConnectionError:
    return "Error: Cannot connect to Ollama. Make sure 'ollama serve' is running."
```

#### Timeout Handling
```python
except requests.exceptions.Timeout:
    return "Response timeout - continuing story..."
```

#### Database Errors
```python
except sqlite3.OperationalError as e:
    # Handle schema mismatches, locked databases
    self._handle_db_error(e)
```

### Graceful Degradation

#### AI Generation Failures
- Fallback to default responses
- Retry with reduced parameters  
- Continue with cached/templated content

#### Memory System Failures
- Operating with reduced context
- Fallback to working memory only
- Database recreation on corruption

---

## Extension Points

### Custom AI Models
Extend `OllamaClient` to support different models:
```python
class CustomModelClient(OllamaClient):
    def __init__(self, model_name="custom-model"):
        super().__init__(model=model_name)
```

### Additional Character Attributes
Extend `CharacterSheet` with custom stats:
```python
class ExtendedCharacterSheet(CharacterSheet):
    def __init__(self):
        super().__init__()
        self.stats.update({
            'magic_power': 10,
            'reputation': 0,
            'karma': 'neutral'
        })
```

### Custom Quest Types
Extend `QuestTracker` with specialized quest handling:
```python
class ExtendedQuestTracker(QuestTracker):
    def detect_custom_quest_type(self, response):
        # Custom quest detection logic
        pass
```

---

## Testing Framework

### Stability Testing
Built-in automated testing with configurable parameters:
```python
def run_stability_test(num_turns=30, test_actions=None):
    """Execute comprehensive stability testing"""
```

### Performance Benchmarking
```python
def benchmark_response_times(iterations=10):
    """Measure and analyze response time distribution"""
```

### Memory Consistency Validation
```python
def validate_memory_consistency(test_scenario):
    """Verify memory accuracy across game sessions"""
```

---

This documentation provides comprehensive coverage of the AI Dungeon Master system architecture, enabling developers to understand, modify, and extend the system effectively.
