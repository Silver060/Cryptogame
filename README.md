# Crypto Trader: Arcade Broker

An offline desktop crypto trading game built with Python and Tkinter.

## Features

- Arcade-style trading dashboard
- Clickable market coin tiles with price, daily move, holdings, live P/L, and difficulty-aware trading signal badges
- Large selected-coin decision panel with a prominent trend chart, trade controls, news, momentum, sentiment, and difficulty-aware helper
- Short-term signals such as Strong Buy, Dip Buy, Good Buy, Wait, Risky Chase, Take Profit, Falling Knife, and Bad Buy
- Easy guided broker helper, Medium compact helper, and Hard raw-market mode with signals hidden
- Horizontal market news ticker with generated daily headlines
- Structured market news events with target, price impact, sentiment impact, ticker text, and explanations
- Compact position tiles with combined buys, weighted average buy price, held days, live P/L, and quick sell buttons
- Trade ticket with quick buy/sell controls
- Market mood, coin momentum, sentiment, and event-driven price movement
- Weak rumour signals that raise sector/coin volatility for a few days
- Sector-wide events for Majors, Meme, Privacy, Infrastructure, and Exchange coins
- Transaction fees and buy/sell spread, so overtrading has a cost
- Fractional crypto buying, including Buy Max for expensive coins like Bitcoin
- Return-percentage high scores with difficulty and run length
- Value-based portfolio risk limit instead of confusing coin-unit capacity
- Trade history panel for each run

## How To Play

1. Pick a difficulty and run length.
2. Select a coin tile from Market Watch.
3. Enter an amount or use Buy Max/Sell All.
4. Watch signal badges, confidence, market mood, rumours, news, and your wallet P/L.
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

- Select a coin from the market tiles
- Enter a trade amount
- Buy, Sell, Buy Max, or Sell All
- Advance to the next day
- Review position tiles and trade history
- Use the sidebar buttons for Market, Wallet, Trade History, Achievements, High Scores, and How To Play

## Run From Source

Requires Python 3.12 or newer.

```powershell
python crypto_game.py
```

## Build The EXE

Install PyInstaller, then run:

```powershell
pyinstaller --onefile --windowed --name crypto_game_v1.5 crypto_game.py
```

Packaged builds should be uploaded through GitHub Releases rather than committed
to the repository.

Local executable builds should use semantic-ish version names:

```text
crypto_game_v1.1.exe
crypto_game_v1.2.exe
crypto_game_v1.3.exe
crypto_game_v1.4.exe
crypto_game_v1.5.exe
```

Use the next minor version for normal feature/fix builds, and reserve bigger
version jumps for larger redesigns.

High scores are stored locally in `%APPDATA%/Crypto Trader/high_scores.json` on
Windows, with a local fallback if that folder is unavailable.

## Roadmap

- GitHub Releases for downloadable builds
- More achievements
- Richer rumour/event chains
- Deeper tutorial/tooltips
- Better charting
