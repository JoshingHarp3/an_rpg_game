import random

class Hero:
    def __init__(self, name, char_class, strength, dexterity, magic, vitality):

        self.name = name
        self.char_class = char_class
        self.level = 1
        self.xp = 0
        self.xp_next_level = 100
        self.strength = strength
        self.dexterity = dexterity
        self.magic = magic
        self.mana = magic
        self.vitality = vitality
        self.hp = vitality

        self.weapon = None
        self.armor = None

        self.inventory = []
        self.max_inventory_slots = 6


    def show_stats(self):
        if self.weapon is not None:
            weapon_info = f"{self.weapon['name']} (Dmg: {self.weapon['damage']})"
        else:
            weapon_info = "None (Bare Hands - Base Dmg: 2)"
        if self.armor is not None:
            armor_info = f"{self.armor['name']} (Def: {self.armor['defense']})"
        else:
            armor_info = "None (Rags - Def: 0)"
        print("\033[H\033[2J", end="")
        print(f"\n --- {self.name} the {self.char_class} (Lv. {self.level}) ---")
        print(f"Experience: {self.xp} / {self.xp_next_level} XP")
        print(f"HP:         {self.hp} / {self.vitality}")
        print(f"Mana:       {self.mana} / {self.magic}")
        print(f"Strength:   {self.strength}")
        print(f"Dexterity:  {self.dexterity}")
        print(f"Magic:      {self.magic}")
        print(f"Weapon:     {weapon_info}")
        print(f"Armor:      {armor_info}")
        print("-" * 60)


    def view_inventory(self):
        print("\033[H\033[2J", end="")
        print(f"\n--- {self.name}'s Inventory ({len(self.inventory)}/{self.max_inventory_slots}) ---")
        if not self.inventory:
            print("Your bag is completely empty.")
        else:
            for index, item in enumerate(self.inventory, 1):
                if item["type"] in ["weapon", "armor"]:
                    stat_type = "Dmg" if item["type"] == "weapon" else "Def"
                    stat_val = item["damage"] if item["type"] == "weapon" else item["defense"]
                    print(f"{index}. {item['name']} ({stat_type}: {stat_val})")
                else:
                    print(f"{index}. {item['name']} ({item['description']})")
        print("-" * 50)


    def use_or_equip_from_inventory(self):
        self.view_inventory()
        if not self.inventory:
            return

        choice = input("Enter item number to use/equip (or hit Enter to close bag): ").strip()
        if not choice.isdigit():
            return

        idx = int(choice) - 1
        if 0 <= idx < len(self.inventory):
            item = self.inventory.pop(idx) # Pull item out of the inventory array

            if item["type"] == "potion":
                if "Health" in item["name"]:
                    self.hp = min(self.vitality, self.hp + 20)
                    print(f"Drank {item['name']}. Restored 20 HP! Current HP: {self.hp}/{self.vitality}")
                elif "Mana" in item["name"]:
                    self.mana = min(self.magic, self.mana + 20)
                    print(f"Drank {item['name']}. Restored 20 Mana! Current Mana: {self.mana}/{self.magic}")

            elif item["type"] == "weapon":
                if self.weapon is not None:
                    self.inventory.append(self.weapon)
                self.weapon = item
                print(f"Equipped {item['name']}!")

            elif item["type"] == "armor":
                if self.armor is not None:
                    self.inventory.append(self.armor)
                self.armor = item
                print(f"Equipped {item['name']}!")
        else:
            print("Invalid inventory slot.")


    def level_up(self):
        self.level += 1
        points_to_spend = 5
        print(f"\n {self.name} the {self.char_class} LEVELED UP TO LEVEL {self.level}!")
        print(f"You have received {points_to_spend} Skill Points to distribute")

        while points_to_spend > 0:
            print(f"\nRemaining Points: {points_to_spend}")
            print("1- Strength (+1)")
            print("2- Dexterity (+1)")
            print("3- Vitality (+1)")
            print("4- Magic (+1)")

            choice = input("Choose an attribute to increase (1-4): ").strip()

            if choice == "1":
                self.strength += 1
                points_to_spend -= 1
                print("Strength increased!")
            elif choice == "2":
                self.dexterity += 1
                points_to_spend -= 1
                print("Dexterity increased!")
            elif choice == "3":
                self.vitality += 1
                points_to_spend -= 1
                print("Max HP increased!")
            elif choice == "4":
                self.magic += 1
                points_to_spend -= 1
                print("Max mana increased!")
            else:
                print("Invalid choice. Please select 1, 2, 3, or 4.")

        self.hp = self.vitality
        self.mana = self.magic

        print("All Skill Points allocated")


    def attack_damage(self):
        if self.weapon is None:
            base_damage = 2
            print(f"{self.name} punches with bare hands!")
        else:
            base_damage = self.weapon["damage"]
            print(f"{self.name} attacks with {self.weapon['name']}!")

        strength_bonus = self.strength // 5
        return base_damage + strength_bonus


    def get_armor_defense(self):
        if self.armor is None:
            return 0
        return self.armor["defense"]


    def equip_item(self, item):
        if item["type"] == "weapon":
            self.weapon = item
            print(f"You equipped {item['name']}! (Damage: {item['damage']})")
        elif item["type"] == "armor":
            self.armor = item
            print(f"You equipped {item['name']}! (Defense: {item['defense']})")


    def gain_xp(self, amount):
        self.xp += amount
        print(f"You gained {amount} experience points!")
        while self.xp >= self.xp_next_level:
            self.xp -= self.xp_next_level
            self.xp_next_level = int(self.xp_next_level * 1.5)
            self.level_up()


