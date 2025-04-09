# 🎰 Python Slot Machine
A simple terminal-based slot machine game built in Python.

## What it Does
- Simulates 3 spinning reels with random symbols (like a real slot machine).
- Calculates and awards winnings based on matching lines.
- Lets the player bet on 1–3 lines and tracks their balance.
- Features different symbol rarities and payouts.

## 🕹️ How to Play
1. Run the game:

```bash
python slot_machine.py
```

2. Deposit some money into your balance.
3. Choose:
How many lines you want to bet on (1–3).
How much money to bet per line.
4. Spin the slot machine and see if you win!
5. Continue playing until you choose to quit.

## 🪙 Symbols & Payouts

| Symbol | Emoji | Frequency     | Payout Multiplier |
|--------|-------|---------------|-------------------|
| A      | 💎    | Very Rare     | x10               |
| B      | 🍒    | Rare          | x5                |
| C      | 🔔    | Common        | x6                |
| D      | 🍋    | Very Common   | x4                |
| E      | 🍉    | Rare          | x3                |
| F      | 🍀    | Very Common   | x2                |

The rarer the symbol, the bigger the payout — but the harder it is to match!

## 🧪 Tests
This project includes unit tests for:

Symbol creation

SlotMachine logic (spin & winnings)

Player balance and input validation

Game interaction logic

To run tests:

```bash
python -m unittest discover -s . -p "*_test.py"
```

## 📁 File Structure
```bash
📦 Spaced-Repetition/
├── slot_machine.py        # Main game logic
├── test_slot_machine.py   # Unit tests
├── README.md              # Project documentation
```

## 💡 Ideas for Expansion
Diagonal win detection

Bonus rounds or free spins

GUI version (e.g. with Tkinter or Pygame)

High score tracker

Save/load balance between runs

### 👩‍💻 Author
Built by @aegarcia03 as a learning project 

