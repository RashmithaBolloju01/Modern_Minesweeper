# Modern Minesweeper

Modern Minesweeper is a Python-based desktop application that reimplements the classic Minesweeper game with an enhanced graphical interface, sound integration, and structured gameplay design. The project emphasizes modular programming, event-driven architecture, and user experience, making it both suitable for learning purposes and extensible for advanced features.

# Project Overview

This project focuses on developing a fully functional Minesweeper game using Python and Tkinter. It combines traditional game logic with modern interface elements such as dynamic difficulty selection, interactive feedback, and sound effects.

The application is designed with a modular structure that separates core logic, UI components, and auxiliary systems such as sound handling and leaderboard management. This structure allows easy extension into more advanced implementations, including animation support or intelligent hint systems.

# Features

## Core Gameplay

- Grid-based Minesweeper implementation
- Left-click to reveal cells
- Right-click to flag suspected mines
- Recursive expansion for empty cells
- Win and loss detection logic

## Difficulty Levels

- Easy: 6 × 6 grid with 10 mines
- Medium: 8 × 8 grid with 8 mines
- Hard: 10 × 10 grid with 30 mines

## Sound Integration

- Click sound for safe cell reveal
- Explosion sound for mine trigger
- Flag placement sound
- Win notification sound

## Interactive Feedback

- Contextual messages such as “Nice Move”, “Great”, “BOOM”, and “Victory”
- Temporary visual feedback displayed during gameplay

## Leaderboard System

- Stores player name and completion time
- Maintains a history of recent scores
- Displays results in a structured table

## User Interface

- Dark-themed layout for improved readability
- High-contrast controls for accessibility
- Structured layout with clear separation of components

# Technologies Used

Category| Tools & Libraries
Language| Python 3
GUI Framework| Tkinter
Sound System| Pygame
Data Storage| CSV (leaderboard)
Standard Libraries| random, os, csv

# Project Structure

Minesweeper/
├── main.py               # Main application logic and UI
├── sound_manager.py      # Sound handling module
├── leaderboard.csv       # Score storage
├── assets/
│   └── sounds/           # Audio files
├── README.md             # Documentation
└── .gitignore

# How to Run

## Clone the repository:
git clone https://github.com/<your-username>/Modern-Minesweeper.git
cd Modern-Minesweeper
## Install dependencies:
pip install pygame
## Run the application:
python main.py

# Sample Use Case

The user launches the application and selects a difficulty level. The grid is generated dynamically based on the selected configuration. The player interacts with the grid by revealing cells and flagging suspected mines.

## During gameplay:

- Safe moves reveal numbers or empty cells
- Incorrect moves trigger a mine and end the game
- Feedback messages provide real-time interaction cues

## Upon successful completion:

- The user is prompted to enter their name
- The score is recorded in the leaderboard
- Results can be viewed in a separate leaderboard window

# Future Enhancements

- Graphical animations and transition effects
- Intelligent hint system for decision support
- Enhanced leaderboard interface with ranking metrics
- Database integration (e.g., SQLite) for persistent storage
- Web-based or cross-platform deployment

# License

This project is licensed under the MIT License.
