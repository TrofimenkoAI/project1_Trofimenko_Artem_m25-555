#!/usr/bin/env python3


from labyrinth_game.constants import COMMANDS
from labyrinth_game.player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from labyrinth_game.utils import (
    attempt_open_treasure,
    describe_current_room,
    show_help,
    solve_puzzle,
)


def process_command(game_state: dict, command: str, commands: dict) -> None:
    parts = command.strip().split()
    if not parts:
        return
    cmd = parts[0].lower()
    arg = parts[1] if len(parts) > 1 else ""
    match cmd:
        case "look":
            describe_current_room(game_state)
        case "use":
            if arg:
                use_item(game_state, arg)
        case "go":
            if arg:
                move_player(game_state, arg)
        case "north" | "south" | "east" | "west":
            move_player(game_state, cmd)
        case "take":
            if arg:
                take_item(game_state, arg)
        case "inventory":
            show_inventory(game_state)
        case "help":
            show_help(commands)
        case "solve":
            if game_state["current_room"] == "treasure_room":
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
        case "quit" | "exit":
            game_state["game_over"] = True
        case _:
            print("Нет такой команды, используйте help для вывода возможных команд.")


def main() -> None:
    game_state = {
        "player_inventory": [],  # Инвентарь игрока
        "current_room": "entrance",  # Текущая комната
        "game_over": False,  # Значения окончания игры
        "steps_taken": 0,  # Количество шагов
    }

    print("Добро пожаловать в Лабиринт сокровищ! "
          "(Используйте help для вывода списка команд.)")
    describe_current_room(game_state)
    while not game_state["game_over"]:
        command = get_input("> ")
        process_command(game_state, command, COMMANDS)


if __name__ == "__main__":
    main()
