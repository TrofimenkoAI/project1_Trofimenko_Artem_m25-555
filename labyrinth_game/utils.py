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


def _normalize_answer(value: str) -> str:
    s = str(value).strip().lower().replace("ё", "е")
    s = " ".join(s.split())
    return s


def _russian_number_words(n: int) -> str:
    ones = {
        0: "ноль",
        1: "один",
        2: "два",
        3: "три",
        4: "четыре",
        5: "пять",
        6: "шесть",
        7: "семь",
        8: "восемь",
        9: "девять",
        10: "десять",
        11: "одиннадцать",
        12: "двенадцать",
        13: "тринадцать",
        14: "четырнадцать",
        15: "пятнадцать",
        16: "шестнадцать",
        17: "семнадцать",
        18: "восемнадцать",
        19: "девятнадцать",
    }
    tens = {
        20: "двадцать",
        30: "тридцать",
        40: "сорок",
        50: "пятьдесят",
        60: "шестьдесят",
        70: "семьдесят",
        80: "восемьдесят",
        90: "девяносто",
    }

    if n in ones:
        return ones[n]
    if n in tens:
        return tens[n]
    if 20 < n < 100:
        t = (n // 10) * 10
        o = n % 10
        if t in tens and o in ones:
            return f"{tens[t]} {ones[o]}"
    return str(n)


def _accepted_answers(correct_answer) -> set[str]:
    answers = {_normalize_answer(correct_answer)}

    s = str(correct_answer).strip()
    try:
        n = int(s)
        answers.add(_normalize_answer(n))
        answers.add(_normalize_answer(_russian_number_words(n)))
    except ValueError:
        pass

    return answers


def solve_puzzle(game_state: dict) -> None:
    current_room_name = game_state["current_room"]
    room = ROOMS[current_room_name]
    puzzle = room.get("puzzle")

    if puzzle is None:
        print("Загадок здесь нет.")
        return

    question, correct_answer = puzzle
    print(question)
    user_answer = input("Ваш ответ: ").strip()

    accepted = _accepted_answers(correct_answer)
    if _normalize_answer(user_answer) in accepted:
        print("Верно! Загадка решена.")
        room["puzzle"] = None

        rewards = {
            "library": "treasure_key",
            "observatory": "map_fragment",
        }
        reward = rewards.get(current_room_name)
        if reward:
            inventory = game_state["player_inventory"]
            if reward not in inventory:
                inventory.append(reward)
            items = room.get("items", [])
            if reward in items:
                items.remove(reward)
    else:
        print("Неверно. Попробуйте снова.")
        if current_room_name == "trap_room":
            trigger_trap(game_state)


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

def show_help(commands: dict) -> None:
    print("\nДоступные команды:")
    for command, description in commands.items():
        print(f"  {command:<16} - {description}")