class Monster:
    def __init__(self, name, level, hp, damage, is_unique=False):
        self.name = name
        self.level = level
        self.max_hp = hp
        self.hp = hp
        self.damage = damage
        self.is_unique = is_unique

    def is_alive(self):
        return self.hp > 0

    def attack_damage(self):
        low_bound = max(1, self.damage - 1)
        high_bound = self.damage + 2
        rolled_damage = random.randint(low_bound, high_bound)

        print(f"{self.name} attacks and deals {rolled_damage} damage!")
        return rolled_damage


class LootGenerator:
    def __init__(self):
        self.prefixes = ["Ash", "Blood", "Dark", "Doom", "Dragon", "Dwarf", "Elf", "Fire", "Flame", "Frost", "Giant", "Gold", "Iron", "Light", "Moon", "Night", "Orc", "Shadow", "Silver", "Storm"]
        self.middles = ["bane", "breaker", "bringer", "cleaver", "crusher", "edge", "flame", "frost", "guard", "hammer", "heart", "keeper", "master", "rage", "reaper", "shard", "singer", "smite", "soul", "strike"]

        self.weapon_suffixes = ["Axe", "Blade", "Bow", "Edge", "Fang", "Flail", "Hammer", "Lance", "Mace", "Scythe", "Spear", "Staff", "Sword", "Talon", "Whip", "Claw", "Dagger", "Sabre", "Maul"]
        self.armor_suffixes = ["Armor", "Breastplate", "Chainmail", "Cloak", "Gauntlets", "Greaves", "Helmet", "Leggings", "Plate Mail"]

        self.unique_items = [
            {"name": "The Grandfather", "type": "weapon", "damage": 25, "defense": 0, "is_unique": True},
            {"name": "Arkaine's Valor", "type": "armor", "damage": 0, "defense": 18, "is_unique": True},
            {"name": "The Butcher's Cleaver", "type": "weapon", "damage": 16, "defense": 0, "is_unique": True},
            {"name": "Harlequin Crest", "type": "armor", "damage": 0, "defense": 10, "is_unique": True}
        ]

    def create_loot(self, floor_level, force_unique=False):
        if force_unique or (random.random() < 0.05):
            return random.choice(self.unique_items)
        if random.random() < 0.35:
            potion_type = random.choice(["Health Potion", "Mana Potion"])
            return {
                "name": potion_type,
                "type": "potion",
                "description": "Restores 20 points of pool resource",
                "is_unique": False
            }
        prefix = random.choice(self.prefixes)
        middle = random.choice(self.middles)
        item_name = f"{prefix}{middle}"

        if random.choice(["weapon", "armor"]) == "weapon":
            suffix = random.choice(self.weapon_suffixes)
            dmg = random.randint(3, 7) + (floor_level * 2)
            return {"name": f"{item_name} {suffix}", "type": "weapon", "damage": dmg, "defense": 0, "is_unique": False}
        else:
            suffix = random.choice(self.armor_suffixes)
            dfns = random.randint(1, 4) + floor_level
            return {"name": f"{item_name} {suffix}", "type": "armor", "damage": 0, "defense": dfns, "is_unique": False}


