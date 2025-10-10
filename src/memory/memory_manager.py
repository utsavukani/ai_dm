import json
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
import uuid
import os
import re


# -----------------------------
# Working (short-term) memory
# -----------------------------
class WorkingMemory:
    """Enhanced short-term memory with summarization"""
    def __init__(self, max_turns: int = 5):
        self.max_turns = max_turns
        self.memory: List[Dict] = []
        self.turn_summaries: List[Dict] = []

    def add_turn(self, player_input: str, ai_response: str, context: Optional[Dict] = None):
        turn = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "player_input": player_input or "",
            "ai_response": ai_response or "",
            "context": context or {},
            "turn_number": len(self.memory) + 1
        }
        self.memory.append(turn)

        # Summarize and roll the buffer
        if len(self.memory) > self.max_turns:
            removed_turn = self.memory.pop(0)
            summary = self._create_turn_summary(removed_turn)
            self.turn_summaries.append(summary)
            if len(self.turn_summaries) > 10:
                self.turn_summaries.pop(0)

    def _create_turn_summary(self, turn: Dict) -> Dict:
        """Create a compressed summary of a turn"""
        return {
            "turn_number": turn.get("turn_number", -1),
            "summary": (
                f"Turn {turn.get('turn_number', 'N/A')}: "
                f"{(turn.get('player_input') or '')[:50]}..."
                f" -> {(turn.get('ai_response') or '')[:100]}..."
            ),
            "key_events": self._extract_key_events(
                turn.get("player_input") or "", turn.get("ai_response") or ""
            ),
            "timestamp": turn.get("timestamp") or datetime.now().isoformat(),
        }

    def _extract_key_events(self, player_input: str, ai_response: str) -> List[str]:
        """Extract important events from turn text (lightweight heuristics)"""
        events: List[str] = []

        # Character-like names
        characters = re.findall(r"\b[A-Z][a-z]+\b", ai_response)
        # Simple location phrases
        locations = re.findall(r"(?:in|at|to) the ([a-z]+)", ai_response.lower())
        # Items from player intent
        items = re.findall(r"(?:find|get|take|give) (?:a |an |the )?([a-z ]+)", player_input.lower())

        if characters:
            events.append(f"met: {', '.join(sorted(set(characters)))}")
        if locations:
            events.append(f"locations: {', '.join(sorted(set(locations)))}")
        if items:
            events.append(f"items: {', '.join(sorted(set(items)))}")

        return events

    def get_recent_context(self) -> str:
        context = "=== Recent Turns (Working Memory) ===\n"
        for summary in self.turn_summaries[-3:]:
            context += f"{summary['summary']}\n"
        for turn in self.memory:
            context += f"Turn {turn.get('turn_number', 'N/A')}: Player: {turn['player_input']}\n"
            context += f"DM: {turn['ai_response']}\n\n"
        return context

    def get_memory(self) -> List[Dict]:
        return self.memory


