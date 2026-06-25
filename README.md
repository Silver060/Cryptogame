# Crypto Trader: Arcade Broker

An offline desktop crypto trading game built with Python and Tkinter.

## Features

- Arcade-style trading dashboard
- Market watch table with price, movement, holdings, value, and profit/loss
- Compact visual wallet with combined positions and weighted average buy price
- Trade ticket with quick buy/sell controls
- Market mood, coin momentum, sentiment, and event-driven price movement
- Fractional crypto buying, including Buy Max for expensive coins like Bitcoin
- Return-percentage high scores with difficulty and run length
- Value-based portfolio risk limit instead of confusing coin-unit capacity
- Trade history panel for each run

## How To Play

1. Pick a difficulty and run length.
2. Select a coin from Market Watch.
3. Enter an amount or use Buy Max/Sell All.
4. Watch market mood, momentum, sentiment, news, and your wallet P/L.
5. Survive the run and chase the highest return percentage.

## Scoring

High scores are ranked by return percentage, not raw money. This keeps Easy,
Medium, and Hard runs more comparable.

Saved scores include:

- Player name
- Final net worth
- Difficulty
- Run length
- Starting cash
- Return percentage

## Controls

- Select a coin from the market table
- Enter a trade amount
- Buy, Sell, Buy Max, or Sell All
- Advance to the next day
- Review wallet positions and trade history

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

Packaged builds should be uploaded through GitHub Releases rather than committed
to the repository.

High scores are stored locally in `%APPDATA%/Crypto Trader/high_scores.json` on
Windows, with a local fallback if that folder is unavailable.

## Roadmap

- GitHub Releases for downloadable builds
- Achievements
- More sector-based market events
- Tutorial/tooltips for momentum, sentiment, and risk limit
- Better charting
