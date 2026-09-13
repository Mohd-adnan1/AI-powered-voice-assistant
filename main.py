import sys
from auth.security import authenticate_user
from gui import AssistantGUI

def main():
    # 1. Terminal Password Lock
    if not authenticate_user():
        sys.exit()

    # 2. Launch CustomTkinter GUI HUD
    app = AssistantGUI()
    app.mainloop()

if __name__ == "__main__":
    main()