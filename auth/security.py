import customtkinter as ctk
from config import APP_PASSWORD

class LoginDialog(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Security Authentication")
        self.geometry("360x220")
        self.resizable(False, False)
        self.authenticated = False

        self.label = ctk.CTkLabel(self, text="🔒 SECURITY AUTHENTICATION", font=("Consolas", 14, "bold"))
        self.label.pack(pady=15)

        self.entry = ctk.CTkEntry(self, show="*", width=220, font=("Consolas", 14), placeholder_text="Enter password...")
        self.entry.pack(pady=10)
        self.entry.focus()
        self.entry.bind("<Return>", lambda event: self.check_password())

        self.status_label = ctk.CTkLabel(self, text="", font=("Consolas", 11), text_color="#ff5555")
        self.status_label.pack(pady=2)

        self.btn = ctk.CTkButton(self, text="Unlock Assistant", command=self.check_password, width=140)
        self.btn.pack(pady=10)

    def check_password(self):
        if self.entry.get() == APP_PASSWORD:
            self.authenticated = True
            self.destroy()
        else:
            self.status_label.configure(text="Invalid Password! Try again.")
            self.entry.delete(0, "end")

def authenticate_user() -> bool:
    ctk.set_appearance_mode("Dark")
    login = LoginDialog()
    login.mainloop()
    return login.authenticated