import math

from labyrinth_game.constants import ROOMS


def pseudo_random(seed: int, modulo: int) -> int:
    if modulo <= 0:
        return 0
    x = math.sin(seed * 13.7777) * 54371.5453
    frac = x - math.floor(x)
    return int(frac * modulo)


def describe_current_room(game_state: dict) -> None:
    current_room_name = game_state["current_room"]
    room = ROOMS[current_room_name]

    print(f"== {current_room_name.upper()} ==")
    print(room["description"])

    items = room.get("items", [])
    if items:
        print("Заметные предметы:", ", ".join(items))

    exits = room.get("exits", {})
    if exits:
        print("Выходы:", ", ".join(exits.keys()))
    else:
        print("Выходы: нет")

    if room.get("puzzle") is not None:
        print("Кажется, здесь есть загадка (используйте команду solve).")


def trigger_trap(game_state: dict) -> None:
    print("Ловушка активирована! Пол стал дрожать...")

    inventory = game_state["player_inventory"]
    seed = int(game_state.get("steps_taken", 0))

    if inventory:
        idx = pseudo_random(seed + 31, len(inventory))
        lost_item = inventory.pop(idx)
        print(f"Вы потеряли предмет: {lost_item}")
        return

    roll = pseudo_random(seed + 59, 10)
    if roll < 3:
        print("Вы не выдержали удар ловушки. Вы проиграли.")
        game_state["game_over"] = True
    else:
        print("Вы чудом уцелели.")


def random_event(game_state: dict) -> None:
    seed = int(game_state.get("steps_taken", 0))
    chance = pseudo_random(seed + 7, 10)
    if chance != 0:
        return

    event_id = pseudo_random(seed + 13, 3)
    current_room = game_state["current_room"]
    room = ROOMS[current_room]
    inventory = game_state["player_inventory"]

    if event_id == 0:
        print("Вы замечаете на полу монетку.")
        items = room.setdefault("items", [])
        items.append("coin")
    elif event_id == 1:
        print("Вы слышите шорох где-то рядом.")
        if "sword" in inventory:
            print("Вы сжимаете меч, и существо отступает.")
    else:
        if current_room == "trap_room" and "torch" not in inventory:
            print("В темноте вы не замечаете опасную плиту под ногами...")
            trigger_trap(game_state)


def solve_puzzle(game_state: dict) -> None:
    room = ROOMS[game_state["current_room"]]
    puzzle = room.get("puzzle")

    if puzzle is None:
        print("Загадок здесь нет.")
        return

    question, correct_answer = puzzle
    print(question)
    user_answer = input("Ваш ответ: ").strip().lower()

    if user_answer == str(correct_answer).strip().lower():
        print("Верно! Загадка решена.")
        room["puzzle"] = None
        if "treasure_key" not in game_state["player_inventory"]:
            game_state["player_inventory"].append("treasure_key")
    else:
        print("Неверно. Попробуйте снова.")


def attempt_open_treasure(game_state: dict) -> None:
    room = ROOMS[game_state["current_room"]]
    items = room.get("items", [])
    inventory = game_state["player_inventory"]

    if "treasure_key" in inventory:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        if "treasure_chest" in items:
            items.remove("treasure_chest")
        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
        return

    answer = input("Сундук заперт. Ввести код? (да/нет) ").strip().lower()
    if answer != "да":
        print("Вы отступаете от сундука.")
        return

    puzzle = room.get("puzzle")
    if puzzle is None:
        print("Кода нет.")
        return

    question, correct_code = puzzle
    code = input("Введите код (подсказка: это квадрат "
                 "четвёртого по порядку простого числа): ").strip()

    if code == str(correct_code).strip():
        print("Код верный. Сундук открыт!")
        if "treasure_chest" in items:
            items.remove("treasure_chest")
        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
    else:
        print("Неверный код.")

def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")
