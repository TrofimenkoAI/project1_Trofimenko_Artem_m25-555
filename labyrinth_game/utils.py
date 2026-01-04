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
