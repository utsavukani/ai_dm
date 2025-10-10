# AI Dungeon Master

DEMO VIDEO LINK: https://youtu.be/lbLSe_plp6k?si=BwNPj5HBeVB6T_WO

## Project Overview
A fully functional AI Dungeon Master with persistent memory, NPC relationships, and 30+ turn stability for immersive role-playing adventures.

## 🏗️ Project Structure

```
ai_dungeon_master/
├── 📁 src/                          # Source code directory
│   ├── 📄 __init__.py               # Package initialization
│   ├── 📁 game/                     # Game engine components
│   │   ├── 📄 __init__.py
│   │   ├── 📄 game_engine.py        # Main game orchestration
│   │   ├── 📄 character_sheet.py    # Player stats & inventory
│   │   └── 📄 quest_tracker.py      # Quest management system
│   ├── 📁 memory/                   # Memory management system
│   │   ├── 📄 __init__.py
│   │   └── 📄 memory_manager.py     # Triple memory architecture
│   ├── 📁 llm/                      # LLM integration layer
│   │   ├── 📄 __init__.py
│   │   └── 📄 ollama_client.py      # Ollama API client
├── 📁 data/                         # Database and storage
│   └── 📄 memory.db                 # SQLite database (auto-created)
├── 📁 tests/                        # Test suite
│   ├── 📄 test_memory.py           # Memory system tests
├── 📁 docs/                         # Documentation
│   ├── 📄 API_DOCUMENTATION.md     # API reference
│   └── 📄 architecture_diagram.png  # System architecture
├── 📁 venv/                         # Python virtual environment
├── 📄 requirements.txt              # Python dependencies
├── 📄 README.md                    # Usage and Setup Guide
```

## 🧠 Core Architecture Components

### 1. Triple Memory System
- **Working Memory**: Last 5 turns for immediate context
- **Persistent Memory**: Long-term storage with importance scoring
- **NPC Memory**: Individual character relationships and traits

### 2. Game Engine
- Turn-based interaction processing
- Performance monitoring and statistics
- Automated stability testing
- Session logging and export

### 3. LLM Integration
- Local Ollama server communication
- Context-aware prompt building
- Error handling and retry logic
- Response quality optimization

### 4. Safety & Quality
- Content filtering for inappropriate inputs
- Memory consistency validation
- Response coherence checking
- Error recovery mechanisms

## 📋 Requirements

### System Requirements
- Python 3.8+ 
- 8GB+ RAM (recommended)
- 4GB+ free disk space
- Windows 10/11, macOS, or Linux

### Dependencies
```txt
requests>=2.28.0
sqlite3 (built-in)
json (built-in)
uuid (built-in)
datetime (built-in)
time (built-in)
re (built-in)
os (built-in)
```

### External Dependencies
- **Ollama**: Local LLM server
- **Llama 3.2 Model**: 3.2B parameter model

## 🚀 Installation & Setup

### Quick Setup
```bash
# 1. Clone/download the project
git clone <repository-url>
cd ai_dungeon_master

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install and setup Ollama
# Download from: https://ollama.ai
ollama pull llama3.2

# 5. Run the game
python src/game/game_engine.py
```

### First Run Checklist
- [ ] Virtual environment activated
- [ ] Ollama server running (`ollama serve`)
- [ ] Llama 3.2 model downloaded
- [ ] All `__init__.py` files present
- [ ] SQLite database auto-created in `data/`

## 🎮 Usage Commands

### In-Game Commands
- **Regular Input**: Type any action to continue the story
- **`stats`**: Show detailed memory and performance statistics
- **`test`**: Run automated 30-turn stability test
- **`export`**: Export current game session to JSON log
- **`character`**: Display character sheet (if implemented)
- **`quests`**: Show active and completed quests (if implemented)
- **`help`**: Display command reference
- **`quit`**: Exit the game

### Example Gameplay Session
```
DM: You awaken in a mystical forest clearing...
You: I explore to the north
DM: As you venture north, you encounter a wise old merchant named Elric...
You: I talk to Elric about the local area
DM: Elric's eyes light up as he recognizes you're new to these parts...
```

## 🔧 Development Features

### Memory Management
- **Working Memory**: 5-turn rolling buffer
- **Persistence**: SQLite database with smart retrieval
- **NPC Tracking**: Individual character memories
- **Context Building**: Relevance-based memory selection

### Performance Monitoring
- Response time tracking
- Memory efficiency metrics
- Error rate monitoring
- Turn count and session duration

### Quality Assurance
- Automated stability testing (30+ turns)
- Memory consistency validation
- Response coherence checking
- Performance benchmarking

### Extensibility
- Modular architecture for easy feature addition
- Plugin-ready design for new memory types
- Configurable LLM parameters
- Customizable safety filters

## 📊 Technical Specifications

### Performance Targets
- **Response Time**: <20 seconds average
- **Memory Efficiency**: >95% relevance in retrieval
- **Stability**: 30+ turn sessions without crashes
- **Storage**: Efficient SQLite compression

### Memory Architecture
- **Working**: 5 turns × ~500 chars = ~2.5KB active
- **Persistent**: Unlimited with compression and scoring
- **NPC**: Individual character profiles with relationship tracking
- **Retrieval**: Keyword and semantic similarity matching

### Database Schema
```sql
-- Game turns storage
game_turns (id, timestamp, turn_number, player_input, ai_response, 
           context, importance_score, summary, key_entities)

-- Story summaries
story_summaries (id, turn_range, summary, key_events, timestamp)

-- NPC profiles
npcs (npc_id, name, first_met_turn, personality_traits, 
     relationship_status, memory_summary, interaction_count)

-- NPC interactions
npc_interactions (id, npc_id, turn_number, player_action, 
                 npc_response, relationship_change, timestamp)
```

## 🧪 Testing Framework

### Automated Tests
- **Unit Tests**: Individual component testing
- **Integration Tests**: Cross-component functionality
- **Stability Tests**: Long-session endurance testing
- **Performance Tests**: Response time and memory benchmarks

### Test Coverage Areas
- Memory storage and retrieval accuracy
- NPC relationship tracking consistency
- LLM integration robustness
- Error handling and recovery
- Database integrity and performance

## 🏆 Competition Advantages

### Technical Innovation
- **Triple Memory Architecture**: Industry-leading memory management
- **Local Deployment**: Complete privacy and control
- **NPC Relationship System**: Advanced character interaction tracking
- **Performance Monitoring**: Built-in quality assurance

### User Experience
- **Narrative Consistency**: Story coherence across 30+ turns
- **Character Persistence**: NPCs remember past interactions
- **Performance Transparency**: Real-time statistics and monitoring
- **Session Management**: Export and replay capabilities

### Development Quality
- **Clean Architecture**: Modular, maintainable codebase
- **Comprehensive Testing**: Automated quality validation
- **Detailed Documentation**: Professional technical reporting
- **Extensible Design**: Plugin-ready for future enhancements

## 🔮 Future Enhancements

### Planned Features
- Web-based interface
- Multi-language support
- Advanced NPC personality modeling
- Campaign persistence across sessions
- Visual character sheets and maps

### Potential Integrations
- Discord bot interface
- Twitch integration for streaming
- Mobile companion app
- Voice input/output support
- Advanced graphics and animations

---

## 📞 Support & Documentation

For detailed technical documentation, see:
- `README.md` - User guide and setup instructions
- `docs/API_DOCUMENTATION.md` - Developer API reference

**Status**: Ready for competition submission ✅
