import tkinter as tk
import random
import time


class TypingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Speed Typing Challenge")
        self.root.geometry("950x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f1e6")

        # =========================
        # 題庫
        # =========================
        self.word_banks = {
            "Normal": [
                "apple",
                "banana",
                "cherry",
                "keyboard",
                "window",
                "school",
                "python",
                "orange",
                "student",
                "camera",
            ],
            "Hard": [
                "binary search",
                "linked list",
                "cloud storage",
                "data mining",
                "machine learning",
                "operating system",
            ],
            "Nightmare": [
                "Practice makes perfect.",
                "Accuracy is more important than speed.",
                "Python is a very useful programming language.",
                "Never give up when solving difficult problems.",
            ],
        }

        self.time_limits = {"Normal": 10, "Hard": 10, "Nightmare": 15}

        # =========================
        # 遊戲狀態
        # =========================
        self.current_text = ""
        self.current_round = 0
        self.total_rounds = 0
        self.score = 0
        self.wrong = 0
        self.time_left = 0
        self.timer_running = False
        self.selected_difficulty = tk.StringVar(value="Normal")

        # WPM
        self.round_start_time = 0
        self.total_typed_chars = 0
        self.total_elapsed_time = 0

        # 動畫
        self.flash_job = None

        # =========================
        # 標題
        # =========================
        title_label = tk.Label(
            root,
            text="SPEED TYPING CHALLENGE",
            font=("Arial", 28, "bold"),
            bg="#f5f1e6",
            fg="#222222",
        )
        title_label.pack(pady=15)

        # =========================
        # 設定區
        # =========================
        top_frame = tk.Frame(root, bg="#f5f1e6")
        top_frame.pack(pady=5)

        tk.Label(top_frame, text="難度：", font=("Arial", 13), bg="#f5f1e6").grid(
            row=0, column=0, padx=5
        )

        difficulty_menu = tk.OptionMenu(
            top_frame, self.selected_difficulty, "Normal", "Hard", "Nightmare"
        )
        difficulty_menu.config(font=("Arial", 11), width=12)
        difficulty_menu.grid(row=0, column=1, padx=5)

        tk.Label(top_frame, text="回合數：", font=("Arial", 13), bg="#f5f1e6").grid(
            row=0, column=2, padx=5
        )

        self.round_entry = tk.Entry(top_frame, font=("Arial", 12), width=10)
        self.round_entry.grid(row=0, column=3, padx=5)
        self.round_entry.insert(0, "5")

        self.start_button = tk.Button(
            top_frame,
            text="開始遊戲",
            font=("Arial", 12, "bold"),
            bg="#d59b54",
            fg="white",
            command=self.start_game,
        )
        self.start_button.grid(row=0, column=4, padx=10)

        # =========================
        # 資訊列
        # =========================
        info_frame = tk.Frame(root, bg="#f5f1e6")
        info_frame.pack(pady=10)

        self.round_label = tk.Label(
            info_frame, text="回合：0 / 0", font=("Arial", 12), bg="#f5f1e6"
        )
        self.round_label.grid(row=0, column=0, padx=20)

        self.score_label = tk.Label(
            info_frame, text="分數：0", font=("Arial", 12), bg="#f5f1e6"
        )
        self.score_label.grid(row=0, column=1, padx=20)

        self.timer_label = tk.Label(
            info_frame,
            text="剩餘時間：0",
            font=("Arial", 12, "bold"),
            fg="red",
            bg="#f5f1e6",
        )
        self.timer_label.grid(row=0, column=2, padx=20)

        self.wpm_label = tk.Label(
            info_frame, text="WPM：0.00", font=("Arial", 12), bg="#f5f1e6"
        )
        self.wpm_label.grid(row=0, column=3, padx=20)

        # =========================
        # 題目顯示區
        # =========================
        question_frame = tk.LabelFrame(
            root,
            text="題目顯示區",
            font=("Arial", 12, "bold"),
            padx=15,
            pady=15,
            bg="#f5f1e6",
        )
        question_frame.pack(pady=10, padx=20, fill="x")

        self.question_text_widget = tk.Text(
            question_frame,
            font=("Consolas", 22, "bold"),
            height=3,
            wrap="word",
            bd=0,
            bg="#fffdf7",
        )
        self.question_text_widget.pack(fill="x")
        self.question_text_widget.config(state="disabled")

        self.question_text_widget.tag_config("correct", foreground="green")
        self.question_text_widget.tag_config("wrong", foreground="red")
        self.question_text_widget.tag_config("remaining", foreground="black")

        # =========================
        # 輸入區
        # =========================
        input_frame = tk.LabelFrame(
            root,
            text="輸入區",
            font=("Arial", 12, "bold"),
            padx=15,
            pady=15,
            bg="#f5f1e6",
        )
        input_frame.pack(pady=10, padx=20, fill="x")

        self.input_entry = tk.Entry(input_frame, font=("Arial", 20), justify="center")
        self.input_entry.pack(fill="x", padx=10, pady=10)
        self.input_entry.bind("<Return>", self.check_answer)
        self.input_entry.bind("<KeyRelease>", self.on_typing)
        self.input_entry.config(state="disabled")

        self.submit_button = tk.Button(
            root,
            text="送出答案",
            font=("Arial", 12, "bold"),
            bg="#2f7d32",
            fg="white",
            command=self.check_answer,
            state="disabled",
        )
        self.submit_button.pack(pady=8)

        self.feedback_label = tk.Label(
            root, text="", font=("Arial", 15, "bold"), bg="#f5f1e6"
        )
        self.feedback_label.pack(pady=10)

        # =========================
        # 結算畫面區
        # =========================
        self.result_frame = tk.Frame(root, bg="#f5f1e6")
        self.result_frame.pack(pady=10)

        self.result_label = tk.Label(
            self.result_frame,
            text="",
            font=("Arial", 16, "bold"),
            bg="#f5f1e6",
            fg="#333333",
            justify="center",
        )
        self.result_label.pack(pady=20)

    def start_game(self):
        rounds_text = self.round_entry.get().strip()

        if not rounds_text.isdigit():
            self.feedback_label.config(text="回合數請輸入正整數", fg="red")
            return

        rounds = int(rounds_text)
        if rounds <= 0:
            self.feedback_label.config(text="回合數必須大於 0", fg="red")
            return

        self.total_rounds = rounds
        self.current_round = 0
        self.score = 0
        self.wrong = 0
        self.total_typed_chars = 0
        self.total_elapsed_time = 0

        self.score_label.config(text="分數：0")
        self.wpm_label.config(text="WPM：0.00")
        self.feedback_label.config(text="", fg="black")
        self.result_label.config(text="")
        self.start_button.config(state="disabled")
        self.round_entry.config(state="disabled")
        self.input_entry.config(state="normal")
        self.submit_button.config(state="normal")

        self.next_round()

    def next_round(self):
        if self.current_round >= self.total_rounds:
            self.end_game()
            return

        if self.flash_job:
            self.root.after_cancel(self.flash_job)
            self.flash_job = None

        self.current_round += 1
        difficulty = self.selected_difficulty.get()

        self.current_text = random.choice(self.word_banks[difficulty])
        self.time_left = self.time_limits[difficulty]
        self.round_start_time = time.time()

        self.round_label.config(
            text=f"回合：{self.current_round} / {self.total_rounds}"
        )
        self.timer_label.config(text=f"剩餘時間：{self.time_left}")
        self.show_text_colored("", self.current_text)

        self.input_entry.delete(0, tk.END)
        self.input_entry.focus()
        self.feedback_label.config(text="", fg="black")

        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        if not self.timer_running:
            return

        self.timer_label.config(text=f"剩餘時間：{self.time_left}")

        if self.time_left <= 0:
            self.timer_running = False
            self.wrong += 1
            self.feedback_label.config(
                text=f"時間到，答案是：{self.current_text}", fg="red"
            )
            self.play_flash_animation("red")
            self.root.after(1200, self.next_round)
            return

        self.time_left -= 1
        self.root.after(1000, self.update_timer)

    def on_typing(self, event=None):
        if not self.timer_running:
            return

        user_text = self.input_entry.get()
        self.show_text_colored(user_text, self.current_text)

    def show_text_colored(self, user_text, target_text):
        self.question_text_widget.config(state="normal")
        self.question_text_widget.delete("1.0", tk.END)

        for i, ch in enumerate(target_text):
            if i < len(user_text):
                if user_text[i] == ch:
                    self.question_text_widget.insert(tk.END, ch, "correct")
                else:
                    self.question_text_widget.insert(tk.END, ch, "wrong")
            else:
                self.question_text_widget.insert(tk.END, ch, "remaining")

        if len(user_text) > len(target_text):
            extra = user_text[len(target_text) :]
            self.question_text_widget.insert(tk.END, extra, "wrong")

        self.question_text_widget.config(state="disabled")

    def check_answer(self, event=None):
        if not self.timer_running:
            return

        user_text = self.input_entry.get()
        self.timer_running = False

        elapsed = time.time() - self.round_start_time
        self.total_elapsed_time += elapsed
        self.total_typed_chars += len(user_text)

        if self.total_elapsed_time > 0:
            wpm = (self.total_typed_chars / 5) / (self.total_elapsed_time / 60)
        else:
            wpm = 0

        self.wpm_label.config(text=f"WPM：{wpm:.2f}")

        if user_text == self.current_text:
            self.score += 1
            self.score_label.config(text=f"分數：{self.score}")
            self.feedback_label.config(text="答對了", fg="green")
            self.play_flash_animation("green")
        else:
            self.wrong += 1
            self.feedback_label.config(
                text=f"答錯了，正確答案是：{self.current_text}", fg="red"
            )
            self.play_flash_animation("red")

        self.root.after(1000, self.next_round)

    def play_flash_animation(self, color):
        original_bg = "#f5f1e6"
        flash_color = "#d8f3dc" if color == "green" else "#ffd6d6"

        widgets = [
            self.root,
            self.feedback_label,
            self.round_label,
            self.score_label,
            self.timer_label,
            self.wpm_label,
            self.result_frame,
            self.result_label,
        ]

        for widget in widgets:
            try:
                widget.configure(bg=flash_color)
            except:
                pass

        def restore():
            for widget in widgets:
                try:
                    widget.configure(bg=original_bg)
                except:
                    pass

        self.flash_job = self.root.after(250, restore)

    def end_game(self):
        self.input_entry.config(state="disabled")
        self.submit_button.config(state="disabled")
        self.start_button.config(state="normal")
        self.round_entry.config(state="normal")
        self.show_text_colored("", "遊戲結束")

        accuracy = 0
        if self.total_rounds > 0:
            accuracy = (self.score / self.total_rounds) * 100

        if self.total_elapsed_time > 0:
            final_wpm = (self.total_typed_chars / 5) / (self.total_elapsed_time / 60)
        else:
            final_wpm = 0

        result_text = (
            f"遊戲結束\n\n"
            f"總回合數：{self.total_rounds}\n"
            f"答對題數：{self.score}\n"
            f"答錯題數：{self.wrong}\n"
            f"正確率：{accuracy:.1f}%\n"
            f"平均 WPM：{final_wpm:.2f}"
        )

        self.result_label.config(text=result_text)
        self.feedback_label.config(text="遊戲結束！可以重新設定回合數再開始", fg="blue")


if __name__ == "__main__":
    root = tk.Tk()
    app = TypingGame(root)
    root.mainloop()
