# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a Zenn books repository containing Japanese technical documentation and tutorials. Zenn is a Japanese technical publishing platform. The repository contains three books:
- `pygame_tutorial/` - Introduction to pygame
- `python_basic/` - Basic Python tutorial
- `python_maze_game/` - Python maze game tutorial with pygame

## Key Commands

### Zenn CLI Commands
```bash
# Preview books locally
npx zenn preview

# Create a new book
npx zenn new:book
```

### Python Development (for python_maze_game)
The maze game project uses Task (go-task) for automation. Navigate to `books/python_maze_game/src/` first:

```bash
# Setup virtual environment and install dependencies
task install

# Run the final game
task run

# Run specific chapters (01-08)
task run01  # Chapter 1: Basic movement
task run02  # Chapter 2: Map and floor
# ... up to run08

# Check Python syntax
task test

# List available tasks
task help
```

## Architecture

### Zenn Structure
- Each book is in `books/[book-name]/`
- Book configuration in `config.yaml` specifies chapters and metadata
- Chapters are markdown files (e.g., `example1.md`, `01.md`)
- Images stored in `images/` or `image/` subdirectories

### Python Maze Game Structure
- Tutorial code organized by chapters (`01.py` through `08.py`)
- Final complete version in `main.py`
- Sound assets in `assets/sounds/`
- Uses pygame for game development
- Virtual environment managed with venv

## Important Notes

- All content is in Japanese
- Slug naming rules: 12-50 characters using only a-z, 0-9, -, _
- Slugs cannot be changed once published on zenn.dev
- Books can be free (price: 0) or paid (200-5000)