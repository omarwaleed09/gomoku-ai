# Gomoku AI

A Python implementation of the Gomoku (Five in a Row) game with AI.  
Play against the computer or let two AIs compete.

## Features

- Human vs AI
- AI vs AI
- 15x15 board
- Graphical user interface using `tkinter`
- AI uses Minimax algorithm with alpha-beta pruning




### Gomoku game

![Gomoku1](https://github.com/omarwaleed09/Omar-Waleed/blob/main/Gomoku-ai/Screenshots/gomoku1.png)


![Gomoku2](https://github.com/omarwaleed09/Omar-Waleed/blob/main/Gomoku-ai/Screenshots/gomoku2.png)


## Requirements

- Python 3.x
- `tkinter` (included with standard Python)

Optional (if using images):

```bash
pip install pillow
```

## How to Run

Clone the repository:

```bash
git clone https://github.com/omarwaleed09/gomoku-ai.git
cd gomoku-ai
```

Run the game:

```bash
python GOMOKU.py
```

Choose mode:

- Press `1` for Human vs AI  
- Press `2` for AI vs AI

## Files

```bash
gomoku-ai/
├── GOMOKU.py            # Full game (GUI + AI)
└── .gitignore
```

## .gitignore

```bash
__pycache__/
*.pyc
*.pyo
*.pyd
env/
```
