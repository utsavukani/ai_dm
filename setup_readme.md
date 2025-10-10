Here’s a comprehensive `README.md` tailored for your AI Dungeon Master (AIDM) project using local Llama models and Ollama.

***

# **AI Dungeon Master**

An intelligent, LLM-powered Dungeon Master for narrative RPGs. This system uses advanced local language models (via [Ollama](https://ollama.com/)) to run fully offline and maintain detailed, context-aware stories, persistent memories, and dynamic NPCs.

***

## **Features**

- 🧠 Short-term & long-term memory for narrative consistency
- 🧑‍🤝‍🧑 Dynamic NPC memory—NPCs remember past interactions
- ⚡ Fully local inference (no tokens, no API limit)
- 🔄 30+ turn stable session support
- 📖 Automated story summarization and memory ranking
- 🛠️ Modular, extensible Python architecture

***

## **Project Structure**

```
AI_DUNGEON_MASTER/
├── data/
├── logs/
├── src/
│   ├── game/
│   │    ├── game_engine.py
│   │    └── __init__.py
│   ├── llm/
│   │    ├── ollama_client.py
│   │    └── __init__.py
│   ├── memory/
│   │    ├── memory_manager.py
│   │    └── __init__.py
│   └── __init__.py
├── tests/
│   └── test_memory.py
├── venv/
├── requirements.txt
└── README.md
```

***

## **Setup Instructions**

### **1. Prerequisites**
- Python 3.8+
- [Ollama](https://ollama.com/download) installed and running locally
- A supported LLM model pulled with Ollama, e.g.:
  ```bash
  ollama pull llama3.2
  ```

### **2. Clone and Prepare Project**
```bash
# Clone your repo (if remote) or move to your code directory
git clone <your-repo-url>
cd ai_dm

# (Optional) Set up a virtual environment
python -m venv venv
venv\Scripts\activate      # On Windows
# source venv/bin/activate # On Mac/Linux

# Install Python dependencies
pip install -r requirements.txt
```
**requirements.txt** should contain at least:
```
requests
```

### **3. Run Ollama Server**
Make sure `ollama serve` is running (may happen automatically):
```bash
ollama serve
```

***

## **Running the Game**

**Always run from your project root directory.**
Set the Python path and launch:
```bash
set PYTHONPATH=%cd%\src
python game_engine.py 
```

***

## **Usage**

- **Type story actions to play:**  
  e.g. `Explore the library`, `Talk to the merchant`, `Attack the goblin`.

- **Type `stats`** for live game memory and performance information  
- **Type `test`** for an automated 30-turn stability check  
- **Type `export`** to save all game data to a log file  
- **Type `quit`** at any time to exit

***

## **Customization**

- Edit `src/memory/memory_manager.py` for memory depth and summarization.
- Swap LLM models by changing `"model"` in `src/llm/ollama_client.py`.
- Enhance prompt management in `src/llm/ollama_client.py` for different storytelling or genre styles.

***

## **Troubleshooting**

- **Import/module errors:**  
  Ensure you run from the project root and set `PYTHONPATH`.
- **Ollama connection issues:**  
  Verify Ollama server is running, and the model (`llama3.2`, etc.) is pulled.
- **Performance lags:**  
  Limit prompt/context size and use quantized Llama models for faster inference.

***

## **Contribution and License**
Feel free to fork, improve, or extend the project!  
For open-source licensing, add a `LICENSE` file as required by your use/purpose.

***

## **Acknowledgements**
- [Ollama](https://ollama.com/)
- Meta Llama 3 models
- Open-source Python ecosystem

***

**Happy adventuring!** If you need further help, open an issue or discuss with project collaborators.






















Guide me step by step to push this whole project folder at github without any error and also guide and teach when I change the code in my VS code it should be directly change there in the github repo also