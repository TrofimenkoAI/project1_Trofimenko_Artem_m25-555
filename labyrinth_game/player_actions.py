from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room, random_event


def show_inventory(game_state: dict) -> None:
    inventory = game_state["player_inventory"]

    if inventory:
        print("Инвентарь:", ", ".join(inventory))
    else:
        print("Инвентарь пуст.")


def get_input(prompt: str = "> ") -> str:
    try:
        return input(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

def move_player(game_state: dict, direction: str) -> None:
    room = ROOMS[game_state["current_room"]]
    exits = room.get("exits", {})
    if direction not in exits:
        print("Нельзя пойти в этом направлении.")
        return

    next_room = exits[direction]
    inventory = game_state["player_inventory"]

    if next_room == "treasure_room":
        if "rusty_key" in inventory:
            print("Вы используете найденный ключ, чтобы открыть путь "
                  "в комнату сокровищ.")
        else:
            print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
            return

    game_state["current_room"] = next_room
    game_state["steps_taken"] += 1
    describe_current_room(game_state)
    random_event(game_state)


def take_item(game_state: dict, item_name: str) -> None:
    room = ROOMS[game_state["current_room"]]
    items = room.get("items", [])
    if item_name in items:
        game_state["player_inventory"].append(item_name)
        items.remove(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")


def use_item(game_state: dict, item_name: str) -> None:
    inventory = game_state["player_inventory"]
    if item_name not in inventory:
        print("У вас нет такого предмета.")
        return
    if item_name == "torch":
        print("Стало светлее.")
    elif item_name == "silver_amulet":
        print("Вы сломали амулет и он сказал вам идти в обсерваторию.")
    elif item_name == "map_fragment":
        print("Карта показывает, что ключ на востоке от входа.")
    elif item_name == "sword":
        print("Вы чувствуете уверенность.")
    elif item_name == "bronze_box":
        if "rusty_key" not in inventory:
            print("Вы открыли шкатулку.")
            inventory.append("rusty_key")
    else:
        print("Вы не знаете, как использовать этот предмет.")

