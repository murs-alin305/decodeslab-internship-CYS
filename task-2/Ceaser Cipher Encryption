#!/usr/bin/env python3
"""
DecodeLabs Industrial Training Kit - Project 2
Basic Encryption & Decryption -- Caesar Cipher Engine (GUI Edition, Blueprint Blue Theme)

Run on Kali Linux:
    sudo apt install python3-tk   # if tkinter not already installed
    python3 caesar_cipher_gui.py

Covers the brief:
    - Encrypt user text using a basic logic (Caesar cipher) -> Met
    - Decrypt the encrypted text                              -> Met
    - Display both encrypted and decrypted output             -> Met

Bonus / beyond brief:
    - Custom shift key (1-25) + optional Vigenere keyword mode
    - Case preservation + edge-case handling for spaces/digits/punctuation
    - Animated IPO model diagram that lights up as data flows through it
    - Per-character ASCII trace for the first few letters
    - Automatic round-trip validation: decrypt(encrypt(x)) == x
    - Brute-force attack simulator across all 25 Caesar keys
    - Plaintext-vs-ciphertext frequency chart

v2 changes:
    - Whole window content now scrolls (mouse wheel or scrollbar) so nothing
      gets cut off on shorter screens.
"""

import tkinter as tk
from tkinter import font as tkfont
import string

# ---------------------------------------------------------------- #
#                       CORE CIPHER LOGIC                          #
# ---------------------------------------------------------------- #

def shift_char(ch, shift):
    """Shift one character; case-preserved; non-letters left untouched."""
    if ch.isupper():
        base = ord('A')
        return chr((ord(ch) - base + shift) % 26 + base)
    if ch.islower():
        base = ord('a')
        return chr((ord(ch) - base + shift) % 26 + base)
    return ch  # spaces, digits, punctuation -> edge case handling


def compute_cipher(text, mode, shift_key, keyword, direction):
    """
    Unified Caesar / Vigenere encrypt-or-decrypt.
    direction: +1 to encrypt, -1 to decrypt.
    Returns (result_text, trace) where trace holds up to the first 4
    (original_char, applied_shift, result_char) tuples for the on-screen
    ASCII walkthrough.
    """
    kw = [c for c in keyword.upper() if c.isalpha()] or ['A']
    result_chars = []
    trace = []
    ki = 0
    for ch in text:
        if ch.isalpha():
            base_shift = shift_key if mode == "caesar" else (ord(kw[ki % len(kw)]) - ord('A'))
            if mode != "caesar":
                ki += 1
            applied = base_shift * direction
            rc = shift_char(ch, applied)
            if len(trace) < 4:
                trace.append((ch, applied, rc))
        else:
            rc = ch
        result_chars.append(rc)
    return ''.join(result_chars), trace


def letter_frequency(text):
    """% frequency distribution across A-Z (case-insensitive)."""
    counts = {c: 0 for c in string.ascii_uppercase}
    letters_only = [c.upper() for c in text if c.isalpha()]
    total = len(letters_only)
    if total == 0:
        return {c: 0.0 for c in string.ascii_uppercase}
    for c in letters_only:
        counts[c] += 1
    return {c: (counts[c] / total) * 100 for c in string.ascii_uppercase}


def brute_force_shifts(ciphertext):
    """Tiny key space (25 keys) = instant brute force."""
    results = []
    for s in range(1, 26):
        plain, _ = compute_cipher(ciphertext, "caesar", s, "", direction=-1)
        results.append((s, plain))
    return results


# ---------------------------------------------------------------- #
#                  BLUEPRINT BLUE THEME (Tkinter)                  #
# ---------------------------------------------------------------- #

BG = "#08111f"
PANEL_BG = "#0d1b2e"
GRID = "#15304d"
ACCENT = "#4fc3f7"
DIM = "#3a6486"
WHITE = "#e8f1fb"
ORANGE = "#ff8c42"
SUCCESS = "#33d17a"
FAIL = "#ff5252"
ENTRY_BG = "#0a1628"
CONTENT_W = 640
WINDOW_W = 720
WINDOW_H = 780
HEADER_H = 46


class CaesarUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DECODELABS // CAESAR CIPHER ENGINE")
        self.configure(bg=BG)
        self.geometry(f"{WINDOW_W}x{WINDOW_H}")
        self.resizable(False, False)

        mono = tkfont.Font(family="Courier", size=10)
        mono_bold = tkfont.Font(family="Courier", size=11, weight="bold")
        title_font = tkfont.Font(family="Courier", size=13, weight="bold")

        # ---- Developer credit, fixed top-left corner (always visible, never scrolls) ---- #
        tk.Label(self, text="MURSALIN AHMED", bg=BG, fg=ACCENT,
                  font=("Courier", 10, "bold")).place(x=12, y=10)
        tk.Label(self, text="Cybersecurity Trainee", bg=BG, fg=DIM,
                  font=("Courier", 8)).place(x=12, y=28)

        # ---- Scrollable body ---- #
        body = tk.Frame(self, bg=BG)
        body.place(x=0, y=HEADER_H, width=WINDOW_W, height=WINDOW_H - HEADER_H)

        self.canvas = tk.Canvas(body, bg=BG, highlightthickness=0)
        vscroll = tk.Scrollbar(body, orient="vertical", command=self.canvas.yview,
                                 bg=BG, troughcolor=ENTRY_BG, activebackground=DIM)
        self.canvas.configure(yscrollcommand=vscroll.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        vscroll.pack(side="right", fill="y")

        self.content = tk.Frame(self.canvas, bg=BG)
        self._content_id = self.canvas.create_window((0, 0), window=self.content, anchor="nw")
        self.content.bind("<Configure>",
                            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>",
                           lambda e: self.canvas.itemconfig(self._content_id, width=e.width))

        def _wheel(event):
            if getattr(event, "num", None) == 4:
                self.canvas.yview_scroll(-1, "units")
            elif getattr(event, "num", None) == 5:
                self.canvas.yview_scroll(1, "units")
            else:
                self.canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")
        self.canvas.bind_all("<MouseWheel>", _wheel)   # Windows / most setups
        self.canvas.bind_all("<Button-4>", _wheel)     # Linux scroll up
        self.canvas.bind_all("<Button-5>", _wheel)     # Linux scroll down

        body_parent = self.content

        # ---- Title block ---- #
        tk.Label(body_parent, text="DECODELABS // CAESAR CIPHER ENGINE", bg=BG, fg=WHITE,
                  font=title_font).pack(pady=(16, 2))
        tk.Label(body_parent, text="PROJECT 2 :: BASIC ENCRYPTION & DECRYPTION", bg=BG, fg=DIM,
                  font=mono).pack(pady=(0, 14))

        # ---- IPO blueprint diagram ---- #
        self.ipo_canvas = tk.Canvas(body_parent, width=CONTENT_W, height=110, bg=PANEL_BG,
                                     highlightthickness=1, highlightbackground=GRID)
        self.ipo_canvas.pack(padx=24, pady=(0, 14))
        self._draw_grid(self.ipo_canvas, CONTENT_W, 110)
        self.ipo_boxes = {}
        self._draw_ipo_diagram()

        # ---- Input ---- #
        tk.Label(body_parent, text="INPUT TEXT (plaintext to encrypt OR ciphertext to decrypt) >",
                  bg=BG, fg=ACCENT, font=mono_bold).pack(anchor="w", padx=24)
        self.input_text = tk.Text(body_parent, height=3, width=78, bg=ENTRY_BG, fg=WHITE,
                                    insertbackground=ACCENT, font=mono, relief="flat",
                                    highlightthickness=1, highlightbackground=DIM,
                                    highlightcolor=ACCENT, wrap="word")
        self.input_text.pack(padx=24, pady=(4, 8))

        # ---- Mode + key controls ---- #
        controls = tk.Frame(body_parent, bg=BG)
        controls.pack(fill="x", padx=24, pady=(0, 8))

        self.mode_var = tk.StringVar(value="caesar")
        tk.Radiobutton(controls, text="CAESAR (shift key)", variable=self.mode_var, value="caesar",
                        command=self._update_mode_fields, bg=BG, fg=WHITE, selectcolor=BG,
                        activebackground=BG, activeforeground=ACCENT, font=mono).pack(side="left")
        tk.Radiobutton(controls, text="VIGENERE (keyword)", variable=self.mode_var, value="vigenere",
                        command=self._update_mode_fields, bg=BG, fg=WHITE, selectcolor=BG,
                        activebackground=BG, activeforeground=ACCENT, font=mono).pack(side="left", padx=(16, 0))

        self.key_frame = tk.Frame(body_parent, bg=BG)
        self.key_frame.pack(fill="x", padx=24, pady=(0, 8))

        self.shift_label = tk.Label(self.key_frame, text="SHIFT KEY (1-25):", bg=BG, fg=WHITE, font=mono)
        self.shift_var = tk.StringVar(value="3")
        self.shift_spin = tk.Spinbox(self.key_frame, from_=1, to=25, textvariable=self.shift_var,
                                       width=6, bg=ENTRY_BG, fg=WHITE, insertbackground=ACCENT,
                                       font=mono, relief="flat", highlightthickness=1,
                                       highlightbackground=DIM, buttonbackground=PANEL_BG)

        self.keyword_label = tk.Label(self.key_frame, text="KEYWORD:", bg=BG, fg=WHITE, font=mono)
        self.keyword_var = tk.StringVar(value="SHIELD")
        self.keyword_entry = tk.Entry(self.key_frame, textvariable=self.keyword_var, width=20,
                                        bg=ENTRY_BG, fg=WHITE, insertbackground=ACCENT, font=mono,
                                        relief="flat", highlightthickness=1, highlightbackground=DIM,
                                        highlightcolor=ACCENT)

        self.shift_label.pack(side="left")
        self.shift_spin.pack(side="left", padx=(6, 0))

        # ---- Action buttons ---- #
        btn_frame = tk.Frame(body_parent, bg=BG)
        btn_frame.pack(pady=(4, 8))

        def make_btn(parent, text, cmd):
            return tk.Button(parent, text=text, command=cmd, bg=BG, fg=ACCENT,
                              activebackground=DIM, activeforeground=WHITE,
                              font=mono_bold, relief="solid", bd=1, highlightbackground=ACCENT,
                              padx=10)
        self._make_btn = make_btn

        make_btn(btn_frame, "[ ENCRYPT ]", self.encrypt_action).pack(side="left", padx=4)
        make_btn(btn_frame, "[ DECRYPT ]", self.decrypt_action).pack(side="left", padx=4)
        make_btn(btn_frame, "[ CLEAR ]", self.clear_action).pack(side="left", padx=4)

        self.status_label = tk.Label(body_parent, text="", bg=BG, fg=DIM, font=mono_bold)
        self.status_label.pack(pady=(0, 8))

        # ---- Output console ---- #
        tk.Label(body_parent, text="PROCESS LOG", bg=BG, fg=DIM, font=("Courier", 8)).pack(anchor="w", padx=24)
        out_frame = tk.Frame(body_parent, bg=BG)
        out_frame.pack(padx=24, pady=(2, 10))
        self.output = tk.Text(out_frame, height=13, width=78, bg="#040a14", fg=WHITE,
                                font=("Courier", 10), relief="flat", wrap="word",
                                highlightthickness=1, highlightbackground=GRID, state="disabled")
        out_scroll = tk.Scrollbar(out_frame, command=self.output.yview, bg=BG,
                                    troughcolor=ENTRY_BG, activebackground=DIM)
        self.output.configure(yscrollcommand=out_scroll.set)
        self.output.pack(side="left", fill="both")
        out_scroll.pack(side="right", fill="y")

        self.output.tag_config("accent", foreground=ACCENT)
        self.output.tag_config("white", foreground=WHITE)
        self.output.tag_config("dim", foreground=DIM)
        self.output.tag_config("orange", foreground=ORANGE)
        self.output.tag_config("success", foreground=SUCCESS)
        self.output.tag_config("fail", foreground=FAIL)

        # ---- Security analysis tools ---- #
        tk.Label(body_parent, text="SECURITY ANALYSIS -- why Caesar is a lockbox, not a vault",
                  bg=BG, fg=DIM, font=("Courier", 8)).pack(anchor="w", padx=24)
        sec_frame = tk.Frame(body_parent, bg=BG)
        sec_frame.pack(pady=(2, 10))
        make_btn(sec_frame, "[ BRUTE FORCE ALL 25 KEYS ]", self.brute_force_action).pack(side="left", padx=4)
        make_btn(sec_frame, "[ FREQUENCY ANALYSIS ]", self.frequency_action).pack(side="left", padx=4)

        self.freq_canvas = tk.Canvas(body_parent, width=CONTENT_W, height=210, bg=PANEL_BG,
                                       highlightthickness=1, highlightbackground=GRID)
        self.freq_canvas.pack(padx=24, pady=(0, 24))

        self._steps = []
        self._step_idx = 0

        self._update_mode_fields()
        self.write_line(">> SYSTEM READY. ENTER TEXT, CHOOSE A MODE, THEN ENCRYPT OR DECRYPT.", "dim")
        self.write_line(">> TIP: scroll down (mouse wheel or scrollbar) to see the security", "dim")
        self.write_line("   analysis tools below the process log.", "dim")

        self._center_window()

    # ---------------- window / drawing helpers ---------------- #

    def _center_window(self):
        self.update_idletasks()
        w, h = WINDOW_W, WINDOW_H
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{max(0,(sw-w)//2)}+{max(0,(sh-h)//2)}")

    def _draw_grid(self, canvas, w, h, step=20):
        for x in range(0, w, step):
            canvas.create_line(x, 0, x, h, fill=GRID)
        for y in range(0, h, step):
            canvas.create_line(0, y, w, y, fill=GRID)

    def _draw_ipo_diagram(self):
        c = self.ipo_canvas
        box_w, box_h, y0 = 150, 60, 25
        positions = {"input": 20, "process": 245, "output": 470}
        labels = {"input": "INPUT\n(Plaintext)", "process": "PROCESS\n(Algorithm + Key)", "output": "OUTPUT\n(Ciphertext)"}
        for key, x0 in positions.items():
            rect = c.create_rectangle(x0, y0, x0 + box_w, y0 + box_h,
                                        outline=DIM, width=1, fill=PANEL_BG)
            c.create_text(x0 + box_w / 2, y0 + box_h / 2, text=labels[key],
                           fill=WHITE, font=("Courier", 9, "bold"), justify="center")
            self.ipo_boxes[key] = rect
        a1 = c.create_line(170, y0 + box_h / 2, 245, y0 + box_h / 2, fill=DIM, width=2, arrow="last")
        a2 = c.create_line(395, y0 + box_h / 2, 470, y0 + box_h / 2, fill=DIM, width=2, arrow="last")
        self.ipo_arrows = [a1, a2]

    def _set_box(self, key, color, width=1):
        self.ipo_canvas.itemconfig(self.ipo_boxes[key], outline=color, width=width)

    def _set_arrow(self, idx, color, width=2):
        self.ipo_canvas.itemconfig(self.ipo_arrows[idx], fill=color, width=width)

    def _reset_ipo(self):
        for k in self.ipo_boxes:
            self._set_box(k, DIM, 1)
        for i in range(len(self.ipo_arrows)):
            self._set_arrow(i, DIM, 2)

    # ---------------- UI helpers ---------------- #

    def _update_mode_fields(self):
        self.keyword_label.pack_forget()
        self.keyword_entry.pack_forget()
        self.shift_label.pack_forget()
        self.shift_spin.pack_forget()
        if self.mode_var.get() == "caesar":
            self.shift_label.pack(side="left")
            self.shift_spin.pack(side="left", padx=(6, 0))
        else:
            self.keyword_label.pack(side="left")
            self.keyword_entry.pack(side="left", padx=(6, 0))

    def write_line(self, text, tag="white"):
        self.output.config(state="normal")
        self.output.insert("end", text + "\n", tag)
        self.output.config(state="disabled")
        self.output.see("end")

    def clear_output(self):
        self.output.config(state="normal")
        self.output.delete("1.0", "end")
        self.output.config(state="disabled")

    def get_shift_key(self):
        try:
            v = int(self.shift_var.get())
        except ValueError:
            v = 3
        return max(1, min(25, v))

    def clear_action(self):
        self.input_text.delete("1.0", "end")
        self.clear_output()
        self.status_label.config(text="")
        self.freq_canvas.delete("all")
        self._reset_ipo()
        self.write_line(">> CLEARED. READY FOR NEW INPUT.", "dim")

    # ---------------- Encrypt / Decrypt (animated) ---------------- #

    def _run_cipher_flow(self, direction):
        text = self.input_text.get("1.0", "end").rstrip("\n")
        if not text:
            self.write_line(">> [NO INPUT PROVIDED]", "dim")
            return

        mode = self.mode_var.get()
        shift_key = self.get_shift_key()
        keyword = self.keyword_var.get()

        result, trace = compute_cipher(text, mode, shift_key, keyword, direction)
        verify, _ = compute_cipher(result, mode, shift_key, keyword, -direction)
        round_trip_ok = (verify == text)

        action_word = "ENCRYPTING" if direction == 1 else "DECRYPTING"
        result_label = "CIPHERTEXT" if direction == 1 else "PLAINTEXT"
        key_desc = f"shift={shift_key}" if mode == "caesar" else f"keyword='{keyword.upper()}'"

        self.clear_output()
        self._reset_ipo()

        steps = [
            (lambda: self._set_box("input", ACCENT, 3), 250),
            (lambda: self.write_line(f">> {action_word} -- MODE: {mode.upper()} ({key_desc})", "accent"), 200),
            (lambda: self._set_arrow(0, ACCENT, 3), 200),
            (lambda: self._set_box("input", DIM, 1), 0),
            (lambda: self._set_box("process", ACCENT, 3), 250),
            (lambda: self.write_line("   [PROCESS] ASCII WALKTHROUGH (first characters):", "dim"), 200),
        ]

        for orig, applied, res in trace:
            steps.append((
                lambda o=orig, a=applied, r=res: self.write_line(
                    f"      '{o}' (ASCII {ord(o)})  --shift {a:+d}-->  '{r}' (ASCII {ord(r)})", "white"
                ), 160
            ))
        if not trace:
            steps.append((lambda: self.write_line("      (no alphabetic characters to trace)", "dim"), 160))

        steps += [
            (lambda: self._set_arrow(0, DIM, 2), 0),
            (lambda: self._set_arrow(1, ACCENT, 3), 250),
            (lambda: self._set_box("process", DIM, 1), 0),
            (lambda: self._set_box("output", ACCENT, 3), 250),
            (lambda: self.write_line(f"   [OUTPUT] {result_label}: {result}", "accent"), 200),
            (lambda: self.write_line(f"   ORIGINAL INPUT      : {text}", "white"), 160),
            (lambda: self._set_arrow(1, DIM, 2), 0),
        ]

        if round_trip_ok:
            steps.append((lambda: self.write_line("   ROUND-TRIP CHECK    : PASS (decrypt(encrypt(x)) == x)", "success"), 200))
            steps.append((lambda: self.status_label.config(text="\u2713 ROUND-TRIP VERIFIED", fg=SUCCESS), 0))
        else:
            steps.append((lambda: self.write_line("   ROUND-TRIP CHECK    : FAIL", "fail"), 200))
            steps.append((lambda: self.status_label.config(text="\u2717 ROUND-TRIP MISMATCH", fg=FAIL), 0))

        steps.append((lambda: self.write_line(">> PROCESS COMPLETE.", "dim"), 0))
        steps.append((lambda: self._set_box("output", DIM, 1), 0))

        self._steps = steps
        self._step_idx = 0
        self._run_next_step()

    def _run_next_step(self):
        if self._step_idx >= len(self._steps):
            return
        action, delay = self._steps[self._step_idx]
        action()
        self._step_idx += 1
        self.after(delay, self._run_next_step)

    def encrypt_action(self):
        self._run_cipher_flow(direction=1)

    def decrypt_action(self):
        self._run_cipher_flow(direction=-1)

    # ---------------- Security analysis tools ---------------- #

    def brute_force_action(self):
        text = self.input_text.get("1.0", "end").rstrip("\n")
        if not text:
            self.write_line(">> [NO INPUT PROVIDED]", "dim")
            return

        self.clear_output()
        actual_shift = self.get_shift_key()
        self.write_line(">> BRUTE FORCE SIMULATION -- TRYING ALL 25 CAESAR KEYS", "orange")
        self.write_line("   (tiny key space = instant brute force)", "dim")
        self.write_line("   ------------------------------------------------", "dim")
        for shift, plain in brute_force_shifts(text):
            tag = "accent" if shift == actual_shift else "white"
            marker = "  <-- CURRENT SHIFT KEY" if shift == actual_shift else ""
            self.write_line(f"   KEY {shift:>2}: {plain}{marker}", tag)
        self.write_line("   ------------------------------------------------", "dim")
        self.write_line(">> NOTE: Vigenere mode (keyword-based) is NOT vulnerable to this", "orange")
        self.write_line("   simple loop -- its key space grows with keyword length & alphabet reuse.", "orange")
        self.write_line(">> BRUTE FORCE COMPLETE.", "dim")

    def frequency_action(self):
        text = self.input_text.get("1.0", "end").rstrip("\n")
        if not text:
            self.write_line(">> [NO INPUT PROVIDED]", "dim")
            return

        mode = self.mode_var.get()
        shift_key = self.get_shift_key()
        keyword = self.keyword_var.get()
        ciphertext, _ = compute_cipher(text, mode, shift_key, keyword, direction=1)

        freq_plain = letter_frequency(text)
        freq_cipher = letter_frequency(ciphertext)
        max_val = max(5.0, max(freq_plain.values()), max(freq_cipher.values()))

        self.freq_canvas.delete("all")
        self._draw_grid(self.freq_canvas, CONTENT_W, 210, step=20)
        self.freq_canvas.create_text(10, 10, anchor="nw", text="PLAINTEXT FREQUENCY (%)",
                                       fill=WHITE, font=("Courier", 8, "bold"))
        self._draw_bars(freq_plain, y_top=24, color=WHITE, max_val=max_val)
        self.freq_canvas.create_text(10, 115, anchor="nw", text="CIPHERTEXT FREQUENCY (%)",
                                       fill=ORANGE, font=("Courier", 8, "bold"))
        self._draw_bars(freq_cipher, y_top=129, color=ORANGE, max_val=max_val)

        self.clear_output()
        self.write_line(">> FREQUENCY ANALYSIS COMPLETE.", "orange")
        self.write_line("   Notice the bar SHAPE is identical between plaintext and", "dim")
        self.write_line("   ciphertext -- only rotated by the shift key. This 'pattern", "dim")
        self.write_line("   preservation' weakness means an attacker can match this shape", "dim")
        self.write_line("   against known English letter frequency to recover the key", "dim")
        self.write_line("   without brute force.", "dim")
        self.write_line("   See the chart panel below.", "dim")

    def _draw_bars(self, freq_dict, y_top, color, max_val):
        letters = string.ascii_uppercase
        n = len(letters)
        bar_w = CONTENT_W / n
        chart_h = 70
        for i, letter in enumerate(letters):
            val = freq_dict[letter]
            h = (val / max_val) * chart_h if max_val > 0 else 0
            x0 = i * bar_w + 2
            x1 = (i + 1) * bar_w - 2
            y1 = y_top + chart_h
            y0 = y1 - h
            self.freq_canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
            self.freq_canvas.create_text((x0 + x1) / 2, y1 + 9, text=letter,
                                           fill=DIM, font=("Courier", 6))


if __name__ == "__main__":
    app = CaesarUI()
    app.mainloop()
