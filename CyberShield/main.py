
import customtkinter as ctk
from tkinter import messagebox
from pathlib import Path
from datetime import datetime
from report import export_report
from analyzer import LogAnalyzer


# ---------------- PROJECT SETTINGS ----------------

BASE_DIR = Path(__file__).resolve().parent
LOG_FILE = BASE_DIR / "sample_log.txt"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

USERS = {
    "aditya": {"password": "adiraj@123", "ip": "192.168.1.10"},
    "nihaar": {"password": "nihaar@123", "ip": "192.168.1.11"},
    "ayaan": {"password": "ayaan@123", "ip": "192.168.1.12"},
    "ayush": {"password": "ayush@123", "ip": "192.168.1.13"},
}


# ---------------- MAIN APPLICATION ----------------

class CyberShieldApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("CyberShield | Login Security Monitor")
        self.geometry("1100x720")
        self.minsize(900, 600)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_main_area()
        self.refresh_dashboard()

    # ---------------- SIDEBAR ----------------

    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self, width=210, corner_radius=0
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        ctk.CTkLabel(
            self.sidebar,
            text="🛡 CyberShield",
            font=("Arial", 24, "bold"),
            text_color="#55B8FF"
        ).pack(padx=15, pady=(30, 5))

        ctk.CTkLabel(
            self.sidebar,
            text="LOGIN SECURITY MONITOR",
            font=("Arial", 10),
            text_color="#8B9BB4"
        ).pack(pady=(0, 35))

        for name, command in [
            ("Dashboard", self.show_dashboard),
            ("User Accounts", self.show_users),
            ("Security Logs", self.show_logs),
            ("Reports", self.show_reports),
        ]:
            ctk.CTkButton(
                self.sidebar,
                text=name,
                anchor="w",
                height=42,
                fg_color="transparent",
                hover_color="#24364F",
                command=command
            ).pack(fill="x", padx=14, pady=5)

        ctk.CTkLabel(
            self.sidebar,
            text="LOCAL DEMO SYSTEM",
            text_color="#73849C",
            font=("Arial", 10)
        ).pack(side="bottom", pady=20)

    # ---------------- MAIN AREA ----------------

    def create_main_area(self):
        self.main = ctk.CTkFrame(self, corner_radius=0)
        self.main.grid(row=0, column=1, sticky="nsew",
                       padx=18, pady=18)

        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_rowconfigure(1, weight=1)

        self.header = ctk.CTkLabel(
            self.main,
            text="Security Dashboard",
            font=("Arial", 28, "bold"),
            anchor="w"
        )
        self.header.grid(
            row=0, column=0, sticky="ew", padx=20, pady=(20, 12)
        )

        self.content = ctk.CTkFrame(
            self.main, fg_color="transparent"
        )
        self.content.grid(
            row=1, column=0, sticky="nsew", padx=15, pady=10
        )
        self.content.grid_columnconfigure((0, 1), weight=1)

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        # Reset the grid layout for the next page
        for column in range(3):
            self.content.grid_columnconfigure(
                column, weight=0, uniform=""
            )

        for row in range(3):
            self.content.grid_rowconfigure(row, weight=0)


    # ---------------- DASHBOARD ----------------

    def show_dashboard(self):
        self.header.configure(text="Security Dashboard")
        self.clear_content()

        analyzer = self.get_analyzer()
        failures = analyzer.show_results()
        suspicious = analyzer.detect_time_window(
            threshold=5, window_seconds=60
        )

        total_failures = sum(failures.values())

        self.content.grid_columnconfigure((0, 1, 2), weight=1)

        self.make_card(
            "Failed Logins", str(total_failures),
            "#55B8FF", 0
        )
        self.make_card(
            "Monitored Accounts", str(len(USERS)),
            "#61D6A5", 1
        )
        self.make_card(
            "Suspicious IPs", str(len(suspicious)),
            "#FF5C68", 2
        )

        login_frame = ctk.CTkFrame(self.content)
        login_frame.grid(
            row=1, column=0, columnspan=2,
            sticky="nsew", padx=6, pady=12
        )

        ctk.CTkLabel(
            login_frame, text="Demo Login Simulator",
            font=("Arial", 19, "bold")
        ).pack(anchor="w", padx=18, pady=(18, 10))

        self.username_entry = ctk.CTkEntry(
            login_frame, placeholder_text="Username"
        )
        self.username_entry.pack(fill="x", padx=18, pady=6)

        self.password_entry = ctk.CTkEntry(
            login_frame, placeholder_text="Password", show="*"
        )
        self.password_entry.pack(fill="x", padx=18, pady=6)

        ctk.CTkButton(
            login_frame, text="Simulate Login",
            command=self.login
        ).pack(fill="x", padx=18, pady=(10, 18))

        alert_frame = ctk.CTkFrame(self.content)
        alert_frame.grid(
            row=1, column=2, sticky="nsew",
            padx=6, pady=12
        )

        ctk.CTkLabel(
            alert_frame, text="Security Alerts",
            font=("Arial", 19, "bold")
        ).pack(anchor="w", padx=15, pady=15)

        if suspicious:
            alert_text = "\n".join(
                f"{ip}\n{count} failures in 60 seconds"
                for ip, count in suspicious.items()
            )
            alert_color = "#FF5C68"
        else:
            alert_text = "No IP has reached the alert threshold."
            alert_color = "#61D6A5"

        ctk.CTkLabel(
            alert_frame, text=alert_text,
            text_color=alert_color,
            wraplength=220, justify="left"
        ).pack(anchor="w", padx=15, pady=5)

        ctk.CTkButton(
            alert_frame, text="Refresh Analysis",
            command=self.refresh_dashboard
        ).pack(fill="x", padx=15, pady=15)

    def make_card(self, title, value, color, column):
        card = ctk.CTkFrame(self.content, height=105)
        card.grid(
            row=0, column=column, sticky="ew",
            padx=6, pady=6
        )
        card.grid_propagate(False)

        ctk.CTkLabel(
            card, text=title, text_color="#A8B7CB"
        ).pack(anchor="w", padx=14, pady=(14, 2))

        ctk.CTkLabel(
            card, text=value, font=("Arial", 27, "bold"),
            text_color=color
        ).pack(anchor="w", padx=14)

    # ---------------- LOGIN LOGIC ----------------

    def login(self):
        username = self.username_entry.get().strip().lower()
        password = self.password_entry.get()

        if username not in USERS:
            messagebox.showerror(
                "Login Failed", "Unknown demo username."
            )
            return

        user = USERS[username]
        status = (
            "SUCCESS" if password == user["password"]
            else "FAILED"
        )

        timestamp = datetime.now().strftime("%H:%M:%S")

        try:
            with open(LOG_FILE, "a", encoding="utf-8") as file:
                file.write(
                    f"{timestamp} | user={username} | "
                    f"ip={user['ip']} | status={status}\n"
                )
        except OSError as error:
            messagebox.showerror(
                "Log Error", f"Could not save login record:\n{error}"
            )
            return

        self.password_entry.delete(0, "end")

        if status == "SUCCESS":
            messagebox.showinfo(
                "Login Successful", f"Welcome, {username.title()}!"
            )
        else:
            messagebox.showerror(
                "Login Failed", "Incorrect password. Attempt recorded."
            )

        self.refresh_dashboard()

    # ---------------- ANALYSIS ----------------

    def get_analyzer(self):
        analyzer = LogAnalyzer()
        analyzer.analyze_file(str(LOG_FILE))
        return analyzer

    def refresh_dashboard(self):
        self.show_dashboard()

    # ---------------- OTHER VIEWS ----------------

    def show_users(self):
        self.header.configure(text="Monitored User Accounts")
        self.clear_content()
        self.content.grid_columnconfigure(0, weight=1)

        for username, user in USERS.items():
            card = ctk.CTkFrame(self.content)
            card.grid(sticky="ew", padx=8, pady=7)

            ctk.CTkLabel(
                card, text=username.title(),
                font=("Arial", 18, "bold")
            ).pack(anchor="w", padx=15, pady=(12, 3))

            ctk.CTkLabel(
                card, text=f"Simulated IP: {user['ip']}",
                text_color="#A8B7CB"
            ).pack(anchor="w", padx=15, pady=(0, 12))

    def show_logs(self):
        self.header.configure(text="Security Log Records")
        self.clear_content()
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

        textbox = ctk.CTkTextbox(
            self.content, font=("Consolas", 13)
        )
        textbox.grid(sticky="nsew", padx=6, pady=6)

        if LOG_FILE.exists():
            try:
                with open(LOG_FILE, "r", encoding="utf-8") as file:
                    textbox.insert("1.0", file.read())
            except OSError as error:
                textbox.insert("1.0", f"Could not read logs: {error}")
        else:
            textbox.insert("1.0", "No log file exists yet.")

        textbox.configure(state="disabled")

    
    def show_reports(self):
        self.header.configure(text="Security Reports")
        self.clear_content()
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=0)

        ctk.CTkLabel(
            self.content,
            text="Excel Reporting",
            font=("Arial", 23, "bold")
        ).grid(row=0, column=0, pady=(35, 10))

        ctk.CTkLabel(
            self.content,
            text="Export recorded login attempts to Excel.",
            text_color="#A8B7CB"
        ).grid(row=1, column=0, pady=10)

        def generate_report():
            try:
                report_path = export_report()
                messagebox.showinfo(
                    "Report Generated",
                    f"Excel report saved successfully!\n\n{report_path}"
                )
            except Exception as error:
                messagebox.showerror(
                    "Report Error",
                    f"Could not generate report:\n{error}"
                )

        ctk.CTkButton(
            self.content,
            text="Generate Excel Report",
            command=generate_report,
            height=42
        ).grid(row=2, column=0, pady=20)



if __name__ == "__main__":
    app = CyberShieldApp()
    app.mainloop()
