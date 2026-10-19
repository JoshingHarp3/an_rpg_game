# Tristram Text Chronicles: A Python Diablo-Style Text RPG

Welcome to **Tristram Text Chronicles**, a highly customized, text-based dungeon crawler heavily inspired by the mechanics and dark fantasy atmosphere of the original **Diablo (1996)**. 

Built entirely in Python, this project focuses on deep character personalization, randomized gear progression, and an extensible object-oriented architecture.

---

## 🎮 Key Gameplay Systems

*   **Deep Customization:** Choose between three iconic classes (Warrior, Rogue, or Sorcerer), each featuring unique baseline statistics. Allocating skill points upon leveling manually forces custom optimization loops.
*   **Procedural Dungeon Generator:** Explore an infinite Cathedral system. Each floor layer dynamically scales threat counts, hidden containers (coffins/sarcophagi), and monster levels based on your active depth.
*   **Authentic Loot Factory:** Features a dynamic text generator that appends prefixes and suffixes to craft classic random magical drops (e.g., *Doombreaker Blade*, *Shadowguard Breastplate*) along with unique legendary gear (*The Grandfather*, *Arkaine's Valor*).
*   **Strategic Dungeon Crawling:** Floors track spatial memory—if your inventory pack is full or you discard an item, it remains saved on that specific floor's ground for later retrieval. Players can manually backtrack up floors or retreat to Tristram Town to heal.

---

## 🛠️ Architecture & Class Breakdown

The game uses clean object-oriented encapsulation principles, breaking logic out across six primary cooperative classes:

### 📐 Structural Layout Hierarchy

| Class Name | System Layer | Primary Responsibility |
| :--- | :--- | :--- |
| **`Hero`** | Data Model | Holds character metadata, attribute calculations, level thresholds, equipment state arrays, and backpack slots. |
| **`Monster`** | Data Model | Represents independent opponents. Computes dynamic damage fluctuations and tracks unique boss modifiers. |
| **`LootGenerator`** | Factory Layer | Combines string arrays to calculate scaling statistics for item dictionaries and manages legendary drop weights. |
| **`DungeonGenerator`** | Factory Layer | The level architect. Outlines container arrays and scales minion stats dynamically based on depth. |
| **`DungeonManager`** | Gameplay Loop | Runs the turn-based battle mechanics and handles exploration screens inside the Cathedral gates. |
| **`GameManager`** | Master Conductor | Instantiates core factories, launches the opening character setup screen, and acts as the town square engine controller. |

---

## 🚀 Execution & Setup Instructions

Ensure your repository code file is arranged in the top-to-bottom sequence expected by the compiler interpreter:
1. `import random`
2. Data Models (`Hero`, `Monster`)
3. Data Factories (`LootGenerator`, `DungeonGenerator`)
4. Execution Controllers (`DungeonManager`, `GameManager`)

To run the game, clone your repository to your local system and execute the master file inside your terminal window:

```bash
python main.py
```

---

## 🔮 Future Development Roadmap
*   **Active Spellbook System:** Hooking active combat menu inputs to the `mana` pool for casting spells like *Firebolt* or *Lesser Heal*.
*   **Tristram Market:** Implementing gold drops to allow trading with a blacksmith merchant in town.
