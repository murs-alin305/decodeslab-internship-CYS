#!/usr/bin/env python3
"""
DecodeLabs Industrial Training Kit - Project 1
Password Strength Checker  (GUI Edition - Hacker Theme, v2: Deep Scan)

Run on Kali Linux:
    sudo apt install python3-tk   # if tkinter not already installed
    python3 password_strength_checker_gui.py

v2 changes:
- Typing in the box now only gives a quick "glow" on the border (cheap check).
- The [ RUN SECURITY SCAN ] button triggers a full animated multi-layer scan:
    LAYER 1 - Length & charset
    LAYER 2 - Pattern recognition (sequential / repeated / keyboard-walk)
    LAYER 3 - Dictionary + leetspeak-decoded dictionary/leak check
    LAYER 4 - Leaked credential database match
    LAYER 5 - Entropy + brute-force crack-time estimate (online vs offline)
    LAYER 6 - Composite risk score -> final verdict
"""

import tkinter as tk
from tkinter import font as tkfont
import string
import hmac
import math

# ---------------------------------------------------------------- #
#                       CORE SECURITY LOGIC                        #
# ---------------------------------------------------------------- #

COMMON_PASSWORDS = {
    "password", "123456", "12345678", "qwerty", "abc123",
    "password1", "111111", "123123", "letmein", "admin",
    "welcome", "monkey", "iloveyou", "dragon", "master",
    "sunshine", "princess", "football", "1234567", "123456789",
}

DICTIONARY_WORDS = {
    "password", "admin", "welcome", "login", "qwerty", "dragon",
    "master", "shadow", "sunshine", "monkey", "freedom", "whatever",
    "trustno", "letmein", "football", "baseball", "princess",
    "superman", "batman", "ninja", "secret", "hello", "computer",
    "internet", "security", "system", "network",
}

KEYBOARD_PATTERNS = [
    "qwertyuiop", "qwerty", "asdfghjkl", "asdfgh", "zxcvbnm", "zxcvbn",
    "1qaz2wsx", "qazwsx", "1q2w3e", "123qwe", "0987654321", "09876",
]

# Common leetspeak substitutions normalized back to plain letters
LEET_MAP = {
    "@": "a", "4": "a",
    "3": "e",
    "1": "i", "!": "i",
    "0": "o",
    "5": "s", "$": "s",
    "7": "t", "+": "t",
}

SYMBOLS = set(string.punctuation)


def analyze_password(password: str) -> dict:
    """
    Single linear pass over the password -> O(n), no nested loops.
    (Slide 8 IPO model + Slide 9 pythonic efficiency mindset)
    """
    length = len(password)
    has_upper = has_lower = has_digit = has_symbol = has_unicode = False

    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        if char.isdigit():
            has_digit = True
        if char in SYMBOLS:
            has_symbol = True
        if ord(char) > 127:
            has_unicode = True

    is_common = password.lower() in COMMON_PASSWORDS
    variety_score = sum([has_upper, has_lower, has_digit, has_symbol])

    charset_size = 0
    if has_lower:
        charset_size += 26
    if has_upper:
        charset_size += 26
    if has_digit:
        charset_size += 10
    if has_symbol:
        charset_size += len(string.punctuation)
    if has_unicode:
        charset_size += 100

    entropy_bits = round(length * math.log2(charset_size), 1) if charset_size else 0.0

    return {
        "length": length,
        "has_upper": has_upper,
        "has_lower": has_lower,
        "has_digit": has_digit,
        "has_symbol": has_symbol,
        "has_unicode": has_unicode,
        "is_common": is_common,
        "variety_score": variety_score,
        "entropy_bits": entropy_bits,
    }


def has_sequential_run(s: str, run_len: int = 3) -> bool:
    """Detects ascending/descending runs like 'abc', '123', 'cba'."""
    s = s.lower()
    for i in range(len(s) - run_len + 1):
        codes = [ord(c) for c in s[i:i + run_len]]
        if all(codes[j + 1] - codes[j] == 1 for j in range(len(codes) - 1)):
            return True
        if all(codes[j + 1] - codes[j] == -1 for j in range(len(codes) - 1)):
            return True
    return False