class DungeonGenerator:
    def __init__(self, loot_factory):
        self.loot_factory = loot_factory

    def generate_floor_layout(self, floor_level):
        print(f"\nGenerating structural layout for Cathedral Floor {floor_level}...")

        monster_count = random.randint(5, 15)
        chest_count = random.randint(1, 10)

        return {
            "monsters_remaining": monster_count,
            "chests_remaining": chest_count,
            "items_on_floor": []
        }

    def spawn_monster(self, floor_level):
        if random.random() < 0.15:
            boss_names = ["The Butcher", "King Leoric", "Archbishop Lazarus", "Blood Raven", "The Skeleton King"]
            name = random.choice(boss_names)
            hp = 35 + (floor_level * 12)
            dmg = 6 + floor_level
            return Monster(name, level=floor_level + 1, hp=hp, damage=dmg, is_unique=True)
        else:
            minion_names = ["Skeleton", "Fallen One", "Zombie", "Scavenger", "Scourge Demon"]
            name = f"Lv.{floor_level} {random.choice(minion_names)}"
            hp = 12 + (floor_level * 4)
            dmg = 2 + floor_level
            return Monster(name, level=floor_level, hp=hp, damage=dmg, is_unique=False)


class DungeonManager:
    def __init__(self, player, loot_factory, dungeon_builder):
        self.player = player
        self.loot_factory = loot_factory
        self.dungeon_builder = dungeon_builder
        self.dungeon_floor = 1
        self.current_layout = None

    def handle_loot(self, monster=None, container_name=None):
        is_boss = monster.is_unique if monster else False
        found_item = self.loot_factory.create_loot(self.dungeon_floor, force_unique=is_boss)

        source = monster.name if monster else container_name
        print(f"\nFrom {source}, you found: '{found_item['name']}'")

        if found_item["type"] == "weapon":
            print(f"Damage: {found_item['damage']}")
        elif found_item["type"] == "armor":
            print(f"Defense: {found_item['defense']}")

        choice = input("Pick it up? (y/n): ").strip().lower()

        if choice == 'y':
            if len(self.player.inventory) < self.player.max_inventory_slots:
                self.player.inventory.append(found_item)
                print(f"Placed '{found_item['name']}' into your inventory bag.")
            else:
                print("\nInventory is FULL! The item falls to the floor.")
                self.current_layout["items_on_floor"].append(found_item)
        else:
            print("You drop the unwanted item onto the cold stone floor.")
            self.current_layout["items_on_floor"].append(found_item)

    def execute_battle(self, monster):
        print("\033[H\033[2J", end="")
        print(f"\nWARNING: A savage {monster.name} emerges from the shadows!")

        while monster.is_alive() and self.player.hp > 0:
            print(f"\n--- Battle Status ---")
            print(f"{self.player.name}: {self.player.hp}/{self.player.vitality} HP")
            print(f"{monster.name}: {monster.hp}/{monster.max_hp} HP")
            print("-" * 30)
            print("1. Attack")
            print("2. Flee back to Floor Safety")

            action = input("What will you do? (1-2): ").strip()

            if action == "1":
                hero_damage = self.player.attack_damage()
                monster.hp -= hero_damage
                print(f"You dealt {hero_damage} damage to {monster.name}!")

                if not monster.is_alive():
                    print("\033[H\033[2J", end="")
                    print(f"\nVictory! You have slain {monster.name}!")
                    xp_reward = monster.level * 35
                    self.player.gain_xp(xp_reward)
                    self.handle_loot(monster)
                    self.current_layout["monsters_remaining"] -= 1
                    break

                raw_monster_dmg = monster.attack_damage()
                hero_defense = self.player.armor["defense"] if self.player.armor else 0
                final_damage = max(1, raw_monster_dmg - hero_defense)

                self.player.hp -= final_damage
                print(f"You take {final_damage} damage! (Blocked {hero_defense} with armor)")

                if self.player.hp <= 0:
                    print("\nYou have died... GAME OVER.")
                    break
            elif action == "2":
                print("\nYou sprint backward, escaping the enemy safely!")
                break

    def inspect_floor_items(self):
        if not self.current_layout["items_on_floor"]:
            print("\nThere are no loose objects lying on the ground.")
            return

        print("\nItems on the ground:")
        for idx, item in enumerate(self.current_layout["items_on_floor"], 1):
            print(f"  {idx}. {item['name']}")

        pickup = input("Enter number to pick up (or hit Enter to cancel): ").strip()
        if pickup.isdigit():
            p_idx = int(pickup) - 1
            if 0 <= p_idx < len(self.current_layout["items_on_floor"]):
                if len(self.player.inventory) < self.player.max_inventory_slots:
                    grabbed = self.current_layout["items_on_floor"].pop(p_idx)
                    self.player.inventory.append(grabbed)
                    print(f"Recovered {grabbed['name']}!")
                else:
                    print("Inventory full!")

    def enter_cathedral(self):
        self.current_layout = self.dungeon_builder.generate_floor_layout(self.dungeon_floor)
        in_dungeon = True

        while in_dungeon and self.player.hp > 0:
            print(f"\n|-----------------------------------|")
            print(f"--- CATHEDRAL FLOOR {self.dungeon_floor} ---")
            print(f"Remaining Enemies:  {self.current_layout['monsters_remaining']}")
            print(f"Objects/Coffins:     {self.current_layout['chests_remaining']}")
            print(f"Items on the Ground: {len(self.current_layout['items_on_floor'])}")
            print(f"|-----------------------------------|")
            print("1. Search for a Monster to Fight")
            print("2. Search for a Chest/Coffin to Open")
            print("3. Inspect the floor for Dropped Items")
            print("4. Open Inventory Bag (Use/Equip items)")
            print("5. Climb Down to Next Floor")
            print("6. Return to Town / Go Back up a Floor")

            sub_choice = input("Choose action (1-5): ").strip()
            if sub_choice == "1":
                if self.current_layout["monsters_remaining"] > 0:
                    active_monster = self.dungeon_builder.spawn_monster(self.dungeon_floor)
                    self.execute_battle(active_monster)
                else:
                    print("\nThis floor's rooms are empty of roaming monsters.")
            elif sub_choice == "2":
                if self.current_layout["chests_remaining"] > 0:
                    self.current_layout["chests_remaining"] -= 1
                    container = random.choice(["Rotting Coffin", "Iron Chest", "Sarcophagus"])
                    print(f"\nYou break open a {container}!")
                    self.handle_loot(container_name=container)
                else:
                    print("\nNo containers remaining here.")
            elif sub_choice == "3":
                self.inspect_floor_items()
            elif sub_choice == "4":
                self.player.use_or_equip_from_inventory()
            elif sub_choice == "5":
                self.dungeon_floor += 1
                self.current_layout = self.dungeon_builder.generate_floor_layout(self.dungeon_floor)
            elif sub_choice == "6":
                if self.dungeon_floor == 1:
                    print("\nYou sprint up the entryway stairs back into Tristram town!")
                    in_dungeon = False
                else:
                    self.dungeon_floor -= 1
                    self.current_layout = self.dungeon_builder.generate_floor_layout(self.dungeon_floor)


