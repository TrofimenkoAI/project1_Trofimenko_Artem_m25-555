ROOMS = {
    "entrance": {
        "description": (
            "Вы в темном входе лабиринта. Стены покрыты мхом. "
            "На полу лежит старый факел."
        ),
        "exits": {"north": "hall", "east": "trap_room"},
        "items": ["torch"],
        "puzzle": None,
    },
    "hall": {
        "description": (
            "Большой и пустой зал с эхом."
        ),
        "exits": {"south": "entrance", "west": "library", "north": "treasure_room"},
        "items": [],
        "puzzle": None,
    },
    "trap_room": {
        "description": (
            'Комната с хитрой плиточной поломкой. На стене видна надпись: '
            '"Осторожно — ловушка".'
        ),
        "exits": {"west": "entrance", "north": "crypt"},
        "items": ["rusty_key"],
        "puzzle": (
            'Система плит активна. Чтобы пройти, назовите слово "шаг" три раза подряд '
            '(введите "шаг шаг шаг")',
            "шаг шаг шаг",
        ),
    },
    "library": {
        "description": (
            "Пыльная библиотека. На полках старые свитки. "
            "Где-то здесь может быть ключ от сокровищницы."
        ),
        "exits": {"east": "hall", "north": "armory", "west": "observatory"},
        "items": ["ancient_book"],
        "puzzle": (
            "В одном свитке загадка: висит груша – нельзя скушать",
            "лампочка",
        ),
    },
    "armory": {
        "description": (
            """Старая оружейная комната. На стене висит меч, рядом — 
небольшая бронзовая шкатулка."""
        ),
        "exits": {"south": "library"},
        "items": ["sword", "bronze_box"],
        "puzzle": None,
    },
    "treasure_room": {
        "description": "Комната, на столе большой сундук. "
        "Дверь заперта — нужен особый ключ.",
        "exits": {"south": "hall"},
        "items": ["treasure_chest"],
        "puzzle": (
            "Дверь защищена кодом. Введите код (подсказка: это квадрат четвёртого "
            "по порядку простого числа)",
            "25",
        ),
    },
    "crypt": {
        "description": (
            "Сырая крипта с каменными нишами в стенах. В углу лежит серебряный амулет."
        ),
        "exits": {"south": "trap_room"},
        "items": ["silver_amulet"],
        "puzzle": None,
    },
    "observatory": {
        "description": (
            "Заброшенная обсерватория. Сквозь трещину в потолке видны звезды. "
            "На столе лежит потёртая карта."
        ),
        "exits": {"east": "library"},
        "items": ["map_fragment"],
        "puzzle": (
            'На карте надпись: "Сколько сторон у треугольника?" (ответ цифрой)',
            "3",
        ),
    },
}
