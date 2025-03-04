import tkinter as tk
from tkinter import messagebox
import random
import sys
import os
import pygame
import json
import time

# Initialize pygame mixer
pygame.mixer.init()

# Get correct path whether running as script or .exe
if getattr(sys, 'frozen', False):
    game_folder = sys._MEIPASS  # PyInstaller folder
else:
    game_folder = os.path.dirname(__file__)

SAVE_FILE = "cards_save.json"

# List of quiz questions and answers
QUIZ_QUESTIONS = [
    ("GPT steht für Generative Pretrained Transformer.", True),
    ("AGI steht für Alternative Generative Intelligence.", False),
    ("AGI steht für Artificial General Intelligence.", True),
    ("Deep Fakes sind immer unzulässig.", False),
    ("Maschinelles Lernen ist ein Teilbereich der KI.", True),
    ("Großen Sprachmodelle (LLMs) wie ChatGPT werden als Foundation Models bezeichnet.", True),
    ("Neuronale Netze sind vom menschlichen Gehirn inspiriert.", True),
    ("Chatbots verstehen menschliche Emotionen immer perfekt.", False),
    ("Für das Training von KI-Modellen sind große Datenmengen erforderlich.", True),
    ("AGI ist ein Synonym für Machine Learning.", False),
    ("Robotik und KI sind dasselbe.", False),
    ("KIs können aus ihren Fehlern lernen.", True),
    ("KI-generierte Inhalte sind immer korrekt.", False),
    ("Computer Vision ist ein Teilbereich der KI.", True),
    ("KI kann keine strategischen Spiele wie Schach spielen.", False),
    ("KI hilft bei der Automatisierung wiederkehrender Aufgaben.", True),
    ("Ein KI-Manager ist nur für die technische Umsetzung von KI-Projekten verantwortlich.", False),
    ("KI kann bei der Diagnose von Krankheiten helfen.", True),
    ("KI benötigt immer eine Internetverbindung, um zu funktionieren.", False),
    ("KI-geschriebener Code ist immer fehlerfrei.", False),
    ("KI kann Bilder und Videos analysieren.", True),
    ("Selbstfahrende Autos nutzen KI-Technologie.", True),
    ("KI kann Wettermuster vorhersagen.", True),
    ("Sie können KI-Tools für Ihre Arbeit nutzen, wenn der Arbeitgeber es nicht verbietet.", True),
    ("Ein Prompt ist immer urheberrechtlich geschützt.", False),
    ("Ein von Ihnen mit einem KI-Tool generiertes Bild ist urheberrechtlich geschützt.", False),
    ("Wenn ich den AGBs eines KI-Tools zustimme, werden sie Vertragsbestandteil.", True),
    ("Wenn ein KI-Bild falsche Informationen enthält, ist die Nutzung des Bildes unzulässig.", False),
    ("Ein Prompt sollte nie Geschäftsgeheimnisse enthalten.", True),
    ("KPI steht für Key Performance Indicator", True),
    ("KI-Tools können ohne Offenlegung genutzt werden, sofern sie die Produktivität steigern.", False),
    ("Zu den Aufgaben eines KI-Managers gehört es, Mitarbeiter im Umgang mit KI zu schulen.", True),
    ("KI-generierte Berichte spiegeln immer unvoreingenommene, sachliche Informationen wider.", False),
    ("KI-Manager sollten KI-Modelle regelmäßig auf Leistung und Fairness bewerten.", True),
    ("Sie können Kundendaten ohne Zustimmung frei mit KI-Tools von Drittanbietern teilen.", False),
    ("KI-gesteuerte Entscheidungen sollten stets erklärbar und transparent sein.", True),
    ("Es ist wichtig, Richtlinien für den ethischen Einsatz von KI-Tools festzulegen.", True),
    ("Der KI-Reifegrad eines Unternehmens ist irrelevant für die Strategieentwicklung.", False),
    ("KI-Manager sollten die Umweltauswirkungen großer KI-Modelle überwachen.", True),
    ("Einmal eingesetzt, erfordern KI-Systeme keine weitere menschliche Aufsicht.", False),
    ("KI-Manager sind dafür verantwortlich, algorithmische Verzerrungen abzumildern.", True),
    ("KI-Tools sollten die menschliche Entscheidungsfindung nach Möglichkeit ersetzen.", False),
    ("KI-Manager sollten die Skalierung von KI-Technologien verantwortungsvoll vorantreiben.", True),
    ("Urheberrechtlich geschütztes Material darf ohne Genehmigung in KI-Tools verwendet werden.", False),
    ("KI-Manager müssen über neue KI-Vorschriften auf dem Laufenden bleiben.", True),
    ("KI-generierte Ideen sollten immer dem KI-System selbst zugeschrieben werden.", False),
    ("Ein KI-Manager bewertet Anbieter von KI-Tools hinsichtlich Compliance und Sicherheit.", True)
]

def save_game(balance, round_val, score, max_rounds, streak, streak_bonus, wins, active_stars, answered_questions):
    data = {
        "balance": balance,
        "round": round_val,
        "score": score,
        "max_rounds": max_rounds,
        "streak": streak,
        "streak_bonus": streak_bonus,
        "wins": wins,
        "active_stars": active_stars,
        "answered_questions": answered_questions
    }
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print(f"Error saving game: {e}")

def load_game():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
            balance = data.get("balance", 10)
            if balance <= 0:
                balance = 10
            return (
                balance,
                data.get("round", 1),
                data.get("score", 0),
                data.get("max_rounds", 0),
                data.get("streak", 0),
                data.get("streak_bonus", 1.0),
                data.get("wins", 0),
                data.get("active_stars", 0),
                data.get("answered_questions", [])
            )
        except Exception as e:
            print(f"Error loading game: {e}")
    return 10, 1, 0, 0, 0, 1.0, 0, 0, []

def play_sound(sound):
    pygame.mixer.Sound.play(sound)

def get_card_name(value, short_form=True):
    if value == 11:
        return "B" if short_form else "Bube"
    elif value == 12:
        return "D" if short_form else "Dame"
    elif value == 13:
        return "K" if short_form else "König"
    elif value == 14:
        return "A" if short_form else "Ass"
    elif value == 15:  # Joker (default type)
        return "Joker"
    return str(value)

