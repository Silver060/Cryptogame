import json
import math
import os
import random
import sys
import tkinter as tk
import tkinter.simpledialog as sd
from collections import deque
from tkinter import messagebox, ttk


class CryptoTraderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crypto Trader: Arcade Broker")
        self.root.geometry("1180x760")
        self.root.minsize(1040, 680)

        self.colors = {
            "bg": "#f4f7fb",
            "panel": "#ffffff",
            "panel_alt": "#eef3f8",
            "nav": "#061529",
            "nav_alt": "#0b213c",
            "ink": "#172033",
            "muted": "#65738a",
            "line": "#d9e1ec",
            "accent": "#2563eb",
            "accent_dark": "#1d4ed8",
            "neon": "#22c55e",
            "gold": "#f59e0b",
            "amber": "#d97706",
            "green": "#16a34a",
            "red": "#dc2626",
            "purple": "#7c3aed",
        }

        self.max_days = 30
        self.day = 1
        self.cash = 1000.0
        self.starting_cash = 1000.0
        self.risk_limit = 500.0
        self.game_over = False
        self.total_trades = 0
        self.best_trade = 0.0
        self.worst_trade = 0.0
        self.market_event_chance = 0.1
        self.rumour_chance = 0.22
        self.transaction_fee_rate = 0.005
        self.spread_rate = 0.0025
        self.high_score_file = self.get_data_path("high_scores.json")
        self.selected_coin_name = "Bitcoin"
        self.event_feed = deque(maxlen=8)
        self.news_items = deque(maxlen=10)
        self.sort_reverse = True
        self.wallet_lots = []
        self.next_lot_id = 1
        self.trade_history = deque(maxlen=80)
        self.active_rumours = []
        self.market_tile_widgets = {}
        self.position_tile_widgets = []

        self.coins = [
            self.make_coin("Bitcoin", 20000.0, 0.07, "Majors"),
            self.make_coin("Ethereum", 1500.0, 0.10, "Majors"),
            self.make_coin("Binance Coin", 300.0, 0.08, "Exchange"),
            self.make_coin("Polkadot", 8.0, 0.12, "Infrastructure"),
            self.make_coin("Cardano", 0.40, 0.16, "Infrastructure"),
            self.make_coin("Dogecoin", 0.10, 0.25, "Meme"),
            self.make_coin("Monero", 151.0, 0.09, "Privacy"),
            self.make_coin("Chainlink", 18.0, 0.14, "Infrastructure"),
        ]

        self.configure_styles()

        self.shell = ttk.Frame(self.root, style="App.TFrame")
        self.shell.pack(fill="both", expand=True)

        self.start_frame = ttk.Frame(self.shell, style="App.TFrame", padding=28)
        self.game_frame = ttk.Frame(self.shell, style="App.TFrame", padding=18)

        self.create_start_frame()
        self.create_game_frame()
        self.show_start_frame()

    def make_coin(self, name, price, volatility, sector):
        return {
            "name": name,
            "sector": sector,
            "price": price,
            "initial_price": price,
            "inventory": 0.0,
            "volatility": volatility,
            "average_cost": 0.0,
            "previous_price": price,
            "price_history": deque([price], maxlen=60),
            "momentum": 0.0,
            "sentiment": 0.0,
        }

    def configure_styles(self):
        self.root.configure(bg=self.colors["bg"])
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("App.TFrame", background=self.colors["bg"])
        style.configure("Panel.TFrame", background=self.colors["panel"], relief="flat")
        style.configure("Alt.TFrame", background=self.colors["panel_alt"])
        style.configure("Nav.TFrame", background=self.colors["nav"])
        style.configure("NavCard.TFrame", background=self.colors["nav_alt"])
        style.configure("Title.TLabel", background=self.colors["bg"], foreground=self.colors["ink"], font=("Segoe UI", 24, "bold"))
        style.configure("Subtitle.TLabel", background=self.colors["bg"], foreground=self.colors["muted"], font=("Segoe UI", 11))
        style.configure("NavLogo.TLabel", background=self.colors["nav"], foreground="#ffffff", font=("Segoe UI", 22, "bold"))
        style.configure("NavAccent.TLabel", background=self.colors["nav"], foreground=self.colors["gold"], font=("Segoe UI", 20, "bold"))
        style.configure("NavItem.TLabel", background=self.colors["nav"], foreground="#d7e5f7", font=("Segoe UI", 11, "bold"))
        style.configure("NavMuted.TLabel", background=self.colors["nav_alt"], foreground="#a9bdd6", font=("Segoe UI", 9))
        style.configure("NavValue.TLabel", background=self.colors["nav_alt"], foreground="#ffffff", font=("Segoe UI", 15, "bold"))
        style.configure("HeroLabel.TLabel", background=self.colors["panel"], foreground=self.colors["muted"], font=("Segoe UI", 10, "bold"))
        style.configure("HeroValue.TLabel", background=self.colors["panel"], foreground=self.colors["green"], font=("Segoe UI", 26, "bold"))
        style.configure("PanelTitle.TLabel", background=self.colors["panel"], foreground=self.colors["ink"], font=("Segoe UI", 12, "bold"))
        style.configure("CardLabel.TLabel", background=self.colors["panel"], foreground=self.colors["muted"], font=("Segoe UI", 9, "bold"))
        style.configure("CardValue.TLabel", background=self.colors["panel"], foreground=self.colors["ink"], font=("Segoe UI", 16, "bold"))
        style.configure("Muted.TLabel", background=self.colors["panel"], foreground=self.colors["muted"], font=("Segoe UI", 9))
        style.configure("Body.TLabel", background=self.colors["panel"], foreground=self.colors["ink"], font=("Segoe UI", 10))
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), padding=(14, 8))
        style.configure("Soft.TButton", font=("Segoe UI", 10), padding=(10, 7))
        style.configure("Buy.TButton", font=("Segoe UI", 10, "bold"), padding=(14, 8), background=self.colors["green"], foreground="#ffffff")
        style.map("Buy.TButton", background=[("active", "#15803d")], foreground=[("active", "#ffffff")])
        style.configure("Treeview", rowheight=32, font=("Segoe UI", 9), background=self.colors["panel"], fieldbackground=self.colors["panel"], foreground=self.colors["ink"], borderwidth=0)
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"), background=self.colors["panel_alt"], foreground=self.colors["muted"], relief="flat", padding=(8, 8))
        style.map("Treeview", background=[("selected", "#dbeafe")], foreground=[("selected", self.colors["ink"])])
        style.configure("Horizontal.TProgressbar", troughcolor=self.colors["line"], background=self.colors["accent"], bordercolor=self.colors["line"], lightcolor=self.colors["accent"], darkcolor=self.colors["accent"])

    # ======================
    #  Start Screen
    # ======================
    def create_start_frame(self):
        self.start_frame.columnconfigure(0, weight=1)
        self.start_frame.columnconfigure(1, weight=1)

        hero = ttk.Frame(self.start_frame, style="App.TFrame")
        hero.grid(row=0, column=0, sticky="nsew", padx=(0, 28))
        ttk.Label(hero, text="Crypto Trader", style="Title.TLabel").pack(anchor="w")
        ttk.Label(hero, text="Arcade Broker Edition", style="Subtitle.TLabel").pack(anchor="w", pady=(2, 20))

        scoreboard = ttk.Frame(hero, style="Panel.TFrame", padding=18)
        scoreboard.pack(fill="x", pady=(0, 18))
        ttk.Label(scoreboard, text="Current hall of fame", style="PanelTitle.TLabel").pack(anchor="w")
        self.start_scores = tk.Listbox(
            scoreboard,
            height=6,
            relief="flat",
            bd=0,
            highlightthickness=0,
            bg=self.colors["panel"],
            fg=self.colors["ink"],
            font=("Segoe UI", 10),
        )
        self.start_scores.pack(fill="x", pady=(10, 0))

        setup = ttk.Frame(self.start_frame, style="Panel.TFrame", padding=22)
        setup.grid(row=0, column=1, sticky="nsew")
        ttk.Label(setup, text="Set up your run", style="PanelTitle.TLabel").pack(anchor="w")
        ttk.Label(setup, text="Pick a pace and risk level before the market opens.", style="Muted.TLabel").pack(anchor="w", pady=(2, 18))

        self.game_length_var = tk.IntVar(value=30)
        ttk.Label(setup, text="Run length", style="CardLabel.TLabel").pack(anchor="w")
        lengths = [(30, "Quick - 30 days"), (60, "Medium - 60 days"), (90, "Long - 90 days")]
        for val, text in lengths:
            ttk.Radiobutton(setup, text=text, variable=self.game_length_var, value=val).pack(anchor="w", pady=3)

        self.difficulty_var = tk.StringVar(value="Easy")
        ttk.Label(setup, text="Difficulty", style="CardLabel.TLabel").pack(anchor="w", pady=(18, 0))
        difficulties = [
            ("Easy", "Easy - GBP 20,000 cash, GBP 30,000 Risk Limit"),
            ("Medium", "Medium - GBP 10,000 cash, GBP 15,000 Risk Limit"),
            ("Hard", "Hard - GBP 1,000 cash, GBP 2,500 Risk Limit"),
        ]
        for val, text in difficulties:
            ttk.Radiobutton(setup, text=text, variable=self.difficulty_var, value=val).pack(anchor="w", pady=3)

        ttk.Button(setup, text="Start trading", style="Accent.TButton", command=self.start_game).pack(fill="x", pady=(24, 8))
        ttk.Button(setup, text="View high scores", style="Soft.TButton", command=self.load_and_show_high_scores).pack(fill="x")

    def show_start_frame(self):
        self.game_frame.pack_forget()
        self.refresh_start_scores()
        self.start_frame.pack(fill="both", expand=True)

    def refresh_start_scores(self):
        if not hasattr(self, "start_scores"):
            return
        self.start_scores.delete(0, "end")
        scores = self.load_high_scores()
        if not scores:
            self.start_scores.insert("end", "No scores yet. Be the first whale.")
            return
        for i, score in enumerate(scores[:6], start=1):
            return_percent = score.get("return_percent")
            difficulty = score.get("difficulty", "Legacy")
            if return_percent is None:
                self.start_scores.insert("end", f"{i}. {score['name']} - GBP {score['net_worth']:,.2f}")
            else:
                self.start_scores.insert("end", f"{i}. {score['name']} - {return_percent:+.1f}% ({difficulty})")

    def start_game(self):
        self.max_days = self.game_length_var.get()
        self.day = 1
        self.game_over = False
        self.event_feed.clear()
        self.news_items.clear()
        self.wallet_lots.clear()
        self.trade_history.clear()
        self.active_rumours.clear()
        self.next_lot_id = 1
        self.total_trades = 0
        self.best_trade = 0.0
        self.worst_trade = 0.0

        difficulty = self.difficulty_var.get()
        if difficulty == "Easy":
            self.cash = 20000.0
            self.starting_cash = 20000.0
            self.risk_limit = 30000.0
        elif difficulty == "Medium":
            self.cash = 10000.0
            self.starting_cash = 10000.0
            self.risk_limit = 15000.0
        else:
            self.cash = 1000.0
            self.starting_cash = 1000.0
            self.risk_limit = 2500.0

        for coin in self.coins:
            coin["price"] = coin["initial_price"]
            coin["inventory"] = 0.0
            coin["average_cost"] = 0.0
            coin["previous_price"] = coin["price"]
            coin["price_history"].clear()
            coin["price_history"].append(coin["price"])
            coin["momentum"] = 0.0
            coin["sentiment"] = 0.0

        self.selected_coin_name = "Bitcoin"
        self.add_news({
            "headline": "Opening bell: market is watching momentum, rumours, and sector risk.",
            "target": "Market",
            "price_impact": 0.0,
            "sentiment_impact": 0.0,
            "ticker": "Opening bell: choose a thesis before the first move.",
            "explanation": "Use the signal badges, momentum, and news ticker to decide where risk looks worthwhile.",
        })
        self.show_game_frame()

    # ======================
    #  Game Screen
    # ======================
    def create_game_frame(self):
        self.game_frame.configure(style="App.TFrame", padding=0)
        self.game_frame.columnconfigure(0, weight=0, minsize=210)
        self.game_frame.columnconfigure(1, weight=1)
        self.game_frame.rowconfigure(0, weight=1)

        nav = ttk.Frame(self.game_frame, style="Nav.TFrame", padding=18)
        nav.grid(row=0, column=0, sticky="nsew")
        ttk.Label(nav, text="CRYPTO", style="NavLogo.TLabel").pack(anchor="w")
        ttk.Label(nav, text="TRADER", style="NavAccent.TLabel").pack(anchor="w", pady=(0, 28))
        nav_actions = (
            ("Dashboard", self.focus_dashboard),
            ("Market", self.focus_market),
            ("Wallet", self.focus_wallet),
            ("Trade History", self.focus_trade_history),
            ("Achievements", self.show_achievements),
            ("High Scores", self.load_and_show_high_scores),
            ("How To Play", self.show_guide),
        )
        for item, command in nav_actions:
            ttk.Button(nav, text=item, style="Soft.TButton", command=command).pack(fill="x", pady=5)
        broker_card = ttk.Frame(nav, style="NavCard.TFrame", padding=14)
        broker_card.pack(side="bottom", fill="x", pady=(20, 0))
        ttk.Label(broker_card, text="ARCADE BROKER", style="NavMuted.TLabel").pack(anchor="w")
        self.nav_rank_label = ttk.Label(broker_card, text="Rookie", style="NavValue.TLabel")
        self.nav_rank_label.pack(anchor="w", pady=(2, 12))
        self.nav_xp_bar = ttk.Progressbar(broker_card, maximum=100, value=0)
        self.nav_xp_bar.pack(fill="x")
        self.nav_wallet_label = ttk.Label(broker_card, text="0 open buys", style="NavMuted.TLabel")
        self.nav_wallet_label.pack(anchor="w", pady=(10, 0))

        content = ttk.Frame(self.game_frame, style="App.TFrame", padding=16)
        content.grid(row=0, column=1, sticky="nsew")
        content.columnconfigure(0, weight=1, minsize=650)
        content.columnconfigure(1, weight=0, minsize=330)
        content.rowconfigure(3, weight=1)
        content.rowconfigure(4, weight=0)

        top = ttk.Frame(content, style="Panel.TFrame", padding=18)
        top.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 14))
        top.columnconfigure(0, weight=1)
        top.columnconfigure(1, weight=1)
        top.columnconfigure(2, weight=0)
        ttk.Label(top, text="NET WORTH", style="HeroLabel.TLabel").grid(row=0, column=0, sticky="w")
        self.hero_net_worth = ttk.Label(top, text="GBP 0.00", style="HeroValue.TLabel")
        self.hero_net_worth.grid(row=1, column=0, sticky="w")
        self.hero_today = ttk.Label(top, text="Today: GBP 0.00", style="Muted.TLabel")
        self.hero_today.grid(row=2, column=0, sticky="w", pady=(4, 0))
        ttk.Label(top, text="RUN PROGRESS", style="HeroLabel.TLabel").grid(row=0, column=1, sticky="w")
        self.day_label = ttk.Label(top, text="Day 1 of 30", style="CardValue.TLabel")
        self.day_label.grid(row=1, column=1, sticky="w")
        self.day_progress = ttk.Progressbar(top, maximum=100, mode="determinate")
        self.day_progress.grid(row=2, column=1, sticky="ew", pady=(8, 0), padx=(0, 18))
        ttk.Button(top, text="High scores", style="Soft.TButton", command=self.load_and_show_high_scores).grid(row=0, column=2, sticky="ew", padx=(10, 0))
        ttk.Button(top, text="Exit run", style="Soft.TButton", command=self.end_game).grid(row=1, column=2, sticky="ew", padx=(10, 0), pady=6)
        self.next_day_button = ttk.Button(top, text="Next day", style="Accent.TButton", command=self.next_day)
        self.next_day_button.grid(row=2, column=2, sticky="ew", padx=(10, 0))

        ticker_frame = ttk.Frame(content, style="Panel.TFrame", padding=(12, 8))
        ticker_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        ticker_frame.columnconfigure(1, weight=1)
        ttk.Label(ticker_frame, text="NEWS", style="CardLabel.TLabel").grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.news_ticker_label = ttk.Label(ticker_frame, text="Market news will appear here.", style="Body.TLabel")
        self.news_ticker_label.grid(row=0, column=1, sticky="ew")

        self.summary_frame = ttk.Frame(content, style="Panel.TFrame", padding=12)
        self.summary_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 14))
        for col in range(6):
            self.summary_frame.columnconfigure(col, weight=1)
        self.summary_labels = {}
        self.build_summary_card(0, "Cash", "cash")
        self.build_summary_card(1, "Holdings", "holdings")
        self.build_summary_card(2, "Risk Limit", "risk_limit")
        self.build_summary_card(3, "Wallet", "lots")
        self.build_summary_card(4, "Mood", "mood")
        self.build_summary_card(5, "Rank", "rank")

        market_panel = ttk.Frame(content, style="Panel.TFrame", padding=14)
        market_panel.grid(row=3, column=0, sticky="nsew", padx=(0, 14), pady=(0, 12))

        market_panel.rowconfigure(1, weight=1)
        market_panel.columnconfigure(0, weight=1)
        market_header = ttk.Frame(market_panel, style="Panel.TFrame")
        market_header.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        market_header.columnconfigure(0, weight=1)
        ttk.Label(market_header, text="Market watch", style="PanelTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Button(market_header, text="Sort price", style="Soft.TButton", command=self.sort_by_price).grid(row=0, column=1, padx=(8, 0))
        self.market_tiles_frame = ttk.Frame(market_panel, style="Panel.TFrame")
        self.market_tiles_frame.grid(row=1, column=0, sticky="nsew")
        for col in range(2):
            self.market_tiles_frame.columnconfigure(col, weight=1)

        wallet_panel = ttk.Frame(content, style="Panel.TFrame", padding=12)
        wallet_panel.grid(row=4, column=0, columnspan=2, sticky="ew")
        wallet_panel.columnconfigure(0, weight=1)
        wallet_header = ttk.Frame(wallet_panel, style="Panel.TFrame")
        wallet_header.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        wallet_header.columnconfigure(0, weight=1)
        ttk.Label(wallet_header, text="Positions", style="PanelTitle.TLabel").grid(row=0, column=0, sticky="w")
        self.wallet_hint = ttk.Label(wallet_header, text="Buys are combined by coin using weighted average buy price.", style="Muted.TLabel")
        self.wallet_hint.grid(row=0, column=1, sticky="e")
        self.position_tiles_frame = ttk.Frame(wallet_panel, style="Panel.TFrame")
        self.position_tiles_frame.grid(row=1, column=0, sticky="ew")
        for col in range(4):
            self.position_tiles_frame.columnconfigure(col, weight=1)

        side = ttk.Frame(content, style="App.TFrame")
        side.grid(row=3, column=1, rowspan=1, sticky="nsew")
        side.rowconfigure(1, weight=1)
        self.trade_panel = ttk.Frame(side, style="Panel.TFrame", padding=16)
        self.trade_panel.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        self.trade_panel.columnconfigure(0, weight=1)
        ttk.Label(self.trade_panel, text="Trade ticket", style="PanelTitle.TLabel").grid(row=0, column=0, columnspan=4, sticky="w")
        coin_card = ttk.Frame(self.trade_panel, style="Panel.TFrame")
        coin_card.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(10, 12))
        self.coin_badge = tk.Canvas(coin_card, width=54, height=54, bg=self.colors["panel"], bd=0, highlightthickness=0)
        self.coin_badge.pack(side="left", padx=(0, 12))
        text_stack = ttk.Frame(coin_card, style="Panel.TFrame")
        text_stack.pack(side="left", fill="x", expand=True)
        self.selected_title = ttk.Label(text_stack, text="Bitcoin", style="CardValue.TLabel")
        self.selected_title.pack(anchor="w")
        self.selected_meta = ttk.Label(text_stack, text="", style="Muted.TLabel")
        self.selected_meta.pack(anchor="w", pady=(2, 0))
        self.selected_mood = ttk.Label(text_stack, text="", style="Muted.TLabel")
        self.selected_mood.pack(anchor="w", pady=(2, 0))
        self.signal_helper = ttk.Label(self.trade_panel, text="", style="PanelTitle.TLabel")
        self.signal_helper.grid(row=2, column=0, columnspan=4, sticky="w", pady=(0, 2))
        self.signal_confidence = ttk.Label(self.trade_panel, text="", style="Muted.TLabel")
        self.signal_confidence.grid(row=3, column=0, columnspan=4, sticky="w")
        self.signal_explanation = ttk.Label(self.trade_panel, text="", style="Muted.TLabel", wraplength=290)
        self.signal_explanation.grid(row=4, column=0, columnspan=4, sticky="w", pady=(0, 10))
        ttk.Label(
            self.trade_panel,
            text="Costs: 0.5% fee plus 0.25% spread on each trade",
            style="Muted.TLabel",
        ).grid(row=5, column=0, columnspan=4, sticky="w", pady=(0, 10))
        ttk.Label(self.trade_panel, text="Amount", style="CardLabel.TLabel").grid(row=6, column=0, sticky="w", pady=(0, 4))
        self.trade_amount = tk.StringVar(value="1")
        ttk.Entry(self.trade_panel, textvariable=self.trade_amount, width=12).grid(row=7, column=0, columnspan=4, sticky="ew", pady=(0, 10))
        for col, amount in enumerate((1, 10, 100, 1000)):
            ttk.Button(self.trade_panel, text=str(amount), style="Soft.TButton", command=lambda value=amount: self.set_trade_amount(value)).grid(row=8, column=col, sticky="ew", padx=(0 if col == 0 else 5, 0))
        ttk.Button(self.trade_panel, text="BUY", style="Buy.TButton", command=self.buy_selected).grid(row=9, column=0, columnspan=2, sticky="ew", pady=(12, 0), padx=(0, 5))
        ttk.Button(self.trade_panel, text="SELL", style="Soft.TButton", command=self.sell_selected).grid(row=9, column=2, columnspan=2, sticky="ew", pady=(12, 0))
        ttk.Button(self.trade_panel, text="Buy max", style="Soft.TButton", command=self.buy_selected_max).grid(row=10, column=0, columnspan=2, sticky="ew", pady=(8, 0), padx=(0, 5))
        ttk.Button(self.trade_panel, text="Sell all", style="Soft.TButton", command=self.sell_selected_max).grid(row=10, column=2, columnspan=2, sticky="ew", pady=(8, 0))

        chart_panel = ttk.Frame(side, style="Panel.TFrame", padding=16)
        chart_panel.grid(row=1, column=0, sticky="nsew", pady=(0, 14))
        chart_panel.rowconfigure(1, weight=1)
        chart_panel.columnconfigure(0, weight=1)
        ttk.Label(chart_panel, text="Trend line", style="PanelTitle.TLabel").grid(row=0, column=0, sticky="w")
        self.chart_canvas = tk.Canvas(chart_panel, height=145, bg=self.colors["panel"], bd=0, highlightthickness=0)
        self.chart_canvas.grid(row=1, column=0, sticky="nsew", pady=(10, 0))

        history_panel = ttk.Frame(side, style="Panel.TFrame", padding=16)
        history_panel.grid(row=2, column=0, sticky="ew")
        ttk.Label(history_panel, text="Trade history", style="PanelTitle.TLabel").pack(anchor="w")
        self.history_list = tk.Listbox(history_panel, height=8, relief="flat", bd=0, highlightthickness=0, bg=self.colors["panel"], fg=self.colors["ink"], font=("Segoe UI", 8))
        self.history_list.pack(fill="x", pady=(10, 0))

    def build_summary_card(self, column, label, key):
        card = ttk.Frame(self.summary_frame, style="Panel.TFrame", padding=(10, 4))
        card.grid(row=0, column=column, sticky="ew", padx=(0 if column == 0 else 8, 0))
        ttk.Label(card, text=label.upper(), style="CardLabel.TLabel").pack(anchor="w")
        value = ttk.Label(card, text="-", style="CardValue.TLabel")
        value.pack(anchor="w")
        self.summary_labels[key] = value

    def show_game_frame(self):
        self.start_frame.pack_forget()
        self.game_frame.pack(fill="both", expand=True)
        self.update_dashboard()

    def update_dashboard(self):
        self.update_summary()
        self.update_news_ticker()
        self.update_market_tiles()
        self.update_position_tiles()
        self.update_trade_panel()
        self.update_chart()
        self.update_feed()
        self.update_trade_history()

    def update_summary(self):
        holdings = self.get_holdings_value()
        net_worth = self.cash + holdings
        total_held = self.get_total_held()
        risk_text = f"GBP {holdings:,.0f}/{self.risk_limit:,.0f}"
        rank = self.get_rank_name(net_worth)
        self.hero_net_worth.config(text=f"GBP {net_worth:,.2f}")
        self.hero_today.config(text=f"Today: {self.get_daily_net_change_text()}")
        self.day_label.config(text=f"Day {min(self.day, self.max_days)} of {self.max_days}")
        self.summary_labels["cash"].config(text=f"GBP {self.cash:,.2f}")
        self.summary_labels["holdings"].config(text=f"GBP {holdings:,.2f}")
        self.summary_labels["risk_limit"].config(text=risk_text)
        wallet_positions = self.get_wallet_positions()
        self.summary_labels["lots"].config(text=f"{len(wallet_positions)} coins")
        self.summary_labels["mood"].config(text=self.get_market_mood())
        self.summary_labels["rank"].config(text=rank)
        self.nav_rank_label.config(text=rank)
        self.nav_wallet_label.config(text=f"{len(wallet_positions)} wallet positions")
        self.nav_xp_bar["value"] = min(100, (net_worth / 50000) * 100)
        self.day_progress["value"] = min(100, (self.day / self.max_days) * 100)
        self.next_day_button.config(text=f"Next day ({self.day}/{self.max_days})")

    def update_news_ticker(self):
        if not hasattr(self, "news_ticker_label"):
            return
        if not self.news_items:
            self.news_ticker_label.config(text="No news yet. Advance a day for market headlines.")
            return
        headlines = [item["ticker"] for item in list(self.news_items)[-4:]]
        self.news_ticker_label.config(text="  |  ".join(headlines))

    def make_news_event(self, headline, target, price_impact, sentiment_impact, ticker, explanation, apply):
        return {
            "headline": headline,
            "target": target,
            "price_impact": price_impact,
            "sentiment_impact": sentiment_impact,
            "ticker": ticker,
            "explanation": explanation,
            "apply": apply,
        }

    def add_news(self, news):
        self.news_items.append(news)
        self.add_event(news["ticker"])
        self.update_news_ticker()

    def update_market_tiles(self):
        if not hasattr(self, "market_tiles_frame"):
            return
        for child in self.market_tiles_frame.winfo_children():
            child.destroy()
        self.market_tile_widgets = {}

        for index, coin in enumerate(self.coins):
            tile = self.create_coin_tile(self.market_tiles_frame, coin)
            tile.grid(row=index // 2, column=index % 2, sticky="nsew", padx=6, pady=6)
            self.market_tile_widgets[coin["name"]] = tile

    def create_coin_tile(self, parent, coin):
        signal = self.get_coin_signal_rating(coin)
        change = self.get_change_percent(coin)
        pl = (coin["price"] - coin["average_cost"]) * coin["inventory"] if coin["inventory"] else 0.0
        border_color = self.get_signal_color(signal["label"])
        tile = tk.Frame(parent, bg=self.colors["panel"], highlightbackground=border_color, highlightthickness=2, bd=0)
        tile.columnconfigure(0, weight=1)
        tile.columnconfigure(1, weight=0)

        tk.Label(tile, text=coin["name"], bg=self.colors["panel"], fg=self.colors["ink"], font=("Segoe UI", 11, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=(8, 0))
        badge = tk.Label(tile, text=signal["label"], bg=border_color, fg="#ffffff", font=("Segoe UI", 8, "bold"), padx=8, pady=2)
        badge.grid(row=0, column=1, sticky="e", padx=10, pady=(8, 0))
        move_color = self.colors["green"] if change >= 0 else self.colors["red"]
        tk.Label(tile, text=f"GBP {coin['price']:,.5f}", bg=self.colors["panel"], fg=self.colors["ink"], font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", padx=10, pady=(4, 0))
        tk.Label(tile, text=f"{change:+.2f}%", bg=self.colors["panel"], fg=move_color, font=("Segoe UI", 10, "bold")).grid(row=1, column=1, sticky="e", padx=10, pady=(4, 0))
        tk.Label(tile, text=f"Owned {self.format_amount(coin['inventory'])}", bg=self.colors["panel"], fg=self.colors["muted"], font=("Segoe UI", 9)).grid(row=2, column=0, sticky="w", padx=10, pady=(6, 8))
        pl_color = self.colors["green"] if pl >= 0 else self.colors["red"]
        tk.Label(tile, text=f"P/L GBP {pl:,.2f}", bg=self.colors["panel"], fg=pl_color, font=("Segoe UI", 9, "bold")).grid(row=2, column=1, sticky="e", padx=10, pady=(6, 8))

        for child in tile.winfo_children():
            child.bind("<Button-1>", lambda _event, name=coin["name"]: self.select_coin(name))
        tile.bind("<Button-1>", lambda _event, name=coin["name"]: self.select_coin(name))
        return tile

    def update_position_tiles(self):
        if not hasattr(self, "position_tiles_frame"):
            return
        for child in self.position_tiles_frame.winfo_children():
            child.destroy()
        self.position_tile_widgets = []

        positions = self.get_wallet_positions()
        if not positions:
            self.wallet_hint.config(text="No holdings yet. Buy a coin to populate the wallet.")
            tk.Label(
                self.position_tiles_frame,
                text="No open positions. Select a coin tile and place a trade.",
                bg=self.colors["panel"],
                fg=self.colors["muted"],
                font=("Segoe UI", 10),
            ).grid(row=0, column=0, sticky="w", padx=6, pady=8)
            return
        self.wallet_hint.config(text="Buys are combined by coin using weighted average buy price.")

        for index, position in enumerate(positions):
            coin = self.get_coin_by_name(position["coin"])
            tile = self.create_position_tile(self.position_tiles_frame, position, coin)
            tile.grid(row=index // 4, column=index % 4, sticky="nsew", padx=6, pady=4)
            self.position_tile_widgets.append(tile)

    def create_position_tile(self, parent, position, coin):
        current_price = coin["price"]
        value = position["amount"] * current_price
        pl = (current_price - position["avg_buy_price"]) * position["amount"]
        pl_color = self.colors["green"] if pl >= 0 else self.colors["red"]
        tile = tk.Frame(parent, bg=self.colors["panel_alt"], highlightbackground=self.colors["line"], highlightthickness=1, bd=0)
        tile.columnconfigure(0, weight=1)
        tk.Label(tile, text=position["coin"], bg=self.colors["panel_alt"], fg=self.colors["ink"], font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=(8, 0))
        tk.Label(tile, text=f"Amount {self.format_amount(position['amount'])}", bg=self.colors["panel_alt"], fg=self.colors["muted"], font=("Segoe UI", 8)).grid(row=1, column=0, sticky="w", padx=10)
        tk.Label(tile, text=f"Avg GBP {position['avg_buy_price']:,.5f}", bg=self.colors["panel_alt"], fg=self.colors["muted"], font=("Segoe UI", 8)).grid(row=2, column=0, sticky="w", padx=10)
        tk.Label(tile, text=f"Now GBP {current_price:,.5f}", bg=self.colors["panel_alt"], fg=self.colors["muted"], font=("Segoe UI", 8)).grid(row=3, column=0, sticky="w", padx=10)
        tk.Label(tile, text=f"P/L GBP {pl:,.2f}", bg=self.colors["panel_alt"], fg=pl_color, font=("Segoe UI", 9, "bold")).grid(row=4, column=0, sticky="w", padx=10, pady=(2, 0))
        tk.Label(tile, text=f"Held {position['held_days']}", bg=self.colors["panel_alt"], fg=self.colors["muted"], font=("Segoe UI", 8)).grid(row=5, column=0, sticky="w", padx=10)
        tk.Button(tile, text="Sell 25%", command=lambda name=coin["name"], amount=position["amount"] * 0.25: self.sell_coin(self.get_coin_index(name), amount), bg="#ffffff", fg=self.colors["ink"], relief="flat").grid(row=6, column=0, sticky="ew", padx=8, pady=(6, 2))
        tk.Button(tile, text="Sell all", command=lambda name=coin["name"]: self.sell_max(self.get_coin_index(name)), bg="#ffffff", fg=self.colors["ink"], relief="flat").grid(row=7, column=0, sticky="ew", padx=8, pady=(0, 8))
        return tile

    def update_trade_panel(self):
        coin = self.get_selected_coin()
        change = self.get_change_percent(coin)
        signal = self.get_coin_signal_rating(coin)
        self.selected_title.config(text=coin["name"])
        self.selected_meta.config(
            text=f"Price GBP {coin['price']:,.5f} | Move {change:+.2f}% | Owned {self.format_amount(coin['inventory'])}"
        )
        self.selected_mood.config(
            text=f"{coin['sector']} | Momentum {coin['momentum'] * 100:+.2f}% | Sentiment {coin['sentiment'] * 100:+.2f}%"
        )
        self.signal_helper.config(text=f"{signal['label']} - {signal['helper']}")
        self.signal_confidence.config(text=f"Confidence: {signal['confidence']}%")
        self.signal_explanation.config(text=signal["explanation"])
        self.draw_coin_badge(coin)

    def draw_coin_badge(self, coin):
        canvas = self.coin_badge
        canvas.delete("all")
        color = self.get_coin_color(coin["name"])
        initials = "".join(part[0] for part in coin["name"].split()[:2]).upper()
        canvas.create_oval(5, 5, 49, 49, fill=color, outline="#ffffff", width=3)
        canvas.create_oval(10, 10, 44, 44, outline="#ffffff", width=1)
        canvas.create_text(27, 27, text=initials, fill="#ffffff", font=("Segoe UI", 13, "bold"))

    def get_coin_color(self, name):
        colors = {
            "Bitcoin": "#f59e0b",
            "Ethereum": "#6366f1",
            "Binance Coin": "#eab308",
            "Polkadot": "#ec4899",
            "Cardano": "#2563eb",
            "Dogecoin": "#ca8a04",
            "Monero": "#f97316",
            "Chainlink": "#0ea5e9",
        }
        return colors.get(name, self.colors["accent"])

    def get_signal_color(self, label):
        colors = {
            "Good Buy": self.colors["green"],
            "Wait": self.colors["amber"],
            "Risky": "#f97316",
            "Bad Buy": self.colors["red"],
        }
        return colors.get(label, self.colors["muted"])

    def get_coin_signal_rating(self, coin):
        change = self.get_change_percent(coin)
        rumour_volatility, rumour_sentiment = self.get_coin_signal(coin)
        momentum_score = coin["momentum"] * 220
        sentiment_score = (coin["sentiment"] + rumour_sentiment) * 260
        move_score = max(-18, min(18, change * 1.8))
        volatility_penalty = (coin["volatility"] + rumour_volatility) * 90
        trend_heat_penalty = max(0, (coin["price"] / coin["initial_price"] - 1.45) * 28)
        crash_value_bonus = max(0, (0.82 - coin["price"] / coin["initial_price"]) * 18)
        score = 50 + momentum_score + sentiment_score + move_score + crash_value_bonus - volatility_penalty - trend_heat_penalty
        score = max(0, min(100, int(round(score))))

        if score >= 68:
            label = "Good Buy"
            helper = "momentum and mood are lining up"
            explanation = "Positive pressure is stronger than the risk penalty, so this coin has a cleaner setup today."
        elif score >= 46:
            label = "Wait"
            helper = "setup is mixed"
            explanation = "The signal is balanced. Watch the next headline or price move before adding more exposure."
        elif score >= 28:
            label = "Risky"
            helper = "volatility is elevated"
            explanation = "There may be upside, but volatility, heat, or weak sentiment makes the trade harder to time."
        else:
            label = "Bad Buy"
            helper = "pressure is negative"
            explanation = "Momentum and sentiment are working against this coin, so buying now has a poor risk profile."

        if rumour_volatility or rumour_sentiment:
            explanation += " Active rumours are also adding uncertainty."

        return {
            "label": label,
            "helper": helper,
            "confidence": score,
            "explanation": explanation,
        }

    def update_chart(self):
        coin = self.get_selected_coin()
        values = list(coin["price_history"])
        canvas = self.chart_canvas
        canvas.delete("all")
        width = max(canvas.winfo_width(), 300)
        height = max(canvas.winfo_height(), 140)
        pad = 16

        canvas.create_rectangle(0, 0, width, height, fill=self.colors["panel"], outline="")
        canvas.create_rectangle(0, 0, width, height, fill="#f8fbff", outline="")
        if len(values) < 2:
            canvas.create_text(width / 2, height / 2, text="Advance a day to draw the pulse", fill=self.colors["muted"], font=("Segoe UI", 10))
            return

        min_v = min(values)
        max_v = max(values)
        spread = max(max_v - min_v, max_v * 0.01)
        points = []
        for i, value in enumerate(values):
            x = pad + (width - pad * 2) * (i / max(1, len(values) - 1))
            y = height - pad - ((value - min_v) / spread) * (height - pad * 2)
            points.append((x, y))

        for y_frac in (0.25, 0.5, 0.75):
            y = pad + (height - pad * 2) * y_frac
            canvas.create_line(pad, y, width - pad, y, fill=self.colors["line"])

        line_color = self.colors["green"] if values[-1] >= values[0] else self.colors["red"]
        for start, end in zip(points, points[1:]):
            canvas.create_line(*start, *end, fill=line_color, width=3, smooth=True)
        canvas.create_oval(points[-1][0] - 4, points[-1][1] - 4, points[-1][0] + 4, points[-1][1] + 4, fill=line_color, outline="")
        canvas.create_text(pad, pad, text=f"Low GBP {min_v:,.4f}", fill=self.colors["muted"], anchor="nw", font=("Segoe UI", 8))
        canvas.create_text(width - pad, pad, text=f"High GBP {max_v:,.4f}", fill=self.colors["muted"], anchor="ne", font=("Segoe UI", 8))

    def update_feed(self):
        return

    def update_trade_history(self):
        if not hasattr(self, "history_list"):
            return
        self.history_list.delete(0, "end")
        if not self.trade_history:
            self.history_list.insert("end", "No trades yet.")
            return
        for trade in reversed(self.trade_history):
            pnl = ""
            if trade["action"] == "SELL":
                pnl = f" | P/L GBP {trade['profit']:,.2f}"
            self.history_list.insert(
                "end",
                f"Day {trade['day']} | {trade['action']} | {trade['coin']} | {self.format_amount(trade['amount'])} @ GBP {trade['price']:,.5f}{pnl}",
            )

    def add_event(self, text):
        self.event_feed.append(f"Day {min(self.day, self.max_days)}: {text}")

    def select_coin(self, name):
        self.selected_coin_name = name
        self.update_market_tiles()
        self.update_trade_panel()
        self.update_chart()

    def on_coin_selected(self, _event=None):
        return

    def focus_dashboard(self):
        self.hero_net_worth.focus_set()

    def focus_market(self):
        self.market_tiles_frame.focus_set()

    def focus_wallet(self):
        self.position_tiles_frame.focus_set()

    def focus_trade_history(self):
        self.history_list.focus_set()

    def show_achievements(self):
        positions = len(self.get_wallet_positions())
        net_worth = self.cash + self.get_holdings_value()
        achievements = [
            ("First Trade", bool(self.trade_history), "Make any buy or sell."),
            ("Diversifier", positions >= 3, "Hold 3 different coins."),
            ("Broker", net_worth >= 10000, "Reach GBP 10,000 net worth."),
            ("Market Maker", net_worth >= 25000, "Reach GBP 25,000 net worth."),
            ("Whale", net_worth >= 50000, "Reach GBP 50,000 net worth."),
        ]
        lines = []
        for name, complete, description in achievements:
            state = "Done" if complete else "Open"
            lines.append(f"{state}: {name} - {description}")
        messagebox.showinfo("Achievements", "\n".join(lines))

    def show_guide(self):
        messagebox.showinfo(
            "How To Play",
            "Pick coins from Market Watch, choose an amount, then Buy or Sell.\n\n"
            "Momentum means recent price movement is carrying forward.\n\n"
            "Sentiment is hidden market mood affecting that coin.\n\n"
            "Rumours are weak signals. They can raise volatility or sentiment for a few days before a move.\n\n"
            "Risk limit is based on portfolio value, not coin units.\n\n"
            "Every trade pays a 0.5% fee and crosses a 0.25% spread, so overtrading has a cost.",
        )

    def set_trade_amount(self, amount):
        self.trade_amount.set(str(amount))

    # ======================
    #  Game Logic
    # ======================
    def buy_selected(self):
        amount = self.get_trade_amount()
        if amount is not None:
            self.buy_coin(self.get_coin_index(self.selected_coin_name), amount)

    def sell_selected(self):
        amount = self.get_trade_amount()
        if amount is not None:
            self.sell_coin(self.get_coin_index(self.selected_coin_name), amount)

    def buy_selected_max(self):
        self.buy_max(self.get_coin_index(self.selected_coin_name))

    def sell_selected_max(self):
        self.sell_max(self.get_coin_index(self.selected_coin_name))

    def get_trade_amount(self):
        try:
            amount = float(self.trade_amount.get())
        except ValueError:
            self.show_notice("Enter a valid amount.")
            return None
        if amount <= 0:
            self.show_notice("Amount must be positive.")
            return None
        return amount

    def buy_coin(self, index, amount):
        if self.game_over:
            return
        coin = self.coins[index]
        execution_price = coin["price"] * (1 + self.spread_rate)
        gross_cost = execution_price * amount
        fee = gross_cost * self.transaction_fee_rate
        total_cost = gross_cost + fee
        new_value = self.get_holdings_value() + gross_cost

        if total_cost > self.cash:
            self.show_notice("Not enough cash for that buy.")
            return
        if new_value > self.risk_limit:
            self.show_notice("That buy exceeds your Risk Limit.")
            return

        self.cash -= total_cost
        self.wallet_lots.append({
            "id": self.next_lot_id,
            "coin": coin["name"],
            "day": min(self.day, self.max_days),
            "amount_bought": amount,
            "amount_remaining": amount,
            "buy_price": execution_price,
            "cost": gross_cost,
            "fee": fee,
        })
        self.next_lot_id += 1
        self.sync_coin_from_lots(coin)
        self.log_trade("BUY", coin, amount, execution_price, total_cost, -fee)
        self.add_event(f"Bought {self.format_amount(amount)} {coin['name']} for GBP {total_cost:,.2f} including fees.")
        self.update_dashboard()

    def sell_coin(self, index, amount):
        if self.game_over:
            return
        coin = self.coins[index]
        if coin["inventory"] < amount:
            self.show_notice("Not enough inventory to sell.")
            return

        execution_price = coin["price"] * (1 - self.spread_rate)
        gross_revenue = execution_price * amount
        fee = gross_revenue * self.transaction_fee_rate
        revenue = gross_revenue - fee
        cost_basis = coin["average_cost"] * amount
        trade_profit = revenue - cost_basis
        self.total_trades += 1
        self.best_trade = max(self.best_trade, trade_profit)
        self.worst_trade = min(self.worst_trade, trade_profit)
        self.consume_wallet_lots(coin["name"], amount)
        self.sync_coin_from_lots(coin)
        self.cash += revenue
        self.log_trade("SELL", coin, amount, execution_price, revenue, trade_profit)
        result = "profit" if trade_profit >= 0 else "loss"
        self.add_event(f"Sold {self.format_amount(amount)} {coin['name']} for GBP {revenue:,.2f} after fees ({result} GBP {trade_profit:,.2f}).")
        self.update_dashboard()

    def buy_max(self, index):
        if self.game_over:
            return
        coin = self.coins[index]
        risk_limit_left = max(0.0, self.risk_limit - self.get_holdings_value())
        execution_price = coin["price"] * (1 + self.spread_rate)
        cash_limited_amount = self.cash / (execution_price * (1 + self.transaction_fee_rate))
        risk_limited_amount = risk_limit_left / execution_price
        amount_to_buy = min(cash_limited_amount, risk_limited_amount)
        amount_to_buy = math.floor(amount_to_buy * 100000000) / 100000000
        if amount_to_buy <= 0:
            self.show_notice("Cannot buy any more of this coin.")
            return
        self.buy_coin(index, amount_to_buy)

    def sell_max(self, index):
        if self.game_over:
            return
        coin = self.coins[index]
        if coin["inventory"] <= 0:
            self.show_notice("No inventory to sell.")
            return
        self.sell_coin(index, coin["inventory"])

    def next_day(self):
        if self.game_over:
            return

        self.day += 1
        daily_drift = 0.003
        movers = []

        for coin in self.coins:
            coin["previous_price"] = coin["price"]
            volatility_bonus, sentiment_bias = self.get_coin_signal(coin)
            shock = random.gauss(0, (coin["volatility"] + volatility_bonus) * 0.42)
            trend = coin["momentum"] * 0.32
            sentiment = (coin["sentiment"] + sentiment_bias) * 0.26
            price_ratio = coin["price"] / coin["initial_price"]
            mean_reversion = -0.012 * (price_ratio - 1)
            total_change = daily_drift + shock + trend + sentiment + mean_reversion
            max_daily_move = coin["volatility"] * 1.85
            total_change = max(-max_daily_move, min(max_daily_move, total_change))
            if coin["price"] < 0.5 * coin["initial_price"] and total_change < 0:
                total_change /= 2.0
            coin["price"] = max(0.00001, coin["price"] * (1 + total_change))
            coin["momentum"] = coin["momentum"] * 0.62 + total_change * 0.38
            coin["sentiment"] *= 0.82
            coin["price_history"].append(coin["price"])
            movers.append((abs(total_change), coin["name"], total_change))

        self.check_market_recovery()
        self.age_rumours()

        biggest = max(movers, key=lambda item: item[0])
        self.add_news({
            "headline": f"{biggest[1]} led the overnight move",
            "target": biggest[1],
            "price_impact": biggest[2],
            "sentiment_impact": 0.0,
            "ticker": f"{biggest[1]} moved {biggest[2] * 100:+.2f}% overnight.",
            "explanation": "Daily movement came from drift, volatility, momentum, sentiment, rumours, and mean reversion.",
        })

        if random.random() < self.market_event_chance:
            self.trigger_market_event()
        if random.random() < self.rumour_chance:
            self.seed_rumour()

        if self.day > self.max_days:
            self.end_game()
        else:
            self.update_dashboard()

    def check_market_recovery(self):
        avg_init = sum(c["initial_price"] for c in self.coins) / len(self.coins)
        avg_current = sum(c["price"] for c in self.coins) / len(self.coins)
        if avg_current < 0.4 * avg_init:
            for coin in self.coins:
                coin["price"] *= 1.30
            self.add_news({
                "headline": "Relief rally: the whole market bounced 30%",
                "target": "Market",
                "price_impact": 0.30,
                "sentiment_impact": 0.07,
                "ticker": "Relief rally: the whole market bounced 30%.",
                "explanation": "Prices had fallen too far below their starting levels, so the market staged a broad recovery.",
            })

    def trigger_market_event(self):
        events = [
            self.make_news_event("Bull Run! All coins gain 30%", "Market", 0.30, 0.09, "Market-wide bull run lifts every coin.", "All coins surged as risk appetite returned.", lambda: self.apply_all(1.30)),
            self.make_news_event("Bear Market! All coins drop 30%", "Market", -0.30, -0.09, "Bear market shock hits every coin.", "The whole market sold off as traders reduced exposure.", lambda: self.apply_all(0.70)),
            self.make_news_event("Exchange Hack! All prices drop 20%", "Market", -0.20, -0.08, "Exchange hack knocks confidence across crypto.", "Security fears pressured every coin at once.", lambda: self.apply_all(0.80)),
            self.make_news_event("Regulation! Big coins drop 15%", "Large-cap coins", -0.15, -0.06, "Regulatory pressure hits higher-priced coins.", "Bigger coins sold off while smaller coins were less affected.", self.regulation_event),
            self.make_news_event("Institutional bid! Majors gain 12%", "Majors", 0.12, 0.05, "Institutions bid up Bitcoin and Ethereum.", "Major coins gained as bigger money stepped in.", lambda: self.apply_sector("Majors", 1.12)),
            self.make_news_event("Infrastructure outage! Infrastructure coins drop 14%", "Infrastructure", -0.14, -0.05, "Infrastructure outage pressures DOT, ADA, and LINK.", "Network reliability concerns hit infrastructure names.", lambda: self.apply_sector("Infrastructure", 0.86)),
            self.make_news_event("Privacy demand jumps! Privacy coins gain 16%", "Privacy", 0.16, 0.06, "Privacy demand lifts Monero.", "Demand for private transactions improved sentiment.", lambda: self.apply_sector("Privacy", 1.16)),
            self.make_news_event("Exchange volume boom! Exchange coins gain 13%", "Exchange", 0.13, 0.05, "Trading volume boom lifts exchange tokens.", "Higher activity helped exchange-linked assets.", lambda: self.apply_sector("Exchange", 1.13)),
            self.make_news_event("Meme hype fades! Meme coins drop 18%", "Meme", -0.18, -0.07, "Meme hype fades and DOGE sells off.", "Speculative appetite cooled quickly.", lambda: self.apply_sector("Meme", 0.82)),
            self.make_news_event("Bitcoin Adoption! Bitcoin up 5%", "Bitcoin", 0.05, 0.03, "Bitcoin adoption headline boosts BTC.", "Adoption news added mild positive pressure.", lambda: self.apply_named("bitcoin", 1.05)),
            self.make_news_event("Bitcoin Crash! Bitcoin down 5%", "Bitcoin", -0.05, -0.03, "Bitcoin crash headline weighs on BTC.", "Bitcoin slipped as short-term holders took risk off.", lambda: self.apply_named("bitcoin", 0.95)),
            self.make_news_event("Ethereum Scaling Success! Ethereum up 10%", "Ethereum", 0.10, 0.04, "Ethereum scaling success boosts ETH.", "Scaling optimism improved sentiment.", lambda: self.apply_named("ethereum", 1.10)),
            self.make_news_event("Ethereum Bug Found! Ethereum down 10%", "Ethereum", -0.10, -0.05, "Ethereum bug report pressures ETH.", "Technical concerns cooled Ethereum demand.", lambda: self.apply_named("ethereum", 0.90)),
            self.make_news_event("Binance Good News! BNB up 25%", "Binance Coin", 0.25, 0.08, "Exchange headline sends BNB higher.", "Positive exchange news boosted confidence in Binance Coin.", lambda: self.apply_named("binance coin", 1.25)),
            self.make_news_event("Binance FUD! BNB down 25%", "Binance Coin", -0.25, -0.08, "Exchange fears hit BNB.", "Uncertainty around exchange activity triggered a fast selloff.", lambda: self.apply_named("binance coin", 0.75)),
            self.make_news_event("Polkadot Partnerships! Polkadot up 20%", "Polkadot", 0.20, 0.07, "Polkadot partnership chatter lifts DOT.", "Infrastructure optimism pulled buyers into Polkadot.", lambda: self.apply_named("polkadot", 1.20)),
            self.make_news_event("Polkadot Partnerships Fail! Polkadot down 20%", "Polkadot", -0.20, -0.07, "Polkadot partnership hopes fade.", "A failed partnership story weakened DOT sentiment.", lambda: self.apply_named("polkadot", 0.80)),
            self.make_news_event("Cardano Hard Fork! Cardano up 15%", "Cardano", 0.15, 0.06, "Cardano hard fork optimism lifts ADA.", "Upgrade optimism helped Cardano catch a bid.", lambda: self.apply_named("cardano", 1.15)),
            self.make_news_event("Cardano Hard Fork Bug! Cardano down 15%", "Cardano", -0.15, -0.06, "Cardano fork bug knocks ADA.", "Upgrade risk pressured Cardano after the bug report.", lambda: self.apply_named("cardano", 0.85)),
            self.make_news_event("Elon Tweet! Dogecoin soars 50%", "Dogecoin", 0.50, 0.12, "Celebrity hype sends DOGE vertical.", "Meme demand spiked fast, but the setup is extremely volatile.", lambda: self.apply_named("dogecoin", 1.50)),
            self.make_news_event("Dogecoin Dump! Dogecoin down 40%", "Dogecoin", -0.40, -0.12, "Dogecoin hype snaps back hard.", "Meme speculation unwound rapidly.", lambda: self.apply_named("dogecoin", 0.60)),
            self.make_news_event("Monero Privacy Boost! Monero up 10%", "Monero", 0.10, 0.05, "Privacy demand boosts Monero.", "Demand for private transfers lifted XMR sentiment.", lambda: self.apply_named("monero", 1.10)),
            self.make_news_event("Monero Privacy Crackdown! Monero down 10%", "Monero", -0.10, -0.05, "Privacy crackdown pressures Monero.", "Regulatory attention reduced appetite for privacy coins.", lambda: self.apply_named("monero", 0.90)),
            self.make_news_event("Chainlink Integration! Chainlink up 25%", "Chainlink", 0.25, 0.08, "New integration lifts Chainlink.", "Oracle adoption news improved Chainlink momentum.", lambda: self.apply_named("chainlink", 1.25)),
            self.make_news_event("Chainlink Rejection! Chainlink down 25%", "Chainlink", -0.25, -0.08, "Integration rejection hits Chainlink.", "A rejected integration cooled LINK demand.", lambda: self.apply_named("chainlink", 0.75)),
        ]
        event = random.choice(events)
        event["apply"]()
        event.pop("apply")
        self.add_news(event)

    def apply_all(self, factor):
        for coin in self.coins:
            coin["price"] *= factor
            self.adjust_coin_pressure(coin, factor - 1)
            coin["price_history"].append(coin["price"])

    def apply_named(self, name, factor):
        for coin in self.coins:
            if coin["name"].lower() == name:
                coin["price"] *= factor
                self.adjust_coin_pressure(coin, factor - 1)
                coin["price_history"].append(coin["price"])

    def apply_sector(self, sector, factor):
        for coin in self.coins:
            if coin["sector"] == sector:
                coin["price"] *= factor
                self.adjust_coin_pressure(coin, factor - 1)
                coin["price_history"].append(coin["price"])

    def regulation_event(self):
        for coin in self.coins:
            if coin["price"] > 100:
                coin["price"] *= 0.85
                self.adjust_coin_pressure(coin, -0.15)
                coin["price_history"].append(coin["price"])

    def adjust_coin_pressure(self, coin, event_change):
        coin["sentiment"] = max(-0.22, min(0.22, coin["sentiment"] + event_change * 0.35))
        coin["momentum"] = max(-0.16, min(0.16, coin["momentum"] + event_change * 0.18))

    def get_coin_signal(self, coin):
        volatility_bonus = 0.0
        sentiment_bias = 0.0
        for rumour in self.active_rumours:
            if rumour.get("coin") == coin["name"] or rumour.get("sector") == coin["sector"]:
                volatility_bonus += rumour["volatility_bonus"]
                sentiment_bias += rumour["sentiment_bias"]
        return volatility_bonus, sentiment_bias

    def age_rumours(self):
        for rumour in self.active_rumours:
            rumour["days_left"] -= 1
        self.active_rumours = [rumour for rumour in self.active_rumours if rumour["days_left"] > 0]

    def seed_rumour(self):
        templates = [
            {
                "label": "Rumour: Ethereum developers hint at scaling news.",
                "coin": "Ethereum",
                "sector": None,
                "strength": "Medium",
                "volatility_bonus": 0.025,
                "sentiment_bias": 0.018,
            },
            {
                "label": "Rumour: institutional desks are watching majors.",
                "coin": None,
                "sector": "Majors",
                "strength": "Low",
                "volatility_bonus": 0.014,
                "sentiment_bias": 0.012,
            },
            {
                "label": "Rumour: infrastructure partnerships may land soon.",
                "coin": None,
                "sector": "Infrastructure",
                "strength": "Medium",
                "volatility_bonus": 0.026,
                "sentiment_bias": 0.014,
            },
            {
                "label": "Rumour: exchange regulators are circling.",
                "coin": None,
                "sector": "Exchange",
                "strength": "High",
                "volatility_bonus": 0.034,
                "sentiment_bias": -0.018,
            },
            {
                "label": "Rumour: celebrity chatter is building around memes.",
                "coin": None,
                "sector": "Meme",
                "strength": "High",
                "volatility_bonus": 0.05,
                "sentiment_bias": 0.02,
            },
            {
                "label": "Rumour: privacy coins face possible delistings.",
                "coin": None,
                "sector": "Privacy",
                "strength": "Medium",
                "volatility_bonus": 0.028,
                "sentiment_bias": -0.014,
            },
        ]
        rumour = random.choice(templates).copy()
        rumour["days_left"] = 3
        self.active_rumours.append(rumour)
        self.add_news({
            "headline": rumour["label"],
            "target": rumour["coin"] or rumour["sector"],
            "price_impact": 0.0,
            "sentiment_impact": rumour["sentiment_bias"],
            "ticker": f"{rumour['label']} Strength: {rumour['strength']}.",
            "explanation": "Rumours are weak signals. They raise volatility and sentiment pressure for 3 days.",
        })

    def sort_by_price(self):
        self.sort_reverse = not self.sort_reverse
        self.coins.sort(key=lambda x: x["price"], reverse=self.sort_reverse)
        self.update_dashboard()

    def end_game(self):
        if self.game_over:
            return
        self.game_over = True
        total_coin_value = self.get_holdings_value()
        final_net_worth = self.cash + total_coin_value

        msg = (
            "Game over!\n\n"
            f"Final Day: {min(self.day, self.max_days)}\n"
            f"Final Cash: GBP {self.cash:,.2f}\n"
            f"Value of Coins: GBP {total_coin_value:,.2f}\n"
            f"Final Net Worth: GBP {final_net_worth:,.2f}\n\n"
            f"Total Trades: {self.total_trades}\n"
            f"Best Trade: GBP {self.best_trade:,.2f}\n"
            f"Worst Trade: GBP {self.worst_trade:,.2f}\n"
        )
        messagebox.showinfo("Results", msg)
        name = sd.askstring("High Score", "Enter your name for the high score table:")
        if name:
            self.save_high_score(name, final_net_worth, self.best_trade, self.worst_trade)
        self.show_start_frame()

    # ======================
    #  Helpers
    # ======================
    def get_selected_coin(self):
        for coin in self.coins:
            if coin["name"] == self.selected_coin_name:
                return coin
        return self.coins[0]

    def get_coin_by_name(self, name):
        for coin in self.coins:
            if coin["name"] == name:
                return coin
        return self.coins[0]

    def get_coin_index(self, name):
        for index, coin in enumerate(self.coins):
            if coin["name"] == name:
                return index
        return 0

    def get_change_percent(self, coin):
        if coin["previous_price"] == 0:
            return 0
        return ((coin["price"] - coin["previous_price"]) / coin["previous_price"]) * 100

    def get_daily_net_change_text(self):
        daily_change = 0.0
        for coin in self.coins:
            daily_change += (coin["price"] - coin["previous_price"]) * coin["inventory"]
        sign = "+" if daily_change >= 0 else "-"
        return f"{sign}GBP {abs(daily_change):,.2f}"

    def get_market_mood(self):
        if not self.coins:
            return "Neutral"
        pressure = sum(coin["momentum"] + coin["sentiment"] for coin in self.coins) / len(self.coins)
        if pressure > 0.045:
            return "Euphoric"
        if pressure > 0.015:
            return "Bullish"
        if pressure < -0.045:
            return "Panic"
        if pressure < -0.015:
            return "Bearish"
        return "Neutral"

    def get_holdings_value(self):
        return sum(coin["price"] * coin["inventory"] for coin in self.coins)

    def get_total_held(self):
        return sum(coin["inventory"] for coin in self.coins)

    def sync_coin_from_lots(self, coin):
        lots = [lot for lot in self.get_open_lots() if lot["coin"] == coin["name"]]
        inventory = sum(lot["amount_remaining"] for lot in lots)
        total_cost = sum(lot["amount_remaining"] * lot["buy_price"] for lot in lots)
        coin["inventory"] = inventory
        coin["average_cost"] = total_cost / inventory if inventory else 0.0

    def sync_all_coins_from_lots(self):
        for coin in self.coins:
            self.sync_coin_from_lots(coin)

    def get_open_lots(self):
        return [lot for lot in self.wallet_lots if lot["amount_remaining"] > 0.000001]

    def get_wallet_positions(self):
        grouped = {}
        for lot in self.get_open_lots():
            data = grouped.setdefault(lot["coin"], {
                "coin": lot["coin"],
                "amount": 0.0,
                "cost": 0.0,
                "days": [],
                "oldest_day": lot["day"],
            })
            amount = lot["amount_remaining"]
            data["amount"] += amount
            data["cost"] += amount * lot["buy_price"]
            data["days"].append(lot["day"])
            data["oldest_day"] = min(data["oldest_day"], lot["day"])

        positions = []
        for data in grouped.values():
            days = sorted(set(data["days"]))
            if len(days) == 1:
                day_label = f"Day {days[0]}"
            else:
                day_label = f"Days {days[0]}-{days[-1]}"
            held_days = max(1, self.day - data["oldest_day"] + 1)
            positions.append({
                "coin": data["coin"],
                "amount": data["amount"],
                "avg_buy_price": data["cost"] / data["amount"] if data["amount"] else 0.0,
                "day_label": day_label,
                "held_days": f"{held_days} day" if held_days == 1 else f"{held_days} days",
            })
        return sorted(positions, key=lambda item: item["coin"])

    def consume_wallet_lots(self, coin_name, amount):
        amount_left = amount
        for lot in self.wallet_lots:
            if lot["coin"] != coin_name or lot["amount_remaining"] <= 0:
                continue
            taken = min(lot["amount_remaining"], amount_left)
            lot["amount_remaining"] -= taken
            amount_left -= taken
            if amount_left <= 0.000001:
                break

    def log_trade(self, action, coin, amount, price, value, profit):
        self.trade_history.append({
            "day": min(self.day, self.max_days),
            "action": action,
            "coin": coin["name"],
            "amount": amount,
            "price": price,
            "value": value,
            "profit": profit,
        })

    def get_rank_name(self, net_worth):
        if net_worth >= 50000:
            return "Whale"
        if net_worth >= 25000:
            return "Market Maker"
        if net_worth >= 10000:
            return "Broker"
        if net_worth >= 2500:
            return "Trader"
        return "Rookie"

    def show_notice(self, text):
        self.add_event(text)
        self.update_feed()

    def format_amount(self, amount):
        if abs(amount) >= 100:
            return f"{amount:,.2f}"
        if abs(amount) >= 1:
            return f"{amount:,.4f}".rstrip("0").rstrip(".")
        return f"{amount:,.8f}".rstrip("0").rstrip(".")

    # ======================
    #  High Score Logic
    # ======================
    def get_data_path(self, filename):
        appdata = os.environ.get("APPDATA")
        if appdata:
            base_dir = os.path.join(appdata, "Crypto Trader")
            try:
                os.makedirs(base_dir, exist_ok=True)
                return os.path.join(base_dir, filename)
            except OSError:
                pass
        if getattr(sys, "frozen", False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_dir, filename)

    def load_high_scores(self):
        if os.path.exists(self.high_score_file):
            try:
                with open(self.high_score_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                return []
        return []

    def load_and_show_high_scores(self):
        self.show_high_scores(self.load_high_scores())

    def save_high_score(self, name, net_worth, best_trade, worst_trade):
        scores = self.load_high_scores()
        return_percent = ((net_worth - self.starting_cash) / self.starting_cash) * 100
        scores.append({
            "name": name,
            "net_worth": net_worth,
            "best_trade": best_trade,
            "worst_trade": worst_trade,
            "difficulty": self.difficulty_var.get(),
            "days": self.max_days,
            "starting_cash": self.starting_cash,
            "return_percent": return_percent,
        })
        scores.sort(key=lambda s: s.get("return_percent", -999999), reverse=True)
        scores = scores[:10]
        with open(self.high_score_file, "w", encoding="utf-8") as f:
            json.dump(scores, f, indent=2)
        self.show_high_scores(scores)

    def show_high_scores(self, scores):
        window = tk.Toplevel(self.root)
        window.title("High Scores")
        window.configure(bg=self.colors["bg"])
        window.geometry("520x360")
        panel = ttk.Frame(window, style="Panel.TFrame", padding=18)
        panel.pack(fill="both", expand=True, padx=16, pady=16)
        ttk.Label(panel, text="Hall of fame", style="PanelTitle.TLabel").pack(anchor="w")

        if not scores:
            ttk.Label(panel, text="No high scores yet.", style="Body.TLabel").pack(anchor="w", pady=18)
            return

        table = ttk.Treeview(panel, columns=("return", "mode", "net"), show="tree headings", height=10)
        table.heading("#0", text="Player")
        table.heading("return", text="Return")
        table.heading("mode", text="Mode")
        table.heading("net", text="Net worth")
        table.column("#0", width=140, anchor="w")
        table.column("return", width=90, anchor="e")
        table.column("mode", width=120, anchor="center")
        table.column("net", width=130, anchor="e")
        table.pack(fill="both", expand=True, pady=(12, 0))
        for index, entry in enumerate(scores, start=1):
            table.insert(
                "",
                "end",
                text=f"{index}. {entry['name']}",
                values=(
                    f"{entry.get('return_percent', 0):+.1f}%" if "return_percent" in entry else "Legacy",
                    f"{entry.get('difficulty', 'Legacy')} / {entry.get('days', '-')}",
                    f"GBP {entry['net_worth']:,.2f}",
                ),
            )


def main():
    root = tk.Tk()
    CryptoTraderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
