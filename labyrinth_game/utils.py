from labyrinth_game.constants import ROOMS


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
