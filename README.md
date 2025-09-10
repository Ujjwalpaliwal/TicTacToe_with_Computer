# 🎮 Tic-Tac-Toe AI Project

## 🔹 Project Overview
This project implements the classic **Tic-Tac-Toe (X-O game)** in two versions:

- **Console Version (`tictactoe.py`)** – A text-based game where the user plays against the computer in the terminal.  
- **Graphical Version (`withGUI.py`)** – A modern **Tkinter GUI-based game** with a smarter AI opponent using the **Minimax algorithm with alpha-beta pruning**.  

---

## 🔹 Features

### 1. Console Version (`tictactoe.py`)
- Text-based interface in the terminal.  
- Player chooses whether to move first or let the computer start.  
- Computer uses a **rule-based strategy**:
  - First tries to win immediately.  
  - If not possible, it blocks the human’s winning move.  
  - Otherwise, it picks the best available square (center > corners > edges).  
- Detects winners, ties, and displays final results.  

### 2. GUI Version (`withGUI.py`)
- Built using **Python’s Tkinter library**.  
- Graphical 3x3 board with clickable buttons.  
- **Minimax with alpha-beta pruning** ensures an unbeatable AI:
  - `X` tries to maximize the score.  
  - `O` tries to minimize the score.  
- Human chooses whether to go first.  
- Scoreboard to track **Wins / Losses / Ties**.  
- Pop-up messages announce results.  
- Option to start a new game or quit anytime.  

---

## 🔹 Tech Stack
- **Python** (core logic & AI)  
- **Tkinter** (for GUI interface)  
- **Algorithms**:  
  - Rule-based AI (Console version)  
  - Minimax with Alpha-Beta Pruning (GUI version)  

---

## 🔹 Learning Outcomes
- Understanding of **game state representation** (board as a list).  
- Implementing **legal moves, winner detection, and game rules**.  
- Applying **AI strategies** (greedy rule-based vs Minimax).  
- Building interactive applications with **Tkinter GUI**.  
- Basics of **alpha-beta pruning optimization** in game search.  

---

## 🚀 How to Run
1. Clone this repository:  
   ```bash
   git clone https://github.com/your-username/tic-tac-toe.git
   cd tic-tac-toe

