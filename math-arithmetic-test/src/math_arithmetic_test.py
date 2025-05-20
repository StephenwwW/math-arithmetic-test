import tkinter as tk
from tkinter import messagebox
import random

class MathTestApp:
    def __init__(self, root):
        # 初始化主視窗與變數
        self.root = root
        self.root.title("數學邏輯測試")
        # 根據最大題目長度推算，設定主視窗寬度為480像素即可顯示完整
        self.root.geometry("480x500")
        self.questions = []  # 題目列表
        self.answers = []    # 答案列表
        self.entries = []    # 輸入框列表
        self.mistake_counts = []  # 每題錯誤次數
        self.correct_count = 0    # 答對題數
        self.incorrect_count = 0  # 答錯題數
        self.time_limit = 99      # 預設倒數秒數
        self.remaining_time = self.time_limit  # 剩餘秒數
        self.entry_vars = []      # 輸入框變數
        self.timer_job = None     # after job id，用於取消舊的計時器

        self.build_interface()    # 建立整體介面
        # 強制同步預設秒數，確保一開始就是99
        self.time_limit = int(self.time_var.get())
        self.remaining_time = self.time_limit
        self.generate_questions() # 產生初始題目

    def build_interface(self):
        # 建立題目顯示區塊
        self.question_frame = tk.Frame(self.root)
        self.question_frame.pack(pady=10)

        # 建立秒數設定欄位
        self.time_setting_frame = tk.Frame(self.root)
        self.time_setting_frame.pack(pady=5)
        tk.Label(self.time_setting_frame, text="請輸入秒數(30~99)：").pack(side=tk.LEFT)
        self.time_var = tk.StringVar(value="99")
        self.time_entry = tk.Entry(self.time_setting_frame, textvariable=self.time_var, width=5)
        self.time_entry.pack(side=tk.LEFT)

        self.question_labels = []  # 題目標籤列表

        # 建立10題的題目與輸入框
        for i in range(10):
            row = tk.Frame(self.question_frame)
            row.pack(pady=2)
            label = tk.Label(row, text=f"題目 {i+1}: ", width=45, anchor='w')  # 題目標籤加寬
            label.pack(side=tk.LEFT)
            entry_var = tk.StringVar()
            entry = tk.Entry(row, textvariable=entry_var, width=15)  # 輸入框加寬
            entry.pack(side=tk.LEFT)
            entry.bind("<Return>", lambda e, idx=i: self.check_answer(idx))  # 按Enter檢查答案
            self.question_labels.append(label)
            self.entry_vars.append(entry_var)
            self.entries.append(entry)

        # 建立倒數計時顯示
        self.timer_label = tk.Label(self.root, text="倒數：99 秒", font=('Helvetica', 14))
        self.timer_label.pack(pady=10)

        # 建立功能按鈕區塊
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        self.refresh_button = tk.Button(self.button_frame, text="重刷題目", command=self.refresh_questions)
        self.refresh_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = tk.Button(self.button_frame, text="清除輸入並重新計時", command=self.clear_inputs)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # 結果顯示標籤
        self.result_label = tk.Label(self.root, text="", font=('Helvetica', 12))
        self.result_label.pack(pady=10)

    def generate_number(self):
        # 隨機產生 3~5 位數整數，三種長度機率均等
        digit_length = random.choice([3, 4, 5])
        lower = 10 ** (digit_length - 1)
        upper = (10 ** digit_length) - 1
        return random.randint(lower, upper)

    def generate_question(self):
        # 隨機選擇一種運算符號，確保四則運算平均出現
        ops = ['+', '-', '*', '/']
        op = random.choice(ops)
        if op == '+':
            # 加法題目，確保答案為3~5位數
            while True:
                a = self.generate_number()
                b = self.generate_number()
                result = a + b
                if 100 <= result <= 99999:
                    break
            question = f"{a} + {b}"
            answer = result
        elif op == '-':
            # 減法題目，確保答案為3~5位數且不為負
            while True:
                a = self.generate_number()
                b = self.generate_number()
                if a < b:
                    a, b = b, a
                result = a - b
                if 100 <= result <= 99999:
                    break
            question = f"{a} - {b}"
            answer = result
        elif op == '*':
            # 乘法題目，確保答案為3~5位數
            while True:
                a = self.generate_number()
                b = self.generate_number()
                result = a * b
                if 100 <= result <= 99999:
                    break
            question = f"{a} * {b}"
            answer = result
        elif op == '/':
            # 除法題目，確保商、分子、分母都為3~5位數
            while True:
                quotient = self.generate_number()
                b = self.generate_number()
                # 避免除數為0或1，且分母分子都要3~5位數
                if b in (0, 1):
                    continue
                a = b * quotient
                if 100 <= quotient <= 99999 and 100 <= b <= 99999 and 100 <= a <= 99999:
                    break
            question = f"{a} / {b}"
            answer = quotient
        return question, answer

    def generate_questions(self):
        # 產生10題新題目，並根據使用者輸入設定倒數秒數
        try:
            user_time = int(self.time_var.get())
            if not (30 <= user_time <= 99):
                raise ValueError
        except ValueError:
            messagebox.showwarning("輸入錯誤", "請輸入30~99之間的整數作為秒數！")
            return
        self.time_limit = user_time
        self.questions.clear()
        self.answers.clear()
        self.mistake_counts = [0] * 10
        self.correct_count = 0
        self.incorrect_count = 0
        self.result_label.config(text="")
        for i in range(10):
            q, a = self.generate_question()
            self.questions.append(q)
            self.answers.append(a)
            self.question_labels[i].config(text=f"題目 {i+1}: {q}")
            self.entry_vars[i].set("")
            self.entries[i].config(state=tk.NORMAL)
        self.reset_timer()

    def reset_timer(self):
        # 重設倒數計時，並取消舊的計時器避免多重倒數
        self.remaining_time = self.time_limit
        if self.timer_job is not None:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
        self.update_timer()

    def update_timer(self):
        # 每秒更新倒數計時顯示，時間到自動結束測驗
        self.timer_label.config(text=f"倒數：{self.remaining_time} 秒")
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.timer_job = self.root.after(1000, self.update_timer)
        else:
            self.finish_test()
            self.timer_job = None

    def check_answer(self, index):
        # 檢查指定題目的使用者輸入是否正確，並給予提示
        if self.entries[index]['state'] == tk.DISABLED:
            return
        try:
            user_input = int(self.entry_vars[index].get())
        except ValueError:
            messagebox.showwarning("輸入錯誤", "請輸入有效的整數")
            return
        correct_answer = self.answers[index]
        if user_input == correct_answer:
            messagebox.showinfo("結果", f"第 {index+1} 題：正確！")
            self.entries[index].config(state=tk.DISABLED)
            self.correct_count += 1
        else:
            self.mistake_counts[index] += 1
            if self.mistake_counts[index] >= 3:
                messagebox.showerror("結果", f"第 {index+1} 題：錯誤三次，正確答案是 {correct_answer}")
                self.entries[index].config(state=tk.DISABLED)
                self.incorrect_count += 1
            else:
                remain = 3 - self.mistake_counts[index]
                messagebox.showwarning("結果", f"第 {index+1} 題：錯誤（剩餘 {remain} 次）")
        # 若全部題目都已作答完畢則結束測驗
        if all(entry['state'] == tk.DISABLED for entry in self.entries):
            self.finish_test()

    def refresh_questions(self):
        # 重新產生新題目並重設計時
        self.generate_questions()

    def clear_inputs(self):
        # 清除所有輸入框內容並重新計時
        for i in range(10):
            if self.entries[i]['state'] == tk.NORMAL:
                self.entry_vars[i].set("")
        self.reset_timer()

    def finish_test(self):
        # 統計作答結果，並將所有輸入框設為不可編輯
        unattempted = 0  # 未作答題數
        for i in range(10):
            if self.entries[i]['state'] == tk.NORMAL:
                # 未作答
                self.entries[i].config(state=tk.DISABLED)
                unattempted += 1
        # 答錯題數 = 錯三次被鎖定的題數（self.incorrect_count）
        # 答對題數 = self.correct_count
        # 未作答題數 = unattempted
        total_answered = self.correct_count + self.incorrect_count  # 共作答=答對+答錯
        self.result_label.config(
            text=f"答對：{self.correct_count} 題，答錯：{self.incorrect_count} 題，未作答：{unattempted} 題，共作答 {total_answered} 題"
        )
        self.timer_job = None

if __name__ == "__main__":
    # 程式進入點，啟動主視窗
    root = tk.Tk()
    app = MathTestApp(root)
    root.mainloop()