def draw_card(canvas, x, y, rank, suit):
    color = "red" if suit in ["♥", "♦"] else "black"
    canvas.create_rectangle(x, y, x + 100, y + 150, outline="black", width=3, fill="white")
    canvas.create_text(x + 15, y + 15, text=rank, font=("Arial", 20, "bold"), anchor="nw", fill=color)
    canvas.create_text(x + 50, y + 75, text=suit, font=("Arial", 30), anchor="center", fill=color)
    canvas.create_text(x + 85, y + 135, text=rank, font=("Arial", 20, "bold"), anchor="se", fill=color)

def draw_card_back(canvas, x, y):
    canvas.create_rectangle(x, y, x + 100, y + 150, outline="#660033", width=3, fill="#660033")
    canvas.create_text(x + 50, y + 66, text="🂠", font=("Arial", 148), anchor="center", fill="white")

def format_gold_balance(balance):
    # Summaries for comedic large numbers
    if balance >= 1_000_000_000_000_000_000_000_000_000:
        return f"1 Elon Musk"
    elif balance >= 1_000_000_000_000_000_000_000_000:
        return f"2 Jeff Bezos"
    elif balance >= 1_000_000_000_000_000_000_000:
        return f"3 Mark Zckrbrg"
    elif balance >= 1_000_000_000_000_000_000:
        return f"5 Larry Ellison"
    elif balance >= 1_000_000_000_000_000:
        return f"6 Bill Gates"
    elif balance >= 1_000_000_000_000:
        return f"7 Warren Buffett"
    elif balance >= 1_000_000_000:
        return f"{balance / 1_000_000_000:.2f} B"
    elif balance >= 1_000_000:
        return f"{balance / 1_000_000:.2f} M"
    else:
        return f"{balance}"

def format_gold_balance_numbers(balance):
    # Summaries for scientific large numbers
    if balance >= 1_000_000_000_000_000_000_000_000_000:
        return f"{balance / 1_000_000_000_000_000_000_000_000_000:.2f} Oc"
    elif balance >= 1_000_000_000_000_000_000_000_000:
        return f"{balance / 1_000_000_000_000_000_000_000_000:.2f} Sp"
    elif balance >= 1_000_000_000_000_000_000_000:
        return f"{balance / 1_000_000_000_000_000_000_000:.2f} Sx"
    elif balance >= 1_000_000_000_000_000_000:
        return f"{balance / 1_000_000_000_000_000_000:.2f} Qi"
    elif balance >= 1_000_000_000_000_000:
        return f"{balance / 1_000_000_000_000_000:.2f} Qa"
    elif balance >= 1_000_000_000_000:
        return f"{balance / 1_000_000_000_000:.2f} T"
    elif balance >= 1_000_000_000:
        return f"{balance / 1_000_000_000:.2f} B"
    elif balance >= 1_000_000:
        return f"{balance / 1_000_000:.2f} M"
    else:
        return f"{balance}"