# -----------------------------
# NPC memory manager
# -----------------------------
class NPCMemoryManager:
    """Manages individual NPC memories and relationships"""
    def __init__(self, db_path: str = "data/memory.db"):
        self.db_path = db_path
        self._init_npc_database()

    def _init_npc_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS npcs (
                npc_id TEXT PRIMARY KEY,
                name TEXT,
                first_met_turn INTEGER,
                personality_traits TEXT,
                relationship_status TEXT DEFAULT 'neutral',
                last_interaction_turn INTEGER,
                memory_summary TEXT,
                interaction_count INTEGER DEFAULT 0
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS npc_interactions (
                id TEXT PRIMARY KEY,
                npc_id TEXT,
                turn_number INTEGER,
                player_action TEXT,
                npc_response TEXT,
                relationship_change TEXT,
                timestamp TEXT,
                FOREIGN KEY (npc_id) REFERENCES npcs (npc_id)
            )
        """)

        conn.commit()
        conn.close()

    def add_or_update_npc(self, name: str, turn_number: int, interaction_context: str = "") -> str:
        npc_id = name.lower().strip().replace(" ", "_")
        if not npc_id:
            return ""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM npcs WHERE npc_id = ?", (npc_id,))
        exists = cursor.fetchone() is not None

        if not exists:
            traits = self._infer_personality_traits(interaction_context or "")
            cursor.execute(
                """
                INSERT INTO npcs (npc_id, name, first_met_turn, personality_traits,
                                  last_interaction_turn, interaction_count, memory_summary)
                VALUES (?, ?, ?, ?, ?, 1, ?)
                """,
                (npc_id, name, turn_number, traits, turn_number, f"First met player on turn {turn_number}")
            )
        else:
            cursor.execute(
                """
                UPDATE npcs
                SET last_interaction_turn = ?, interaction_count = interaction_count + 1
                WHERE npc_id = ?
                """,
                (turn_number, npc_id)
            )

        conn.commit()
        conn.close()
        return npc_id

    def add_npc_interaction(self, npc_id: str, turn_number: int, player_action: str, npc_response: str):
        if not npc_id:
            return

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        relationship_change = self._analyze_relationship_change(player_action or "", npc_response or "")

        cursor.execute(
            """
            INSERT INTO npc_interactions (id, npc_id, turn_number, player_action, npc_response, relationship_change, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (str(uuid.uuid4()), npc_id, turn_number, player_action or "", npc_response or "",
             relationship_change, datetime.now().isoformat())
        )

        if relationship_change != "neutral":
            cursor.execute(
                "UPDATE npcs SET relationship_status = ? WHERE npc_id = ?",
                (relationship_change, npc_id)
            )

        conn.commit()
        conn.close()

    def get_npc_memory(self, name: str) -> Optional[Dict]:
        npc_id = (name or "").lower().strip().replace(" ", "_")
        if not npc_id:
            return None

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM npcs WHERE npc_id = ?", (npc_id,))
        npc_data = cursor.fetchone()
        if not npc_data:
            conn.close()
            return None

        cursor.execute(
            "SELECT * FROM npc_interactions WHERE npc_id = ? ORDER BY turn_number DESC LIMIT 5",
            (npc_id,)
        )
        recent_interactions = cursor.fetchall()
        conn.close()

        return {
            "npc_id": npc_data[0],
            "name": npc_data[1],
            "first_met_turn": npc_data[2],
            "personality_traits": npc_data[3],
            "relationship_status": npc_data[4],
            "last_interaction_turn": npc_data[5],
            "memory_summary": npc_data[6],
            "interaction_count": npc_data[7],
            "recent_interactions": recent_interactions
        }

    def _infer_personality_traits(self, context: str) -> str:
        traits: List[str] = []
        ctx = (context or "").lower()
        if any(w in ctx for w in ["merchant", "sell", "buy", "trade"]):
            traits.append("merchant")
        if any(w in ctx for w in ["guard", "soldier", "protect"]):
            traits.append("guard")
        if any(w in ctx for w in ["wise", "old", "sage", "knowledge"]):
            traits.append("wise")
        return ", ".join(traits) if traits else "unknown"

    def _analyze_relationship_change(self, player_action: str, npc_response: str) -> str:
        pa = (player_action or "").lower()
        nr = (npc_response or "").lower()
        if any(w in pa for w in ["help", "give", "assist", "kind"]) or any(
            w in nr for w in ["thank", "grateful", "pleased", "happy"]
        ):
            return "friendly"
        if any(w in pa for w in ["attack", "steal", "threaten", "rude"]) or any(
            w in nr for w in ["angry", "upset", "hostile", "flee"]
        ):
            return "hostile"
        return "neutral"


# -----------------------------
# Persistent (long-term) memory
# -----------------------------
class EnhancedPersistentMemory:
    """Enhanced long-term memory with smart retrieval and migrations"""
    def __init__(self, db_path: str = "data/memory.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_database()

    def _init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Base table to ensure file exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS game_turns (
                id TEXT PRIMARY KEY,
                timestamp TEXT,
                turn_number INTEGER,
                player_input TEXT,
                ai_response TEXT,
                context TEXT
            )
        """)

        # Migration: add new columns if missing
        cursor.execute("PRAGMA table_info(game_turns)")
        cols = {row[1] for row in cursor.fetchall()}

        if "importance_score" not in cols:
            cursor.execute("ALTER TABLE game_turns ADD COLUMN importance_score REAL DEFAULT 1.0")
        if "summary" not in cols:
            cursor.execute("ALTER TABLE game_turns ADD COLUMN summary TEXT")
        if "key_entities" not in cols:
            cursor.execute("ALTER TABLE game_turns ADD COLUMN key_entities TEXT")

        # Story summaries table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS story_summaries (
                id TEXT PRIMARY KEY,
                turn_range TEXT,
                summary TEXT,
                key_events TEXT,
                timestamp TEXT
            )
        """)

        conn.commit()
        conn.close()

    def store_turn(self, turn_data: Dict, turn_number: int):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        player_input = (turn_data.get("player_input") or "").strip()
        ai_response = (turn_data.get("ai_response") or "").strip()

        importance = self._calculate_importance(player_input, ai_response)
        entities = self._extract_entities(player_input, ai_response)
        summary = self._create_summary(player_input, ai_response)

        cursor.execute(
            """
            INSERT INTO game_turns
            (id, timestamp, turn_number, player_input, ai_response, context, importance_score, summary, key_entities)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                turn_data["id"],
                turn_data["timestamp"],
                turn_number,
                player_input,
                ai_response,
                json.dumps(turn_data.get("context", {})),
                importance,
                summary,
                json.dumps(entities),
            ),
        )

        conn.commit()
        conn.close()

        if turn_number % 10 == 0:
            self._create_story_summary(turn_number - 9, turn_number)

    def retrieve_relevant_turns(self, query: str, limit: int = 5) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        q = (query or "").strip()
        if not q:
            # If no query text, return most recent important turns
            cursor.execute(
                """
                SELECT *, (importance_score * 2) as relevance_score
                FROM game_turns
                ORDER BY turn_number DESC
                LIMIT ?
                """,
                (limit,),
            )
            rows = cursor.fetchall()
            conn.close()
            return self._rows_to_turn_dicts(rows)

        words = q.lower().split()
        keyword_conditions = " OR ".join(
            ["(player_input LIKE ? OR ai_response LIKE ? OR summary LIKE ?)"] * len(words)
        )
        params: List[str] = []
        for w in words:
            params.extend([f"%{w}%", f"%{w}%", f"%{w}%"])

        cursor.execute(
            f"""
            SELECT *,
                   (importance_score * 2
                    + CASE WHEN player_input LIKE ? THEN 3 ELSE 0 END
                    + CASE WHEN ai_response LIKE ? THEN 2 ELSE 0 END) AS relevance_score
            FROM game_turns
            WHERE {keyword_conditions}
            ORDER BY relevance_score DESC, turn_number DESC
            LIMIT ?
            """,
            [f"%{q}%", f"%{q}%"] + params + [limit],
        )
        rows = cursor.fetchall()
        conn.close()
        return self._rows_to_turn_dicts(rows)

    @staticmethod
    def _rows_to_turn_dicts(rows) -> List[Dict]:
        results: List[Dict] = []
        for row in rows:
            # row indices follow SELECT * order plus relevance_score at the end
            data = {
                "id": row[0],
                "timestamp": row[1],
                "turn_number": row[2],
                "player_input": row[3],
                "ai_response": row[4],
                "context": json.loads(row[5]) if row[5] else {},
                "importance_score": row[6] if len(row) > 6 else 1.0,
                "summary": row[7] if len(row) > 7 else "",
                "key_entities": json.loads(row[8]) if len(row) > 8 and row[8] else [],
            }
            # relevance_score may not exist in some queries
            if len(row) > 9:
                data["relevance_score"] = row[9]
            results.append(data)
        return results

    def _calculate_importance(self, player_input: str, ai_response: str) -> float:
        importance = 1.0
        high = ["fight", "battle", "death", "quest", "treasure", "magic", "dragon", "king", "princess"]
        medium = ["npc", "character", "item", "place", "meet", "find", "discover"]

        text = f"{player_input} {ai_response}".lower()
        if any(w in text for w in high):
            importance += 2.0
        if any(w in text for w in medium):
            importance += 1.0
        if len(ai_response) > 200:
            importance += 0.5
        return min(importance, 5.0)

    def _extract_entities(self, player_input: str, ai_response: str) -> List[str]:
        text = f"{player_input} {ai_response}"
        entities: List[str] = []
        entities.extend(re.findall(r"\b[A-Z][a-z]+\b", text))                # Names/places
        entities.extend(re.findall(r"(?:the|a|an) ([a-z]+ ?[a-z]*)", text.lower()))  # Items
        # Deduplicate while preserving order
        seen = set()
        uniq = []
        for e in entities:
            if e not in seen:
                seen.add(e)
                uniq.append(e)
        return uniq

    def _create_summary(self, player_input: str, ai_response: str) -> str:
        pi = player_input[:50] + ("..." if len(player_input) > 50 else "")
        ar = ai_response[:100] + ("..." if len(ai_response) > 100 else "")
        return f"Player: {pi} -> {ar}"

    def _create_story_summary(self, start_turn: int, end_turn: int):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT summary, key_entities FROM game_turns
            WHERE turn_number BETWEEN ? AND ?
            ORDER BY turn_number
            """,
            (start_turn, end_turn),
        )
        turns = cursor.fetchall()

        if turns:
            summaries = [t[0] for t in turns if t and t[0]]
            all_entities: List[str] = []
            for t in turns:
                if t and t[1]:
                    try:
                        all_entities.extend(json.loads(t[1]))
                    except Exception:
                        pass

            story_summary = f"Turns {start_turn}-{end_turn}: " + " | ".join(summaries[:3])
            key_events = []
            seen = set()
            for e in all_entities:
                if e not in seen:
                    seen.add(e)
                    key_events.append(e)
                    if len(key_events) >= 10:
                        break

            cursor.execute(
                """
                INSERT INTO story_summaries (id, turn_range, summary, key_events, timestamp)
                VALUES (?, ?, ?, ?, ?)
                """,
                (str(uuid.uuid4()), f"{start_turn}-{end_turn}", story_summary,
                 json.dumps(key_events), datetime.now().isoformat()),
            )
            conn.commit()

        conn.close()


# -----------------------------
# Orchestrator
# -----------------------------
class EnhancedMemoryManager:
    """Enhanced memory manager with NPC support"""
    def __init__(self):
        self.working_memory = WorkingMemory()
        self.persistent_memory = EnhancedPersistentMemory()
        self.npc_memory = NPCMemoryManager()
        self.turn_counter = 0

    def process_turn(self, player_input: str, ai_response: str, context: Optional[Dict] = None):
        self.turn_counter += 1

        # Process NPCs mentioned in this turn
        self._process_npcs_in_turn(player_input or "", ai_response or "")

        # Add to working memory
        self.working_memory.add_turn(player_input or "", ai_response or "", context)

        # Store in persistent memory
        turn_data = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "player_input": player_input or "",
            "ai_response": ai_response or "",
            "context": context or {},
        }
        self.persistent_memory.store_turn(turn_data, self.turn_counter)

    def _process_npcs_in_turn(self, player_input: str, ai_response: str):
        """Detect and process NPCs mentioned in the turn"""
        npc_names = re.findall(r"\b([A-Z][a-z]+ ?[A-Z]?[a-z]*)\b", ai_response or "")
        for name in npc_names:
            if len(name.split()) <= 2 and name not in {"You", "The", "Player"}:
                npc_id = self.npc_memory.add_or_update_npc(name, self.turn_counter, ai_response or "")
                self.npc_memory.add_npc_interaction(npc_id, self.turn_counter, player_input or "", ai_response or "")

    def get_context_for_llm(self, current_input: str) -> str:
        """Build enhanced context string for LLM"""
        context = ""

        # Recent working memory
        context += self.working_memory.get_recent_context()

        # Relevant historical context
        relevant_turns = self.persistent_memory.retrieve_relevant_turns(current_input or "", limit=3)
        if relevant_turns:
            context += "\n=== Relevant Past Events ===\n"
            for t in relevant_turns:
                imp = t.get("importance_score", 1.0)
                summ = t.get("summary", "")
                tn = t.get("turn_number", "?")
                context += f"Turn {tn} (importance: {imp:.1f}): {summ}\n"

        # NPC context
        context += self._get_npc_context(current_input or "", relevant_turns or [])

        return context

    def _get_npc_context(self, current_input: str, relevant_turns: List[Dict]) -> str:
        npc_context = ""
        potential_npcs = re.findall(r"\b[A-Z][a-z]+\b", current_input or "")

        for t in relevant_turns:
            for ent in t.get("key_entities", []):
                if isinstance(ent, str) and ent and ent[0].isupper():
                    potential_npcs.append(ent)

        for npc_name in sorted(set(potential_npcs)):
            mem = self.npc_memory.get_npc_memory(npc_name)
            if mem:
                npc_context += f"\n=== {mem['name']} (NPC Memory) ===\n"
                npc_context += f"Relationship: {mem['relationship_status']}\n"
                npc_context += f"Traits: {mem['personality_traits']}\n"
                npc_context += f"Memory: {mem['memory_summary']}\n"
                npc_context += f"Interactions: {mem['interaction_count']} times\n"

        return npc_context
