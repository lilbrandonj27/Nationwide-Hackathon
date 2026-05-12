"""
SmartSchedule AI - FINAL WOW FACTOR VERSION 🚀 (Admin + Register Added)

🔥 NEW FEATURES:
- Register new users from login screen
- Admin dashboard (view all users + data)
- Admin login: username=admin password=seeall

RUN:
python this_file.py
"""

import tkinter as tk

# ---------- DATABASE ----------
users_db = {
    "Fashadm": {
        "password": "Musiq8",
        "schedule": [],
        "completed": [],
        "goals": []
    },
    "admin": {
        "password": "seeall",
        "schedule": [],
        "completed": [],
        "goals": []
    }
}

# ---------- AI ----------
class SmartAI:
    def generate_schedule(self):
        return [
            "Class: Math at 9AM",
            "Workout: Gym at 1PM",
            "Study: Library at 7PM",
            "Rest: Relax at 10PM"
        ]

    def detect_burnout(self, schedule):
        if len(schedule) >= 5:
            return "⚠️ High workload detected. Add rest."
        return "✅ Balanced schedule"

    def insights(self, completed, total):
        if total == 0:
            return "Start building your schedule."
        rate = completed / total
        if rate > 0.7:
            return "🔥 High productivity!"
        elif rate > 0.4:
            return "👍 Solid progress"
        else:
            return "⚠️ Try completing more tasks"

# ---------- APP ----------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SmartSchedule AI")
        self.geometry("390x820")
        self.configure(bg="black")

        self.ai = SmartAI()
        self.current_user = None

        self.show_login()

    # ---------- LOGIN ----------
    def show_login(self):
        self.clear()

        tk.Label(self, text="Login", fg="white", bg="black", font=("Helvetica", 22)).pack(pady=20)

        self.username = tk.Entry(self)
        self.username.pack(pady=5)

        self.password = tk.Entry(self, show="*")
        self.password.pack(pady=5)

        tk.Button(self, text="Login", command=self.login).pack(pady=5)
        tk.Button(self, text="Register", command=self.register).pack(pady=5)

    def login(self):
        user = self.username.get()
        pwd = self.password.get()

        if user in users_db and users_db[user]["password"] == pwd:
            self.current_user = user
            if user == "admin":
                self.show_admin()
            else:
                self.show_main()
        else:
            self.popup("Invalid login")

    def register(self):
        user = self.username.get()
        pwd = self.password.get()

        if not user or not pwd:
            self.popup("Enter username and password")
            return

        if user in users_db:
            self.popup("User already exists")
        else:
            users_db[user] = {"password": pwd, "schedule": [], "completed": [], "goals": []}
            self.popup("Account created! Please login.")

    # ---------- ADMIN ----------
    def show_admin(self):
        self.clear()

        tk.Label(self, text="Admin Dashboard", fg="white", bg="black",
                 font=("Helvetica", 20)).pack(pady=10)

        self.admin_view = tk.Text(self)
        self.admin_view.pack(fill="both", expand=True, padx=10, pady=10)

        for user, data in users_db.items():
            self.admin_view.insert("end", f"\nUser: {user}\n")
            self.admin_view.insert("end", f"Tasks: {len(data['schedule'])}\n")
            self.admin_view.insert("end", f"Completed: {len(data['completed'])}\n")
            self.admin_view.insert("end", f"Goals: {len(data['goals'])}\n")

        tk.Button(self, text="Logout", command=self.show_login).pack(pady=5)

    # ---------- MAIN ----------
    def show_main(self):
        self.clear()

        tk.Label(self, text=f"Welcome {self.current_user}", fg="white", bg="black",
                 font=("Helvetica", 18)).pack(pady=10)

        self.entry = tk.Entry(self)
        self.entry.pack(fill="x", padx=10, pady=5)

        self.time = tk.Entry(self)
        self.time.insert(0, "Time")
        self.time.pack(fill="x", padx=10, pady=5)

        tk.Button(self, text="Add Task", command=self.add_task).pack()
        tk.Button(self, text="AI Generate", command=self.ai_generate).pack()

        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill="both", padx=10, pady=10)

        tk.Button(self, text="Complete Task", command=self.complete_task).pack()
        tk.Button(self, text="Add Goal", command=self.add_goal).pack(pady=5)

        self.analytics = tk.Label(self, fg="white", bg="black")
        self.analytics.pack()

        self.progress = tk.Canvas(self, height=20, bg="gray")
        self.progress.pack(fill="x", padx=20, pady=5)

        self.insight_label = tk.Label(self, fg="white", bg="black")
        self.insight_label.pack()

        tk.Button(self, text="View Completed", command=self.view_completed).pack()
        tk.Button(self, text="Logout", command=self.show_login).pack(pady=5)

        self.output = tk.Text(self, height=6)
        self.output.pack(fill="both", padx=10)

        self.load_data()

    # ---------- FEATURES ----------
    def add_task(self):
        name = self.entry.get()
        time = self.time.get()
        item = f"{name} at {time}"

        users_db[self.current_user]["schedule"].append(item)
        self.refresh()

    def ai_generate(self):
        users_db[self.current_user]["schedule"] = self.ai.generate_schedule()
        self.refresh()

    def complete_task(self):
        sel = self.listbox.curselection()
        if not sel: return

        i = sel[0]
        item = users_db[self.current_user]["schedule"].pop(i)
        users_db[self.current_user]["completed"].append(item)
        self.refresh()

    def add_goal(self):
        goal = self.entry.get()
        users_db[self.current_user]["goals"].append(goal)
        self.output.insert("end", f"🎯 Goal Added: {goal}\n")

    def view_completed(self):
        self.output.insert("end", "\nCompleted:\n")
        for c in users_db[self.current_user]["completed"]:
            self.output.insert("end", c + "\n")

    # ---------- ANALYTICS ----------
    def refresh(self):
        self.listbox.delete(0, "end")
        schedule = users_db[self.current_user]["schedule"]

        for s in schedule:
            self.listbox.insert("end", s)

        total = len(schedule) + len(users_db[self.current_user]["completed"])
        done = len(users_db[self.current_user]["completed"])

        self.analytics.config(text=f"Tasks: {done}/{total} completed")

        self.progress.delete("all")
        if total > 0:
            width = (done / total) * 300
            self.progress.create_rectangle(0, 0, width, 20, fill="green")

        self.insight_label.config(text=self.ai.insights(done, total))

        burnout = self.ai.detect_burnout(schedule)
        self.output.insert("end", burnout + "\n")

    def load_data(self):
        self.refresh()

    # ---------- UTIL ----------
    def clear(self):
        for w in self.winfo_children():
            w.destroy()

    def popup(self, msg):
        top = tk.Toplevel(self)
        tk.Label(top, text=msg).pack(padx=20, pady=20)

# ---------- RUN ----------
if __name__ == "__main__":
    app = App()
    app.mainloop()