def has_repeated_run(s: str, run_len: int = 3) -> bool:
    """Detects repeated characters like 'aaa', '111'."""
    count = 1
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
            if count >= run_len:
                return True
        else:
            count = 1
    return False


def has_keyboard_pattern(s: str) -> bool:
    low = s.lower()
    return any(pat in low for pat in KEYBOARD_PATTERNS)


def dictionary_hit(s: str):
    low = s.lower()
    for word in DICTIONARY_WORDS:
        if word in low:
            return word
    return None


def normalize_leet(s: str) -> str:
    return "".join(LEET_MAP.get(c, c) for c in s.lower())


def deep_layer_analysis(password: str) -> dict:
    """Pattern + dictionary + leetspeak-decode layer (Layers 2 & 3)."""
    normalized = normalize_leet(password)
    return {
        "sequential": has_sequential_run(password),
        "repeated": has_repeated_run(password),
        "keyboard_pattern": has_keyboard_pattern(password),
        "dict_word": dictionary_hit(password),
        "leet_common_match": normalized in COMMON_PASSWORDS and password.lower() not in COMMON_PASSWORDS,
        "leet_dict_word": dictionary_hit(normalized) if normalized != password.lower() else None,
    }


def human_time(seconds: float) -> str:
    if seconds < 1:
        return "<1 sec"
    units = [
        ("centuries", 100 * 365 * 24 * 3600),
        ("years", 365 * 24 * 3600),
        ("days", 24 * 3600),
        ("hours", 3600),
        ("minutes", 60),
        ("seconds", 1),
    ]
    for name, count in units:
        if seconds >= count:
            return f"{seconds / count:,.1f} {name}"
    return "<1 sec"


def estimate_crack_times(entropy_bits: float):
    """Layer 5: rough brute-force time at two attacker speeds."""
    combos = 2.0 ** entropy_bits if entropy_bits else 0.0
    online = combos / 100        # throttled online login attempt (~100 guess/sec)
    offline = combos / 1e10      # offline fast-hash / GPU attack (~10B guess/sec)
    return human_time(online), human_time(offline)


def compute_risk_score(metrics: dict, deep: dict) -> int:
    """Layer 6: composite 0-100 security score."""
    if metrics["is_common"]:
        return 0

    score = 0.0
    score += min(metrics["length"] * 3, 40)
    score += metrics["variety_score"] * 6
    score += min(metrics["entropy_bits"] * 0.3, 30)
    if metrics["has_unicode"]:
        score += 6

    if deep["sequential"]:
        score -= 15
    if deep["repeated"]:
        score -= 15
    if deep["keyboard_pattern"]:
        score -= 15
    if deep["dict_word"]:
        score -= 20
    if deep["leet_common_match"] or deep["leet_dict_word"]:
        score -= 25

    return max(0, min(100, round(score)))


def classify_from_score(score: int, metrics: dict):
    if metrics["is_common"] or metrics["length"] < 8:
        return "WEAK", "weak"
    if score >= 70:
        return "STRONG", "strong"
    elif score >= 40:
        return "MEDIUM", "medium"
    else:
        return "WEAK", "weak"


def constant_time_compare(a: str, b: str) -> bool:
    """
    Slide 11 callback: never compare secrets with '=='.
    hmac.compare_digest avoids timing side-channel leaks.
    Kept here for the security-logic record (not wired into the UI flow).
    """
    return hmac.compare_digest(a.encode(), b.encode())


# ---------------------------------------------------------------- #
#                      HACKER-THEMED GUI (Tkinter)                 #
# ---------------------------------------------------------------- #

BG = "#0a0e0a"
FG = "#39ff14"
DIM = "#1f6b13"
ENTRY_BG = "#04140a"


class HackerUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DECODELABS // PASSWORD STRENGTH CHECKER")
        self.configure(bg=BG)
        self.geometry("660x640")
        self.resizable(False, False)

        mono = tkfont.Font(family="Courier", size=11)
        mono_bold = tkfont.Font(family="Courier", size=13, weight="bold")

        banner = (
            " ____  _____ ____ ___  ____  _____\n"
            "|  _ \\| ____/ ___/ _ \\|  _ \\| ____|\n"
            "| | | |  _|| |  | | | | | | |  _|\n"
            "| |_| | |__| |__| |_| | |_| | |___\n"
            "|____/|_____\\____\\___/|____/|_____|"
        )
        tk.Label(self, text=banner, bg=BG, fg=FG, font=("Courier", 9), justify="left").pack(pady=(14, 0))
        tk.Label(self, text="PROJECT 1 :: PASSWORD STRENGTH CHECKER",
                 bg=BG, fg=DIM, font=mono).pack(pady=(0, 14))

        tk.Label(self, text="ENTER TARGET PASSWORD >", bg=BG, fg=FG, font=mono_bold).pack(anchor="w", padx=24)

        entry_frame = tk.Frame(self, bg=BG)
        entry_frame.pack(fill="x", padx=24, pady=6)

        self.show_var = tk.BooleanVar(value=False)
        self.pw_var = tk.StringVar()
        self.entry = tk.Entry(
            entry_frame, textvariable=self.pw_var, show="*",
            bg=ENTRY_BG, fg=FG, insertbackground=FG,
            font=mono_bold, relief="flat",
            highlightthickness=2, highlightbackground=DIM, highlightcolor=DIM,
        )
        self.entry.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 8))
        self.entry.bind("<KeyRelease>", self.quick_feedback)

        tk.Checkbutton(
            entry_frame, text="SHOW", variable=self.show_var, command=self.toggle_show,
            bg=BG, fg=FG, selectcolor=BG, activebackground=BG, activeforeground=FG, font=mono,
        ).pack(side="left")

        tk.Label(self, text="(border glows red/yellow/green as you type - quick hint only)",
                 bg=BG, fg=DIM, font=("Courier", 8)).pack(anchor="w", padx=24)

        self.scan_btn = tk.Button(
            self, text="[ RUN SECURITY SCAN ]", command=self.deep_scan,
            bg=BG, fg=FG, activebackground=DIM, activeforeground=BG,
            font=mono_bold, relief="solid", bd=1, highlightbackground=FG,
        )
        self.scan_btn.pack(pady=12)

        self.output = tk.Text(
            self, height=21, width=72, bg="#000000", fg=FG,
            font=("Courier", 10), relief="flat",
            highlightthickness=1, highlightbackground=DIM, state="disabled",
        )
        self.output.pack(padx=24, pady=(6, 16))

        self.output.tag_config("weak", foreground="#ff3333")
        self.output.tag_config("medium", foreground="#ffd700")
        self.output.tag_config("strong", foreground="#39ff14")
        self.output.tag_config("dim", foreground=DIM)
        self.output.tag_config("normal", foreground=FG)

        self._steps = []
        self._step_idx = 0

        self.write_line(">> SYSTEM READY. TYPE A PASSWORD, THEN RUN SCAN...", "dim")

    # ---------------- UI helpers ---------------- #

    def toggle_show(self):
        self.entry.config(show="" if self.show_var.get() else "*")

    def write_line(self, text, tag="normal"):
        self.output.config(state="normal")
        self.output.insert("end", text + "\n", tag)
        self.output.config(state="disabled")
        self.output.see("end")

    def clear_output(self):
        self.output.config(state="normal")
        self.output.delete("1.0", "end")
        self.output.config(state="disabled")

    # ---------------- Quick live glow (cheap, on every keystroke) ---------------- #

    def quick_feedback(self, event=None):
        password = self.pw_var.get()
        if not password:
            self.entry.config(highlightbackground=DIM, highlightcolor=DIM)
            return

        metrics = analyze_password(password)
        if metrics["is_common"] or metrics["length"] < 8:
            color = "#ff3333"
        elif metrics["variety_score"] >= 4 and metrics["length"] >= 12:
            color = "#39ff14"
        elif metrics["variety_score"] >= 3 and metrics["length"] >= 8:
            color = "#ffd700"
        else:
            color = "#ff3333"

        self.entry.config(highlightbackground=color, highlightcolor=color)

    # ---------------- Deep multi-layer scan (button-triggered, animated) ---------------- #

    def deep_scan(self):
        password = self.pw_var.get()
        self.clear_output()

        if not password:
            self.write_line(">> [NO TARGET SET. AWAITING INPUT...]", "dim")
            return

        metrics = analyze_password(password)
        deep = deep_layer_analysis(password)
        score = compute_risk_score(metrics, deep)
        label, tag = classify_from_score(score, metrics)
        online_time, offline_time = estimate_crack_times(metrics["entropy_bits"])

        steps = [
            (">> DEEP SCAN INITIATED -- MULTI-LAYER ANALYSIS", "dim", 250),

            ("   [LAYER 1] LENGTH & CHARSET SCAN...", "dim", 300),
            (f"      LENGTH        : {metrics['length']} chars "
             f"{'[FAIL <8]' if metrics['length'] < 8 else '[OK]'}", "normal", 120),
            (f"      UPPER / LOWER : {'YES' if metrics['has_upper'] else 'NO'} / "
             f"{'YES' if metrics['has_lower'] else 'NO'}", "normal", 120),
            (f"      DIGIT / SYMBOL: {'YES' if metrics['has_digit'] else 'NO'} / "
             f"{'YES' if metrics['has_symbol'] else 'NO'}", "normal", 120),
            (f"      UNICODE       : {'YES' if metrics['has_unicode'] else 'NO'}", "normal", 280),

            ("   [LAYER 2] PATTERN RECOGNITION...", "dim", 300),
            (f"      SEQUENTIAL RUN  : {'DETECTED !!' if deep['sequential'] else 'CLEAN'}",
             "weak" if deep["sequential"] else "normal", 120),
            (f"      REPEATED CHARS  : {'DETECTED !!' if deep['repeated'] else 'CLEAN'}",
             "weak" if deep["repeated"] else "normal", 120),
            (f"      KEYBOARD WALK   : {'DETECTED !!' if deep['keyboard_pattern'] else 'CLEAN'}",
             "weak" if deep["keyboard_pattern"] else "normal", 280),

            ("   [LAYER 3] DICTIONARY + LEETSPEAK DECODE...", "dim", 300),
            (f"      RAW DICTIONARY  : {('MATCH: ' + deep['dict_word']) if deep['dict_word'] else 'CLEAN'}",
             "weak" if deep["dict_word"] else "normal", 120),
            (f"      LEET-DECODED    : "
             f"{'LEAK MATCH AFTER DECODING !!' if (deep['leet_common_match'] or deep['leet_dict_word']) else 'CLEAN'}",
             "weak" if (deep["leet_common_match"] or deep["leet_dict_word"]) else "normal", 280),

            ("   [LAYER 4] LEAKED CREDENTIAL DATABASE...", "dim", 300),
            (f"      KNOWN-BREACH LIST: {'MATCH FOUND !!' if metrics['is_common'] else 'CLEAN'}",
             "weak" if metrics["is_common"] else "normal", 280),

            ("   [LAYER 5] ENTROPY + BRUTE-FORCE ESTIMATE...", "dim", 300),
            (f"      ENTROPY         : {metrics['entropy_bits']} bits", "normal", 120),
            (f"      CRACK (ONLINE)  : ~{online_time}  (@ 100 guess/sec)", "normal", 120),
            (f"      CRACK (OFFLINE) : ~{offline_time}  (@ 10B guess/sec)", "normal", 280),

            ("   [LAYER 6] COMPOSITE RISK SCORE...", "dim", 300),
            (f"      SECURITY SCORE  : {score}/100", tag, 250),
            ("   ------------------------------------", "dim", 100),
            (f"   VERDICT           : {label}", tag, 150),
            (">> DEEP SCAN COMPLETE.", "dim", 0),
        ]

        self.scan_btn.config(state="disabled", text="[ SCANNING... ]")
        self._steps = steps
        self._step_idx = 0
        self._run_next_step()

    def _run_next_step(self):
        if self._step_idx >= len(self._steps):
            self.scan_btn.config(state="normal", text="[ RUN SECURITY SCAN ]")
            return
        text, tag, delay = self._steps[self._step_idx]
        self.write_line(text, tag)
        self._step_idx += 1
        self.after(delay, self._run_next_step)


if __name__ == "__main__":
    app = HackerUI()
    app.mainloop()
