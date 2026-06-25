# Crypto Trader: Arcade Broker

An offline desktop crypto trading game built with Python and Tkinter.

## Latest Build

Run the packaged Windows build:

```text
dist/crypto_game_arcade_broker_engine_polish.exe
```

## Features

- Arcade-style trading dashboard
- Market watch table with price, movement, holdings, value, and profit/loss
- Compact visual wallet with combined positions and weighted average buy price
- Trade ticket with quick buy/sell controls
- Market mood, coin momentum, sentiment, and event-driven price movement
- High score saving beside the app/executable

## Run From Source

Requires Python 3.12 or newer.

```powershell
python crypto_game.py
```

## Build The EXE

Install PyInstaller, then run:

```powershell
pyinstaller --onefile --windowed --name crypto_game_arcade_broker_engine_polish crypto_game.py
```

High scores are stored locally in `high_scores.json` beside the script or executable.
