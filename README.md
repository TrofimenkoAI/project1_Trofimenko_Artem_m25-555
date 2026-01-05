# Лабиринт сокровищ

Консольная игра на Python: исследуйте комнаты лабиринта, собирайте предметы, решайте загадки и откройте сокровищницу.

## Установка и запуск

Требования: Python 3.11+, Poetry.

make install
make project

## Управление

Основные команды:

- `look` — осмотреть текущую комнату  
- `go <direction>` — перейти в направлении (`north`, `south`, `east`, `west`)  
- `north` / `south` / `east` / `west` — перейти в направлении без команды `go`  
- `take <item>` — поднять предмет  
- `use <item>` — использовать предмет из инвентаря  
- `inventory` — показать инвентарь  
- `solve` — решить загадку в комнате (в комнате сокровищ — попытка открыть сундук)  
- `help` — показать список команд  
- `quit` — выйти из игры

## Демонстрация (asciinema)

[![asciicast](https://asciinema.org/a/vDnaQbCigsMTkuNqRLOQKA6yx.svg)](https://asciinema.org/a/vDnaQbCigsMTkuNqRLOQKA6yx?autoplay=1)



