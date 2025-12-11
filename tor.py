import threading
import time
import requests
from stem.control import Controller
import customtkinter as ctk

TOR_SOCKS_PORT = 9050
TOR_CONTROL_PORT = 9051
TOR_PASSWORD = "pass here WITH the number: and then your has for it to work :3"

def reconnecter():
    with Controller.from_port(port=TOR_CONTROL_PORT) as controller:
        controller.authenticate(password=TOR_PASSWORD)
        controller.signal("NEWNYM")
        time.sleep(controller.get_newnym_wait())

def tor_ip():
    proxies = {
        "http": f"socks5h://127.0.0.1:{TOR_SOCKS_PORT}",
        "https": f"socks5h://127.0.0.1:{TOR_SOCKS_PORT}"
    }
    return requests.get("https://checkip.amazonaws.com", proxies=proxies, timeout=10).text.strip()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("opsex tor rotator")
        self.geometry("600x300")
        self.resizable(False, False)

        self.label = ctk.CTkLabel(self, text="checking tor connection :3")
        self.label.pack(pady=20)

        self.proclab = ctk.CTkLabel(self, text="""please run tor.exe --SocksPort 127.0.0.1:9050 --ControlPort 9051
                                    
        """)
        self.proclab.pack(pady=10)

        self.instruc = ctk.CTkLabel(self, text="more instructions at my github repo :3")
        threading.Thread(target=self.rotate_loop, daemon=True).start()

        self.update_ip()

    def rotate_loop(self):
        while True:
            time.sleep(10)
            reconnecter()

    def update_ip(self):
        try:
            ip = tor_ip()
            self.label.configure(text=f"Tor IP:\n{ip}")
        except Exception as e:
            self.label.configure(text=f"Error:\n{e}")

        self.after(5000, self.update_ip)

if __name__ == "__main__":
    App().mainloop()
