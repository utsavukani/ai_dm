# AI Dungeon Master

## Overview

AI Dungeon Master is an intelligent, memory-enhanced role-playing game system that creates immersive fantasy adventures using local AI (Ollama + Llama 3.2). The system features persistent memory management, NPC relationship tracking, automatic quest detection, and character progression—all running locally on your machine.

## Key Features

- **🧠 Advanced Memory System**: Triple-layered memory (working, persistent, NPC) for perfect story consistency
- **🎭 NPC Relationships**: Characters remember your actions and relationships evolve dynamically  
- **📋 Automatic Quest Tracking**: AI detects and tracks quests from story responses
- **⚔️ Character Progression**: Level up, gain items, manage inventory automatically
- **🏰 30+ Turn Stability**: Proven stable gameplay for extended sessions
- **🔒 100% Local**: Complete privacy, no internet required during gameplay
- **⚡ Performance Optimized**: Average response time under 60 seconds

---

## Installation

### Prerequisites

- **Python 3.8+** (recommended: Python 3.9 or higher)
- **8GB RAM minimum** (16GB recommended for optimal performance)
- **5GB free disk space** (for AI model and game data)
- **Windows 10/11, macOS, or Linux**

### Step 1: Install Ollama

**Windows:**
```bash
# Download and install from https://ollama.ai
# Or use winget:
winget install Ollama.Ollama
```

**macOS:**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Step 2: Install AI Model

```bash
# Pull the Llama 3.2 model (2GB download)
ollama pull llama3.2

# Verify installation
ollama list
```

### Step 3: Clone and Setup Project

```bash
# Clone the repository
git clone <your-repo-url>
cd ai_dungeon_master

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### Step 4: Initialize Directory Structure

```bash
# Create required directories and __init__.py files
mkdir -p data logs
touch src/__init__.py
touch src/game/__init__.py  
touch src/memory/__init__.py
touch src/llm/__init__.py
```

---

## Quick Start Guide

### Starting Your First Adventure

1. **Start Ollama Server** (in one terminal):
   ```bash
   ollama serve
   ```

2. **Launch the Game** (in another terminal):
   ```bash
   # Activate virtual environment
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # macOS/Linux
   
   # Run the game
   python -m src.game.game_engine
   ```

3. **Begin Playing**:
   - The AI will create an opening scene automatically
   - Type your actions in natural language: "I explore the forest"
   - The AI remembers everything and responds consistently

### Essential Commands

- **Regular gameplay**: Type any action ("I talk to the merchant", "I search for clues")
- **`stats`**: View detailed game statistics and performance metrics
- **`character`**: Display character sheet with level, health, inventory
- **`quests`**: Show active and completed quest log  
- **`inventory`**: List all items in your possession
- **`test`**: Run 30-turn stability test for system validation
- **`help`**: Display all available commands
- **`quit`**: Exit the game (progress is saved)

### Example Gameplay Session

```
DM: You awaken in a misty forest clearing. Ancient oak trees surround you, their branches whispering secrets. A narrow path leads north toward distant mountains, while smoke rises from a village to the east. Your leather bag contains basic supplies: a short sword, 50 gold pieces, and a healing potion.

What would you like to do next?

You: I head toward the village to gather information

DM: As you approach the village of Millhaven, you notice bustling market stalls and friendly villagers. An elderly merchant named Gareth waves you over...

📋 New Quest Detected: Find the missing village children
🎒 Added Village Map to inventory!

You: I talk to Gareth about the missing children
```

---

## Features Overview

### 🧠 Triple Memory System

**Working Memory (5 turns)**
- Maintains perfect recall of recent conversation
- Instant access for immediate story context
- Automatically summarizes older content

**Persistent Memory (Unlimited)**  
- Stores all game events with importance scoring
- Smart retrieval based on current context
- Periodic story summarization every 10 turns

**NPC Memory (Individual)**
- Each character has personal memory and traits
- Relationship tracking (friendly/neutral/hostile)
- Dynamic personality development

### 🎭 Advanced NPC System

- **Automatic Detection**: AI identifies new characters in story responses
- **Personality Inference**: Deduces traits from context (merchant, guard, wise sage)
- **Relationship Evolution**: Characters remember gifts, insults, help, betrayals
- **Interaction History**: Full log of every encounter with each NPC

### 📋 Quest Management

- **Auto-Detection**: Recognizes quest-giving language patterns
- **Progress Tracking**: Monitors quest completion automatically  
- **Quest Log**: Organized view of active and completed quests
- **Completion Recognition**: AI detects when objectives are fulfilled

### ⚔️ Character Progression

- **Automatic Leveling**: Gain XP from battles, quest completion, problem-solving
- **Dynamic Inventory**: Items detected and added from AI responses
- **Attribute Growth**: Strength, Intelligence, Charisma increase with levels
- **Health Management**: Combat damage and healing tracked

### 🏰 Stability & Performance

- **Proven 30+ Turn Stability**: Extensive automated testing
- **Memory Optimization**: Smart context building prevents slowdowns  
- **Error Recovery**: Graceful handling of connection issues
- **Performance Monitoring**: Real-time response time tracking

---

## Usage Examples

### Basic Adventure Commands

```bash
# Exploration
"I explore the dark cave carefully"
"I examine the ancient runes on the wall"
"I listen for any sounds or movement"