class CardGame:
    def __init__(self, master):
        self.master = master
        master.title("Higher or Lower - Das LVQ Kartenspiel")
        window_width = 640
        window_height = 700
        master.geometry(f"{window_width}x{window_height}")
        master.configure(bg="#003333")
        master.resizable(False, False)

        self.scale_factor = window_height / 700
        self.game_over = False
        self.bet_amount = 1

        # Joker cooldown initialization
        self.joker_cooldown = 0

        # Quiz card initialization
        self.quiz_cards = QUIZ_QUESTIONS.copy()
        self.active_stars = 0
        self.answered_questions = []

        # Sound & reset menus
        menu_bar = tk.Menu(master)
        master.config(menu=menu_bar)
        self.sounds_enabled = True
        reset_menu = tk.Menu(menu_bar, tearoff=0)
        reset_menu.add_command(label="Reset Game", command=self.manual_reset)
        reset_menu.add_command(label="About", command=self.about)
        menu_bar.add_cascade(label="Game", menu=reset_menu)
        sound_menu = tk.Menu(menu_bar, tearoff=0)
        sound_menu.add_command(label="Sounds An/Aus", command=self.toggle_sounds)
        menu_bar.add_cascade(label="Options", menu=sound_menu)

        # Game state variables
        self.wins = 0
        self.joker_found = False
        self.joker_shield = False
        self.high_roller_active = False
        self.high_roller_rounds = 0
        self.lucky_streak_active = False
        self.lucky_streak_rounds = 0
        self.cursed_joker_active = False
        self.fifty_fifty_active = False
        self.wheel_active = False
        self.quiz_active = False

        # NEW: the possible percentages for Wheel of Fortune
        self.wheel_percentages = [
            10, 20, 30, 40, 50, 60, 70, 80, 90, 100,
            -90, -80, -70, -60, -50, -40, -30, -20, -10
        ]

        # Load sounds
        self.start_sound = pygame.mixer.Sound(os.path.join(game_folder, "hmm-male.ogg"))
        self.win_sound = pygame.mixer.Sound(os.path.join(game_folder, "collect-points.ogg"))
        self.lose_sound = pygame.mixer.Sound(os.path.join(game_folder, "no-with-attitude-3.ogg"))
        self.draw_sound = pygame.mixer.Sound(os.path.join(game_folder, "eh.ogg"))
        self.game_over_sound = pygame.mixer.Sound(os.path.join(game_folder, "sub-bass-4-seconds.ogg"))
        self.joker_sound = pygame.mixer.Sound(os.path.join(game_folder, "joker.ogg"))
        self.highroller_sound = pygame.mixer.Sound(os.path.join(game_folder, "fanfare.ogg"))
        self.card_shuffle = pygame.mixer.Sound(os.path.join(game_folder, "cards.ogg"))
        self.card_snap = pygame.mixer.Sound(os.path.join(game_folder, "card-snap.ogg"))
        self.wheel_spin = pygame.mixer.Sound(os.path.join(game_folder, "wheel-spin.ogg"))
        self.set_sound_volumes()
        self.master.after(420, self.start_sound.play)

        # Load saved game state
        (self.balance, self.round, self.score, self.max_rounds,
         self.streak, self.streak_bonus, self.wins, self.active_stars,
         self.answered_questions) = load_game()

        self.bet_var = tk.StringVar(value=str(self.bet_amount))
        self.init_ui()

    def toggle_sounds(self):
        self.sounds_enabled = not self.sounds_enabled
        status = "enabled" if self.sounds_enabled else "disabled"
        self.message_label.config(text=f"Sounds {status}", fg="yellow")

    def play_sound(self, sound):
        if self.sounds_enabled:
            pygame.mixer.Sound.play(sound)

    def manual_reset(self):
        if messagebox.askyesno("Reset Game", "Sind Sie sicher, dass Sie alle Spielwerte zurücksetzen möchten?"):
            self.score = 0
            self.wins = 0
            self.balance = 10
            self.balance_label.config(text=f"Gold:\n{format_gold_balance(self.balance)}")
            self.round_label.config(text="Runde: 0")
            self.wins_label.config(text="Wins: 0")
            self.current_card = random.randint(2, 14)
            self.current_suit = self.get_suit()
            self.active_stars = 0
            self.answered_questions = []
            self.update_star_panel()
            self.draw_current_card()
            self.new_card_label.config(text="Neue Karte: ?")
            self.message_label.config(text="", fg="white")
            self.higher_button.config(state="normal")
            self.lower_button.config(state="normal")
            self.restart_button.grid_remove()
            self.game_over = False
            self.draw_new_card_back()
            self.max_rounds_label.config(text=f"Meiste wins pro Spiel: {self.max_rounds}")
            self.bet_var.set("1")
            self.joker_found = False
            self.joker_shield = False
            self.high_roller_active = False
            self.high_roller_rounds = 0
            self.fifty_fifty_active = False
            self.lucky_streak_active = False
            self.cursed_joker_active = False
            self.wheel_active = False
            self.quiz_active = False
            self.joker_cooldown = 0
            self.clear_joker()
            self.update_bet_buttons()
            self.master.after(360, self.card_shuffle.play)
            self.master.after(420, self.start_sound.play)

    def about(self):
        messagebox.showinfo("About this Game", "Created by Alexander Schmidt with\nChatGPT, DeepSeek & Gemini.\nFEB 2025 - Creative Commons")

    def init_ui(self):
        # Left-side betting panel
        self.betting_panel = tk.Frame(self.master, bg="#1a413e", width=100)
        self.betting_panel.pack(side="left", fill="both", expand=False)

        self.coin_icon = tk.Label(self.betting_panel, text="🪙", font=("Arial", 40),
                                  bg="#1a413e", fg="#ffcc66")
        self.coin_icon.pack(pady=int(10 * self.scale_factor))
        self.balance_label = tk.Label(
            self.betting_panel,
            text=f"Gold:\n{format_gold_balance(self.balance)}",
            font=("Helvetica", int(14 * self.scale_factor)),
            fg="#ffcc66", bg="#1a413e", justify="left"
        )
        self.balance_label.pack(pady=int(10 * self.scale_factor),
                                padx=int(20 * self.scale_factor), anchor="w")

        self.bet_label = tk.Label(self.betting_panel, text="Wetteinsatz:",
                                  font=("Helvetica", int(12 * self.scale_factor)),
                                  fg="#bacddc", bg="#1a413e", justify="left")
        self.bet_label.pack(pady=int(5 * self.scale_factor),
                            padx=int(20 * self.scale_factor), anchor="w")

        self.bet_options = [1, 10, 50, 100, 500, 1000, "All-in"]
        self.bet_buttons = []
        for amount in self.bet_options:
            btn = tk.Radiobutton(
                self.betting_panel, text=f"{amount}", variable=self.bet_var,
                value=str(amount),
                font=("Helvetica", int(10 * self.scale_factor)),
                fg="white", bg="#1a413e", selectcolor="#27275a",
                command=self.update_expected_profit,
                padx=int(4 * self.scale_factor), pady=int(2 * self.scale_factor),
                indicatoron=0, width=12
            )
            btn.pack(anchor="w", padx=int(20 * self.scale_factor),
                     pady=int(2 * self.scale_factor))
            self.bet_buttons.append(btn)
        self.update_bet_buttons()

        self.streak_label = tk.Label(
            self.betting_panel, text=f"Bonus:\nx {self.streak_bonus}",
            font=("Helvetica", int(12 * self.scale_factor)),
            fg="#cc99ff", bg="#1a413e", justify="left"
        )
        self.streak_label.pack(pady=int(8 * self.scale_factor),
                               padx=int(20 * self.scale_factor), anchor="w")
        self.expected_profit_label = tk.Label(
            self.betting_panel,
            text=f"Gewinnsumme:\n{int(self.bet_amount * self.streak_bonus)}",
            font=("Helvetica", int(12 * self.scale_factor)),
            fg="#99cc66", bg="#1a413e", justify="left"
        )
        self.expected_profit_label.pack(pady=0, padx=int(20 * self.scale_factor), anchor="w")

        self.joker_canvas = tk.Canvas(
            self.betting_panel, width=110, height=150,
            bg="#003333", highlightthickness=0
        )
        self.joker_canvas.pack(pady=(int(10 * self.scale_factor), 0),
                               padx=int(20 * self.scale_factor), anchor="w")

        # Stars panel (new vertical column)
        self.stars_panel = tk.Frame(self.master, bg="#1a413e", width=20)
        self.stars_panel.pack(side="left", fill="both", expand=False)

        self.star_canvas = tk.Canvas(
            self.stars_panel, width=40, height=550,
            bg="#1a413e", highlightthickness=0
        )
        self.star_canvas.pack(pady=(int(152 * self.scale_factor), 0),
                              padx=int(5 * self.scale_factor), anchor="w")
        self.update_star_panel()

        # Right-side game panel
        self.game_panel = tk.Frame(self.master, bg="#003333", width=450)
        self.game_panel.pack(side="right", fill="both", expand=True)

        self.title_label = tk.Label(
            self.game_panel, text="Higher or Lower?",
            font=("Helvetica", int(24 * self.scale_factor)),
            fg="white", bg="#003333"
        )
        self.title_label.pack(pady=int(18 * self.scale_factor))

        self.max_rounds_label = tk.Label(
            self.game_panel,
            text=f"Meiste wins pro Spiel: {self.max_rounds}",
            font=("Helvetica", int(14 * self.scale_factor)),
            fg="#cc99ff", bg="#003333"
        )
        self.max_rounds_label.pack()

        self.round_wins_frame = tk.Frame(self.game_panel, bg="#003333")
        self.round_wins_frame.pack(pady=int(5 * self.scale_factor))
        self.round_label = tk.Label(
            self.round_wins_frame,
            text=f"Runde: {self.score}",
            font=("Helvetica", int(14 * self.scale_factor)),
            fg="#ffcc66", bg="#003333"
        )
        self.round_label.pack(side="left", padx=5)

        self.wins_label = tk.Label(
            self.round_wins_frame,
            text=f"Wins: {self.wins}",
            font=("Helvetica", int(14 * self.scale_factor)),
            fg="#99cc66", bg="#003333"
        )
        self.wins_label.pack(side="left", padx=5)

        self.canvas = tk.Canvas(self.game_panel, width=350, height=200,
                                bg="#1a413e", highlightthickness=0)
        self.canvas.pack(pady=int(10 * self.scale_factor))

        self.current_card = random.randint(2, 14)
        self.current_suit = self.get_suit()
        self.draw_current_card()
        self.draw_new_card_back()

        self.new_card_label = tk.Label(
            self.game_panel,
            text="Neue Karte: ?",
            font=("Helvetica", int(16 * self.scale_factor)),
            fg="#bacddc", bg="#003333"
        )
        self.new_card_label.pack(pady=int(10 * self.scale_factor))

        self.message_label = tk.Label(
            self.game_panel,
            text="",
            font=("Helvetica", int(16 * self.scale_factor)),
            fg="white", bg="#003333", wraplength=350, height=3
        )
        self.message_label.pack(pady=int(10 * self.scale_factor))

        button_frame = tk.Frame(self.game_panel, bg="#003333")
        button_frame.pack(pady=int(20 * self.scale_factor))

        self.higher_button = tk.Button(
            button_frame, text="Higher",
            width=int(11 * self.scale_factor), height=int(2 * self.scale_factor),
            font=("Helvetica", int(14 * self.scale_factor)),
            command=lambda: self.guess("higher"), state="normal",
            bg="#27275a", fg="white", activebackground="#222288", activeforeground="white"
        )
        self.higher_button.grid(row=0, column=0, padx=int(7 * self.scale_factor))

        self.lower_button = tk.Button(
            button_frame, text="Lower",
            width=int(11 * self.scale_factor), height=int(2 * self.scale_factor),
            font=("Helvetica", int(14 * self.scale_factor)),
            command=lambda: self.guess("lower"), state="normal",
            bg="#27275a", fg="white", activebackground="#222288", activeforeground="white"
        )
        self.lower_button.grid(row=0, column=1, padx=int(7 * self.scale_factor))

        self.restart_button = tk.Button(
            button_frame, text="Neues Spiel",
            width=int(24 * self.scale_factor), height=int(1 * self.scale_factor),
            font=("Helvetica", int(14 * self.scale_factor)),
            command=self.restart_game, state="disabled",
            bg="#27275a", fg="white", activebackground="#225a27", activeforeground="white"
        )
        self.restart_button.grid(row=1, column=0, columnspan=2, pady=int(14 * self.scale_factor))
        self.restart_button.grid_remove()

        self.copyright_label = tk.Label(
            self.game_panel,
            text="🅭 2025",
            font=("Segoe UI Symbol", int(10 * self.scale_factor)),
            fg="#bacddc", bg="#003333"
        )
        self.copyright_label.pack(pady=int(38 * self.scale_factor))

    def set_sound_volumes(self):
        self.start_sound.set_volume(0.5)
        self.win_sound.set_volume(0.6)
        self.lose_sound.set_volume(0.6)
        self.draw_sound.set_volume(0.3)
        self.game_over_sound.set_volume(0.8)
        self.joker_sound.set_volume(0.5)
        self.highroller_sound.set_volume(0.2)
        self.card_shuffle.set_volume(0.4)
        self.card_snap.set_volume(0.1)
        self.wheel_spin.set_volume(0.1)

    def get_suit(self):
        return random.choice(["♥", "♦", "♣", "♠"])

    def draw_current_card(self):
        self.canvas.delete("current_card")
        rank = get_card_name(self.current_card, short_form=True)
        draw_card(self.canvas, 50, 25, rank, self.current_suit)

    def draw_new_card_back(self):
        self.canvas.delete("new_card")
        draw_card_back(self.canvas, 200, 25)

    def draw_new_card(self, rank, suit):
        """Draws the second (new) card on the main canvas (right side)."""
        self.canvas.delete("new_card")
        self.play_sound(self.card_snap)
        # If it's not a custom Joker type:
        if rank not in ["Joker", "High Roller", "Lucky Streak", "Cursed", "50/50", "Wheel of Fortune", "Shield", "Quiz"]:
            color = "red" if suit in ["♥", "♦"] else "black"
            self.canvas.create_rectangle(200, 25, 300, 175, outline="black", width=3,
                                         fill="white", tags="new_card")
            self.canvas.create_text(215, 40, text=rank, font=("Arial", 20, "bold"),
                                    anchor="nw", fill=color, tags="new_card")
            self.canvas.create_text(250, 100, text=suit, font=("Arial", 30),
                                    anchor="center", fill=color, tags="new_card")
            self.canvas.create_text(285, 160, text=rank, font=("Arial", 20, "bold"),
                                    anchor="se", fill=color, tags="new_card")
        else:
            self.draw_joker_card(rank)

    def draw_joker_card(self, joker_type):
        """Draws a special Joker card (or its variant) on the main canvas."""
        mapping = {
            "Shield": ("#ccffff", "#27275a", "☂"),
            "High Roller": ("#663399", "#ffcc66", "👑"),
            "Lucky Streak": ("#ccffcc", "#228b22", "🍀"),
            "Cursed": ("#fef3cc", "#654e00", "☠️"),
            "50/50": ("#ffcccc", "#330000", "💰"),
            "Wheel of Fortune": ("#ccccff", "#FF6600", "🎡"),
            "Joker": ("#ccffff", "#27275a", "☂"),
            "Quiz": ("#ffffff", "#00519c", "💡")
        }
        fill_color, text_color, symbol = mapping.get(joker_type, ("white", "black", "☂"))
        self.canvas.create_rectangle(200, 25, 300, 175, outline="black", width=3,
                                     fill=fill_color, tags="new_card")

        # Conditional check for Quiz card text
        card_text = "Quiz" if joker_type == "Quiz" else "Joker"

        self.canvas.create_text(210, 35, text=card_text, font=("Arial", 12, "bold"),
                                anchor="nw", fill=text_color, tags="new_card")
        self.canvas.create_text(250, 95, text=symbol, font=("Segoe UI Emoji", 45),
                                anchor="center", fill=text_color, tags="new_card")
        self.canvas.create_text(290, 165, text=card_text, font=("Arial", 12, "bold"),
                                anchor="se", fill=text_color, tags="new_card")


    def draw_joker_panel(self, joker_key):
        """Draws a smaller Joker card on the betting panel (left side)."""
        self.joker_canvas.delete("all")
        mapping = {
            "shield": ("#ccffff", "#27275a", "☂"),
            "high_roller": ("#663399", "#ffcc66", "👑"),
            "lucky_streak": ("#ccffcc", "#228b22", "🍀"),
            "cursed": ("#fef3cc", "#654e00", "☠️"),
            "fifty_fifty": ("#ffcccc", "#330000", "💰"),
            "wheel": ("#ffcccc", "#FF6600", "🎡"),
        }
        fill_color, text_color, symbol = mapping[joker_key]
        self.joker_canvas.create_rectangle(10, 10, 100, 140, outline="black",
                                           width=2, fill=fill_color)
        self.joker_canvas.create_text(20, 20, text="Joker", font=("Arial", 9, "bold"),
                                      anchor="nw", fill=text_color)
        self.joker_canvas.create_text(55, 74, text=symbol, font=("Segoe UI Emoji", 35),
                                      anchor="center", fill=text_color)
        self.joker_canvas.create_text(90, 130, text="Joker", font=("Arial", 9, "bold"),
                                      anchor="se", fill=text_color)

    def update_star_panel(self):
        """Updates the star panel based on the number of active stars."""
        self.star_canvas.delete("all")
        
        for i in range(20):
            x = 10
            y = 10 + i * 25
            color = "#ffcc66" if i < self.active_stars else "#003333"
            self.star_canvas.create_text(x, y, text="★", font=("Arial", 14),
                                         fill=color, anchor="nw")

    def handle_quiz_card(self):
        """Handles the logic for drawing and answering a quiz card."""
        if not self.quiz_cards:
            return
        # Choose a quiz card that hasn't been asked yet
        available_quizzes = [q for q in self.quiz_cards if q[0] not in self.answered_questions]
        if not available_quizzes:
            return

        self.quiz_question, self.quiz_answer = random.choice(available_quizzes)
        self.quiz_active = True
        self.higher_button.config(text="Wahr", command=lambda: self.answer_quiz(True))
        self.lower_button.config(text="Falsch", command=lambda: self.answer_quiz(False))
        self.higher_button.config(state="normal")
        self.lower_button.config(state="normal")

        self.play_sound(self.start_sound)
        self.quiz_question, self.quiz_answer = random.choice(self.quiz_cards)
        self.message_label.config(text=self.quiz_question, fg="#99ccff")
        self.draw_new_card("Quiz", "💡")

    def answer_quiz(self, answer):
        """Handles the player's answer to the quiz question."""
        if answer == self.quiz_answer:
            self.active_stars += 1
            self.answered_questions.append(self.quiz_question)
            self.quiz_cards.remove((self.quiz_question, self.quiz_answer))
            self.update_star_panel()
            self.message_label.config(text=random.choice(["Das ist korrekt!", "Gut gemacht!", "Richtig!"]), fg="#99cc66")
            self.play_sound(self.joker_sound)
            if self.active_stars == 20:
                self.message_label.config(text="Glückwunsch!\nDu bist ein KI Master.", fg="#99cc66")
                self.play_sound(self.win_sound)
                self.play_sound(self.highroller_sound)
        else:
            self.message_label.config(text=random.choice(["Du hast es vergeigt!", "Das ist falsch!", "Leider nein, leider gar nicht."]), fg="#ff6699")
            self.play_sound(self.lose_sound)

        self.quiz_active = False
        self.higher_button.config(text="Higher", command=lambda: self.guess("higher"))
        self.lower_button.config(text="Lower", command=lambda: self.guess("lower"))
        # Clear the Quiz card from the main canvas
        self.canvas.delete("new_card")
        self.draw_new_card_back()
        self.enable_buttons()
        self.joker_cooldown = 3

    def spin_wheel(self):
        """Animate the spinning wheel for the Wheel of Fortune joker."""
        if not hasattr(self, 'spin_round_counter'):
            self.spin_round_counter = 0
        if self.spin_round_counter < 7:
            self.play_sound(self.wheel_spin)
        self.spin_round_counter += 1

        elapsed = time.time() - self.wheel_start_time
        if elapsed < 7:
            # Speed up for first ~5 sec, then slow down
            delay = 50 if elapsed < 5 else int(50 + ((elapsed - 3) / 2) * (300 - 50))
            spin_value = self.wheel_percentages[self.wheel_index % len(self.wheel_percentages)]
            self.wheel_index += 1
            display_text = f"Bewertung:\n{'+' if spin_value > 0 else ''}{spin_value}%"
            self.message_label.config(text=display_text, fg="#ffcc99")
            self.master.after(delay, self.spin_wheel)
        else:
            final_spin_value = self.wheel_percentages[self.wheel_index % len(self.wheel_percentages)]
            self.message_label.config(text=f"Ergebnis:\n{'+' if final_spin_value > 0 else ''}{final_spin_value}%",
                                      fg="#f3e7db")
            self.master.after(1500, lambda: self.finalize_wheel(final_spin_value))

    def finalize_wheel(self, spin_value):
        """Applies the final spin value of the Wheel of Fortune to the player's balance."""
        winning_amount = int(self.balance * (spin_value / 100.0))
        self.update_balance(winning_amount)
        if winning_amount >= 0:
            final_message = (f"Dein neuer Job bringt dir {spin_value}%\n"
                             f"+{format_gold_balance_numbers(winning_amount)} Gold")
            self.message_label.config(text=final_message, fg="#99ff99")
        else:
            final_message = (f"Die Prüfung kostet dich {spin_value}%\n"
                             f"-{format_gold_balance_numbers(-winning_amount)} Gold")
            self.message_label.config(text=final_message, fg="#ff9999")

        self.wheel_active = False
        self.play_sound(self.joker_sound)
        # Start the 3-guess cooldown the moment Wheel ends
        self.joker_cooldown = 3
        self.master.after(2000, self.new_round_after_wheel)

    def new_round_after_wheel(self):
        self.spin_round_counter = 0
        self.clear_joker()
        self.update_bet_buttons()
        new_card, new_suit = self.deal_new_card()
        self.update_cards(new_card, new_suit)
        self.higher_button.config(state="normal")
        self.lower_button.config(state="normal")
        self.update_expected_profit()

    def update_expected_profit(self):
        if self.fifty_fifty_active:
            self.expected_profit_label.config(text="Gewinnsumme:\n50/50")
            return
        if self.cursed_joker_active:
            self.bet_amount = self.balance - 1
        else:
            bet_value = self.bet_var.get()
            self.bet_amount = self.balance if bet_value == "All-in" else int(bet_value)
        expected = int(self.bet_amount * self.streak_bonus)
        self.expected_profit_label.config(text=f"Gewinnsumme:\n{format_gold_balance_numbers(expected)}")

    def update_bet_buttons(self):
        """Enable/disable bet radio buttons depending on balance and cursed-joker status."""
        for btn, amt in zip(self.bet_buttons, self.bet_options):
            if self.cursed_joker_active:
                if amt == "All-in":
                    btn.config(state="normal")
                    self.bet_var.set("All-in")
                else:
                    btn.config(state="disabled")
            else:
                if amt == "All-in":
                    btn.config(state="normal" if self.balance > 0 else "disabled")
                else:
                    btn.config(state="normal" if (isinstance(amt, int) and self.balance >= amt) else "disabled")
        if self.balance == 1:
            self.bet_var.set("1")

    def update_balance(self, amount):
        self.balance += amount
        self.balance_label.config(text=f"Gold:\n{format_gold_balance(self.balance)}")
        self.update_bet_buttons()
        if self.balance <= 0:
            self.game_over_sequence()

    def game_over_sequence(self):
        self.game_over = True
        self.update_bet_buttons()
        self.higher_button.config(state="disabled")
        self.lower_button.config(state="disabled")
        self.expected_profit_label.config(text="Gewinnsumme:\n0")
        self.restart_button.grid()
        self.restart_button.config(state="normal")
        self.message_label.config(text="♥ GAME OVER ♥", fg="#ff99ff")
        self.play_sound(self.game_over_sound)

    def clear_joker(self):
        self.joker_canvas.delete("all")

    def handle_joker(self, joker_type):
        """Apply the immediate effect of a Joker, plus draw it on the main canvas."""
        if joker_type == "Shield":
            self.joker_found = True
            self.message_label.config(text="Frank Michna ist da\nund passt auf dich auf.", fg="#ccffff")
            self.play_sound(self.joker_sound)
            self.draw_new_card("Shield", "☂")
            self.master.after(750, self.move_joker_to_panel, "shield")

        elif joker_type == "High Roller":
            self.message_label.config(text="Kai Heddergott kommt rein!\n5 Runden lang geht's hoch her.", fg="#ffcc00")
            self.play_sound(self.highroller_sound)
            self.draw_new_card("High Roller", "👑")
            self.master.after(750, self.move_joker_to_panel, "high_roller")

        elif joker_type == "Lucky Streak":
            self.lucky_streak_active = True
            self.lucky_streak_rounds = 3
            self.streak_bonus = 50.0
            self.streak_label.config(text=f"Streak Bonus:\nx {self.streak_bonus}")
            self.message_label.config(text="Glückssträhne!\n50x Bonus für 3 Gewinne.", fg="#32CD32")
            self.play_sound(self.joker_sound)
            self.draw_new_card("Lucky Streak", "🍀")
            self.master.after(750, self.move_joker_to_panel, "lucky_streak")

        elif joker_type == "Cursed":
            self.cursed_joker_active = True
            self.message_label.config(text="Der Admin kommt! Kamera an?\nJetzt geht's um alles.", fg="#fef3cc")
            self.play_sound(self.joker_sound)
            self.draw_new_card("Cursed", "☠️")
            self.master.after(750, self.move_joker_to_panel, "cursed")

        elif joker_type == "50/50":
            self.fifty_fifty_active = True
            self.message_label.config(text="Gefährliches Halbwissen!\nVerdopple oder halbiere dein Gold.", fg="#ffcccc")
            self.play_sound(self.joker_sound)
            self.draw_new_card("50/50", "💰")
            self.master.after(750, self.move_joker_to_panel, "fifty_fifty")
            # Force current card to be 7 for the 50/50 scenario
            self.current_card = 7
            self.current_suit = self.get_suit()
            self.draw_current_card()
            self.update_expected_profit()

        elif joker_type == "Wheel of Fortune":
            self.wheel_active = True
            self.message_label.config(text="Es ist Prüfungstag!", fg="#ffcc99")
            self.play_sound(self.joker_sound)
            self.draw_new_card("Wheel of Fortune", "🎡")
            self.master.after(750, self.move_joker_to_panel, "wheel")

    def deal_new_card(self):
        """
        Returns (new_card, new_suit), avoiding an identical card if cursed_joker_active.
        """
        new_card = random.randint(2, 14)
        new_suit = self.get_suit()
        if self.cursed_joker_active:
            # Avoid draws that exactly match the current card
            while new_card == self.current_card:
                new_card = random.randint(2, 14)
                new_suit = self.get_suit()
        return new_card, new_suit

    def guess(self, direction):
        if self.game_over:
            return

        try:
            # [CHANGED] Decrement cooldown on every guess (ties included)
            if self.joker_cooldown > 0:
                self.joker_cooldown -= 1

            # [CHANGED] Attempt to spawn a Joker or Quiz card only if cooldown == 0
            #           and no Joker or Quiz is currently active
            if (
                self.joker_cooldown == 0
                and not any([
                    self.joker_shield, self.high_roller_active, self.lucky_streak_active,
                    self.cursed_joker_active, self.fifty_fifty_active, self.wheel_active, self.quiz_active
                ])
            ):
                quiz_chance = 0.2  # Increased quiz chance to 20%
                joker_chance = 0.1 #keep the jokers at 10%
                random_value = random.random()

                if random_value < quiz_chance and self.quiz_cards:
                    self.handle_quiz_card()
                    return
                elif random_value < quiz_chance + joker_chance:
                    joker_type = random.choice([
                        "Shield", "High Roller", "Lucky Streak",
                        "Cursed", "50/50", "Wheel of Fortune"
                    ])
                    self.handle_joker(joker_type)
                    return

            # Disable buttons and re-enable after 0.75 sec
            self.higher_button.config(state="disabled")
            self.lower_button.config(state="disabled")
            self.master.after(750, self.enable_buttons)

            # --- Betting logic ---
            if self.cursed_joker_active:
                self.bet_amount = self.balance - 1
            else:
                bet_value = self.bet_var.get()
                self.bet_amount = self.balance if bet_value == "All-in" else int(bet_value)

            if self.bet_amount > self.balance:
                messagebox.showerror("Fehler", "Du hast nicht genug Gold für diese Wette.")
                return

            self.score += 1
            self.round_label.config(text=f"Runde: {self.score}")

            # Draw the new card
            new_card = random.randint(2, 14)
            new_suit = self.get_suit()
            self.new_card_label.config(text=f"Neue Karte: {get_card_name(new_card, short_form=True)}")
            self.draw_new_card(get_card_name(new_card, short_form=True), new_suit)

            # Brief delay to show the second card before final comparison
            self.master.after(750, self.update_cards, new_card, new_suit)

            # Check for tie
            if new_card == self.current_card:
                if self.high_roller_active:
                    self.high_roller_rounds -= 1
                    if self.high_roller_rounds <= 0:
                        self.high_roller_active = False
                        self.streak_bonus = 1.0
                        self.message_label.config(text="Kai Heddergott ist raus.", fg="#ffcc00")
                        self.clear_joker()
                        self.lower_button.config(state="normal")
                        self.play_sound(self.highroller_sound)
                        # [CHANGED] Start 3-guess cooldown
                        self.joker_cooldown = 3
                    else:
                        self.message_label.config(
                            text=f"Unentschieden!\nRunden verbleibend: {self.high_roller_rounds}",
                            fg="white"
                        )
                        self.play_sound(self.draw_sound)
                else:
                    self.message_label.config(text="Unentschieden! Gleich nochmal.", fg="white")
                    self.play_sound(self.draw_sound)

                if self.cursed_joker_active:
                    self.end_cursed_joker()
                return

            # 50/50 Joker logic
            if self.fifty_fifty_active:
                if (direction == "higher" and new_card > self.current_card) or \
                (direction == "lower" and new_card < self.current_card):
                    # Double entire gold
                    winnings = self.balance
                    self.update_balance(winnings)
                    self.message_label.config(text="Gold verdoppelt!", fg="#99cc66")
                    self.play_sound(self.win_sound)
                else:
                    # Lose half
                    loss = self.balance // 2
                    self.update_balance(-loss)
                    self.message_label.config(text="50% Gold verloren!", fg="#ff6699")
                    self.play_sound(self.lose_sound)

                self.fifty_fifty_active = False
                self.clear_joker()

                # [CHANGED] Start 3-guess cooldown when 50/50 ends
                self.joker_cooldown = 3

                self.update_expected_profit()
                return

            # Normal higher/lower logic
            win = ((direction == "higher" and new_card > self.current_card) or
                (direction == "lower" and new_card < self.current_card))

            if self.lucky_streak_active:
                self.streak_bonus = 50.0
                self.streak_label.config(text=f"Bonus:\nx {self.streak_bonus}")
                self.update_expected_profit()
                if win:
                    self.lucky_streak_rounds -= 1
                    if self.lucky_streak_rounds == 0:
                        self.lucky_streak_active = False
                        self.streak_bonus = 1.0
                        self.message_label.config(text="Deine Glückssträhne endet", fg="#32CD32")
                        self.streak_label.config(text=f"Bonus:\nx {self.streak_bonus}")
                        self.clear_joker()
                        self.update_expected_profit()
                        # [CHANGED] Start 3-guess cooldown
                        self.joker_cooldown = 3
                else:
                    self.message_label.config(text="Glückssträhne abgebrochen", fg="red")
                    self.lucky_streak_active = False
                    self.streak_bonus = 1.0
                    self.clear_joker()
                    self.update_expected_profit()
                    # [CHANGED] Start 3-guess cooldown
                    self.joker_cooldown = 3

            if win:
                winnings = int(self.bet_amount * self.streak_bonus)
                self.update_balance(winnings)
                self.wins += 1
                self.wins_label.config(text=f"Wins: {self.wins}")
                self.message_label.config(
                    text=f"Du gewinnst\n+{format_gold_balance_numbers(winnings)} Gold", fg="#99cc66"
                )
                self.update_streak(True)
                self.play_sound(self.win_sound)
            else:
                if self.joker_shield:
                    self.message_label.config(text="Frank Michna hat dich beschützt", fg="#ffcc00")
                    self.joker_shield = False
                    self.clear_joker()
                    self.play_sound(self.joker_sound)
                    # [CHANGED] Start 3-guess cooldown after shield is used
                    self.joker_cooldown = 3
                else:
                    self.update_balance(-self.bet_amount)
                    self.message_label.config(
                        text=f"Du verlierst\n-{self.bet_amount} Gold", fg="#ff6699"
                    )
                    self.update_streak(False)
                    self.play_sound(self.lose_sound)

            if self.cursed_joker_active:
                self.end_cursed_joker()

            if self.high_roller_active:
                self.high_roller_rounds -= 1
                if self.high_roller_rounds <= 0:
                    self.high_roller_active = False
                    self.streak_bonus = 1.0
                    self.message_label.config(text="Kai Heddergott ist raus", fg="#ffcc00")
                    self.clear_joker()
                    self.lower_button.config(state="normal")
                    self.play_sound(self.highroller_sound)
                    # [CHANGED] Start 3-guess cooldown
                    self.joker_cooldown = 3

        finally:
            # This always runs, even if the function returned early above
            save_game(
                self.balance, self.round, self.score,
                self.max_rounds, self.streak, self.streak_bonus, self.wins, self.active_stars, self.answered_questions
            )

    def end_cursed_joker(self):
        """Ends the cursed joker effect and re-enables normal bet choices."""
        self.cursed_joker_active = False
        self.clear_joker()
        self.update_bet_buttons()
        self.joker_cooldown = 3  # [CHANGED] Start cooldown whenever Cursed Joker ends

    def update_streak(self, won):
        """Updates streak bonus when a normal (non-Joker) round is won or lost."""
        if self.high_roller_active or self.lucky_streak_active:
            # If in high roller or lucky streak, we override normal streak logic
            self.streak_label.config(text=f"Bonus:\nx {self.streak_bonus}")
            self.update_expected_profit()
            return

        if won:
            if self.wins > self.max_rounds:
                self.max_rounds = self.wins
                self.max_rounds_label.config(text=f"Meiste wins pro Spiel: {self.max_rounds}")
            self.streak += 1
            if self.streak >= 50:
                self.streak_bonus = 15.0
            elif self.streak >= 30:
                self.streak_bonus = 12.0
            elif self.streak >= 20:
                self.streak_bonus = 7.0
            elif self.streak >= 10:
                self.streak_bonus = 2.0
            elif self.streak >= 5:
                self.streak_bonus = 1.5
            elif self.streak >= 2:
                self.streak_bonus = 1.2
        else:
            self.streak = 0
            self.streak_bonus = 1.0
        self.streak_label.config(text=f"Bonus:\nx {self.streak_bonus}")
        self.update_expected_profit()

    def update_cards(self, new_card, new_suit):
        """Completes the update of displayed cards after the brief delay."""
        if not self.game_over:
            self.current_card = new_card
            self.current_suit = new_suit
            self.draw_current_card()
            self.new_card_label.config(text="Neue Karte: ?")
            self.draw_new_card_back()

    def enable_buttons(self):
        """Re-enable the Higher/Lower buttons if not locked by Wheel or High Roller."""
        if self.wheel_active or self.quiz_active:
            return
        self.higher_button.config(state="normal")
        if self.high_roller_active:
            self.lower_button.config(state="disabled")
        else:
            self.lower_button.config(state="normal")

    def move_joker_to_panel(self, joker_key):
        """Moves the Joker to the left betting panel and sets up any required states."""
        self.clear_joker()
        if joker_key == "shield":
            self.joker_shield = True
            self.draw_joker_panel("shield")

        elif joker_key == "high_roller":
            self.high_roller_active = True
            self.high_roller_rounds = 5
            self.streak_bonus = 100.0
            self.streak_label.config(text=f"Bonus:\nx {self.streak_bonus}")
            self.update_expected_profit()
            self.draw_joker_panel("high_roller")
            self.lower_button.config(state="disabled")

        elif joker_key == "lucky_streak":
            self.lucky_streak_active = True
            self.lucky_streak_rounds = 3
            self.streak_bonus = 50.0
            self.streak_label.config(text=f"Bonus:\nx {self.streak_bonus}")
            self.update_expected_profit()
            self.draw_joker_panel("lucky_streak")

        elif joker_key == "cursed":
            self.cursed_joker_active = True
            self.update_bet_buttons()
            self.update_expected_profit()
            self.draw_joker_panel("cursed")

        elif joker_key == "fifty_fifty":
            self.fifty_fifty_active = True
            self.update_expected_profit()
            self.draw_joker_panel("fifty_fifty")

        elif joker_key == "wheel":
            self.wheel_active = True
            self.update_expected_profit()
            self.draw_joker_panel("wheel")
            self.draw_new_card_back()
            # Instead of spinning immediately, rename both buttons to "Spin"
            self.higher_button.config(text="Los", command=self.spin_wheel_wait, state="normal")
            self.lower_button.config(text="Los", command=self.spin_wheel_wait, state="normal")
            return

        elif joker_key == "quiz":
            self.quiz_active = True
            self.update_expected_profit()
            self.draw_joker_panel("quiz")
            self.draw_new_card_back()
            # Rename both buttons to "True" and "False"
            self.higher_button.config(text="Wahr", command=lambda: self.answer_quiz(True), state="normal")
            self.lower_button.config(text="Falsch", command=lambda: self.answer_quiz(False), state="normal")
            return

        self.draw_new_card_back()
        # Re-enable the guess buttons, except for the wheel (which is handled above)
        if joker_key != "wheel" and joker_key != "quiz":
            self.enable_buttons()

    def spin_wheel_wait(self):
        """
        Called when the user clicks one of the 'Spin' buttons.
        Reverts them to 'Higher' / 'Lower', then starts the spin.
        """
        self.higher_button.config(text="Higher", command=lambda: self.guess("higher"))
        self.lower_button.config(text="Lower", command=lambda: self.guess("lower"))
        self.higher_button.config(state="disabled")
        self.lower_button.config(state="disabled")

        self.wheel_start_time = time.time()
        self.wheel_index = random.randint(0, len(self.wheel_percentages) - 1)
        # Spin begins after a short delay
        self.master.after(20, self.spin_wheel)

    def restart_game(self):
        """Resets all relevant state to start a fresh game."""
        self.score = 0
        self.wins = 0
        self.balance = 10
        self.balance_label.config(text=f"Gold:\n{format_gold_balance(self.balance)}")
        self.round_label.config(text="Runde: 0")
        self.wins_label.config(text="Wins: 0")
        self.current_card = random.randint(2, 14)
        self.current_suit = self.get_suit()
        self.active_stars = 0
        self.answered_questions = []
        self.update_star_panel()
        self.draw_current_card()
        self.new_card_label.config(text="Neue Karte: ?")
        self.message_label.config(text="", fg="white")
        self.higher_button.config(state="normal")
        self.lower_button.config(state="normal")
        self.restart_button.grid_remove()
        self.game_over = False
        self.draw_new_card_back()
        self.max_rounds_label.config(text=f"Meiste wins pro Spiel: {self.max_rounds}")
        self.bet_var.set("1")
        self.joker_found = False
        self.joker_shield = False
        self.high_roller_active = False
        self.high_roller_rounds = 0
        self.fifty_fifty_active = False
        self.lucky_streak_active = False
        self.cursed_joker_active = False
        self.wheel_active = False
        self.quiz_active = False
        self.joker_cooldown = 0
        self.clear_joker()
        self.update_bet_buttons()
        self.master.after(360, self.card_shuffle.play)
        self.master.after(420, self.start_sound.play)

if __name__ == "__main__":
    root = tk.Tk()
    game = CardGame(root)
    root.mainloop()