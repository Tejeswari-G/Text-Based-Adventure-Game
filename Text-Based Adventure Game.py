pip install -r requirements.txt
#Use pip install -r requirements.txt to install all project dependencies in one step.

import json
import os

# -----------------------
# Game Data
# -----------------------
locations = {
    "village": {
        "description": "You are in a small village. There's a path to the forest and a shop here.",
        "paths": ["forest", "shop"],
        "items": []
    },
    "forest": {
        "description": "You are in a dark forest. You hear wolves howling. There's a path to a cave.",
        "paths": ["village", "cave"],
        "items": ["magic stone"]
    },
    "shop": {
        "description": "You are in a small shop. You can buy a sword here for the magic stone.",
        "paths": ["village"],
        "items": []
    },
    "cave": {
        "description": "You are inside a cave. There's a sleeping dragon here guarding a treasure chest.",
        "paths": ["forest"],
        "items": ["treasure"]
    }
}

# Player data
player = {
    "location": "village",
    "inventory": []
}

SAVE_FILE = "savegame.json"

# -----------------------
# Game Functions
# -----------------------
def save_game():
    with open(SAVE_FILE, "w") as f:
        json.dump(player, f)
    print("\n💾 Game saved!\n")

def load_game():
    global player
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            player = json.load(f)
        print("\n📂 Game loaded!\n")
    else:
        print("\n⚠ No saved game found.\n")

def show_location():
    loc = locations[player["location"]]
    print(f"\n📍 Location: {player['location'].capitalize()}")
    print(loc["description"])
    if loc["items"]:
        print(f"🪙 Items here: {', '.join(loc['items'])}")
    print(f"🚶 Paths: {', '.join(loc['paths'])}")

def move(destination):
    if destination in locations[player["location"]]["paths"]:
        player["location"] = destination
        print(f"\n➡ You move to the {destination}.")
        show_location()
    else:
        print("❌ You can't go there.")
def take_item(item):
    loc = locations[player["location"]]
    if not loc["items"]:
        print("📦 No items here.")
        return
    if item in loc["items"]:
        player["inventory"].append(item)
        loc["items"].remove(item)
        print(f"✅ You picked up {item}.")
    else:
        print("❌ That item isn't here.")
def use_item(item):
    if not player["inventory"]:
        print("📭 You have no items.")
        return
    if item in player["inventory"]:
        if player["location"] == "shop" and item == "magic stone":
            print("🗡 You trade the magic stone for a sword!")
            player["inventory"].remove("magic stone")
            player["inventory"].append("sword")
        elif player["location"] == "cave" and item == "sword":
            print("🐉 You slay the dragon and take the treasure! YOU WIN!")
            player["inventory"].append("treasure")
            save_game()
            exit()
        else:
            print(f"ℹ You can't use {item} here.")
    else:
        print("❌ You don't have that item.")

def show_inventory():
    if player["inventory"]:
        print("🎒 Inventory:", ", ".join(player["inventory"]))
    else:
        print("📭 Your inventory is empty.")
        
def show_help():
    print("""
📜 HOW TO PLAY:
Commands:
  look        - Show your current location and paths
  move        - Travel to another location
  take        - Pick up an item here
  use         - Use an item from your inventory
  inventory   - See items you carry
  save        - Save your progress
  load        - Load saved game
  help        - Show this help message
  walkthrough - Show an example path to win
  quit        - Exit the game

🎯 Goal:
Explore locations, collect useful items, and figure out how to defeat the dragon to win the treasure.
    """)

def show_walkthrough():
    print("""
🗺 Example Walkthrough to Win:
1. Type: look
2. Type: move → forest
3. Type: take → magic stone
4. Type: move → village
5. Type: move → shop
6. Type: use → magic stone  (Get sword)
7. Type: move → village
8. Type: move → forest
9. Type: move → cave
10. Type: use → sword  (Slay dragon and win treasure!)
    """)

# -----------------------
# Main Game Loop
# -----------------------
print("=== TEXT ADVENTURE GAME ===")
print("Commands: move, take, use, look, inventory, save, load, help, walkthrough, quit")

print("Type 'help' at any time for instructions.")
show_help()
show_location()  # Show initial location description when game starts

while True:
    user_input = input("\n> ").lower().strip()
    if not user_input:
        continue
    
    parts = user_input.split(maxsplit=1)
    command = parts[0]
    argument = parts[1] if len(parts) > 1 else None

    if command == "move":
        if argument:
            move(argument)
        else:
            print("Where do you want to move?")
    elif command == "look":
        show_location()
    elif command == "take":
        if argument:
            take_item(argument)
        else:
            print("What do you want to take?")
    elif command == "use":
        if argument:
            use_item(argument)
        else:
            print("What do you want to use?")
    elif command == "inventory":
        show_inventory()
    elif command == "save":
        save_game()
    elif command == "load":
        load_game()
    elif command == "help":
        show_help()
    elif command == "walkthrough":
        show_walkthrough()
    elif command == "quit":
        print("👋 Goodbye!")
        break
    else:
        print("❓ Unknown command. Try: move, take, use, look, inventory, save, load, help, walkthrough, quit")



   