# NPC Interaction  
"I greet the tavern keeper warmly"
"I ask the guard about recent troubles"
"I offer to help the worried merchant"

# Combat Actions
"I draw my sword and attack the orc"
"I cast a fire spell at the enemy"
"I try to dodge the incoming arrow"

# Quest Actions
"I accept the quest to find the missing artifact"
"I return the stolen goods to the merchant"
"I report my success to the village elder"
```

### Advanced System Commands

```bash
# System Information
stats          # Comprehensive statistics
character      # Full character sheet  
quests         # Quest log with progress
inventory      # Complete item list

# Testing & Validation  
test           # Run 30-turn stability test
export         # Export complete game log

# Performance Optimization
help           # Command reference
quit           # Safe game exit
```

---

## Troubleshooting

### Common Issues & Solutions

#### "Error connecting to Ollama: Connection refused"

**Cause**: Ollama server is not running  
**Solution**: 
```bash
# Start Ollama server in separate terminal
ollama serve

# Verify it's running
curl http://localhost:11434/api/tags
```

#### "500 Server Error: Internal Server Error"

**Cause**: Model not fully loaded or memory pressure  
**Solution**:
```bash
# Pre-warm the model
ollama run llama3.2 "Hello"

# If issue persists, try smaller model
ollama pull llama3.2:1b
```

#### "ModuleNotFoundError: No module named 'game'"

**Cause**: Running from wrong directory or missing `__init__.py` files  
**Solution**:
```bash
# Ensure you're in project root
cd ai_dungeon_master

# Create missing __init__.py files
touch src/__init__.py src/game/__init__.py src/memory/__init__.py src/llm/__init__.py

# Run as module
python -m src.game.game_engine
```

#### Slow Response Times (>90 seconds)

**Cause**: Large context or resource constraints  
**Solution**:
```bash
# Close other applications to free RAM
# Use optimized client settings in ollama_client.py:
"options": {
    "num_predict": 200,
    "num_ctx": 2048,
    "num_thread": 8
}
```

#### Game Freezes or Stops Responding

**Cause**: Long AI generation or memory issues  
**Solution**:
```bash
# Press Ctrl+C to interrupt
# Restart with clean slate:
rm -rf data/memory.db  # Clears memory (optional)
python -m src.game.game_engine
```

#### Memory Database Errors

**Cause**: Corrupted SQLite database or schema mismatch  
**Solution**:
```bash
# Reset memory database
rm data/memory.db
# Game will recreate it automatically on next run
```

### System Requirements Issues

#### Insufficient RAM
- **Symptoms**: Frequent freezes, slow responses, system crashes
- **Solution**: Close other applications, use smaller model (`llama3.2:1b`)

#### Storage Space
- **Symptoms**: "No space left on device" errors  
- **Solution**: Free up 5GB+ disk space, clean temp files

#### Network Issues  
- **Symptoms**: Model download failures
- **Solution**: Check internet connection, use VPN if geo-blocked

### Getting Help

If issues persist:

1. **Check logs** in `logs/` directory for detailed error information
2. **Run diagnostics**: Use `test` command to validate system health  
3. **Reset database**: Delete `data/memory.db` for fresh start
4. **Verify installation**: Ensure all dependencies installed correctly

### Performance Optimization

**For faster responses:**
- Close unnecessary applications
- Use SSD storage for faster database access
- Increase system RAM to 16GB+ if possible
- Use wired internet connection for model downloads

**For better stability:**
- Run stability test regularly: `test` command
- Monitor system resources during gameplay
- Keep game sessions under 100 turns for optimal performance

---

## File Structure

```
ai_dungeon_master/
├── src/
│   ├── __init__.py
│   ├── game/
│   │   ├── __init__.py
│   │   ├── game_engine.py      # Main game controller
│   │   ├── character_sheet.py  # Character progression
│   │   └── quest_tracker.py    # Quest management
│   ├── memory/
│   │   ├── __init__.py
│   │   └── memory_manager.py   # Triple memory system  
│   └── llm/
│       ├── __init__.py
│       └── ollama_client.py    # AI client interface
├── data/
│   └── memory.db              # Game state database
├── logs/                      # Game session logs
├── venv/                      # Python virtual environment
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

---

## Technical Requirements

- **Python**: 3.8+ (tested on 3.9, 3.10, 3.11)
- **RAM**: 8GB minimum (16GB recommended)  
- **Storage**: 5GB free space
- **CPU**: Multi-core processor recommended
- **OS**: Windows 10+, macOS 10.14+, Ubuntu 18.04+

---

## License

This project is released under the MIT License. See LICENSE file for details.

---

## Support

For technical support, bug reports, or feature requests, please check the troubleshooting section above or contact the development team.