class GameManager:
    def __init__(self):
        self.player = None
        self.is_running = True
        self.loot_factory = LootGenerator()
        self.dungeon_builder = DungeonGenerator(self.loot_factory)


    def start_menu(self):
        print("=== Welcome to the Tristram Text Chronicles ===")
        player_name = input("Enter your hero's name: ").strip()
        if not player_name:
            player_name = "The Dark Wanderer"

        while True:
            print("\033[H\033[2J", end="")
            print(f"\nGreetings {player_name}! Choose your starting Class:")
            print("1. Warrior   (High Strength & Vitality)")
            print("2. Rogue     (High Dexterity)")
            print("3. Sorcerer  (High Magic & Mana)")

            choice = input("Select a class (1-3): ").strip()

            if choice == "1":
                self.player = Hero(player_name, "Warrior", strength=15, dexterity=10, magic=50, vitality=150)
                break
            elif choice == "2":
                self.player = Hero(player_name, "Rogue", strength=8, dexterity=17, magic=70, vitality=110)
                break
            elif choice == "3":
                self.player = Hero(player_name, "Sorcerer", strength=5, dexterity=10, magic=200, vitality=80)
                break
            else:
                print("Invalid selection. Choose 1, 2, or 3.")

        print(f"\nCharacter Created successfully!")
        self.player.show_stats()


    def main_loop(self):
        self.start_menu()
        dungeon_crawler = DungeonManager(self.player, self.loot_factory, self.dungeon_builder)
        while self.is_running and self.player.hp > 0:
            print("\n--- TRISTRAM TOWN SQUARE ---")
            print("1. Venture into the Cathedral (Explore Dungeons)")
            print("2. Rest at the Tavern (Full Restore)")
            print("3. View Character Sheet")
            print("4. Open Inventory Bag (Use/Equip items)")
            print("5. Exit Game")

            action = input("Select an action (1-5): ").strip()

            if action == "1":
                dungeon_crawler.enter_cathedral()
            elif action == "2":
                self.player.hp = self.player.vitality
                self.player.mana = self.player.magic
                print("\nYou rest at the tavern. HP and Mana fully restored!")
            elif action == "3":
                self.player.show_stats()
            elif action == "4":
                self.player.use_or_equip_from_inventory()
            elif action == "5":
                print("\nGoodbye, traveler!")
                self.is_running = False

        if self.player.hp <= 0:
            print("\nYour journey has come to an end. Refresh the console to try again.")


if __name__ == "__main__":
    # Initialize the engine
    game = GameManager()
    # Kickstart the game cycle
    game.main_loop()
