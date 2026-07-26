import argparse
import socket
import sys
import threading
from typing import Optional


class WifiTextingApp:
    def __init__(self) -> None:
        self.host = "0.0.0.0"
        self.port = 5005
        self.sock: Optional[socket.socket] = None
        self.connected = False

    def show_menu(self) -> None:
        print("\n=== Wi-Fi Console Texting App ===")
        print("1. Start chat server")
        print("2. Join chat server")
        print("3. Exit")

    def get_local_ip(self) -> str:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as probe:
                probe.connect(("8.8.8.8", 80))
                return probe.getsockname()[0]
        except OSError:
            return "127.0.0.1"

    def start_server(self) -> None:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(1)

        print(f"Server listening on {self.get_local_ip()}:{self.port}")
        print("Waiting for another device to connect...")

        conn, addr = server.accept()
        self.sock = conn
        self.connected = True
        print(f"Connected to {addr[0]}:{addr[1]}")
        self._start_receiver()
        self.chat_loop()
        server.close()

    def connect_to_server(self, host: str) -> None:
        try:
            self.sock = socket.create_connection((host, self.port), timeout=5)
        except OSError as exc:
            print(f"Unable to connect to {host}:{self.port}: {exc}")
            return

        self.connected = True
        print(f"Connected to {host}:{self.port}")
        self._start_receiver()
        self.chat_loop()

    def _start_receiver(self) -> None:
        receiver = threading.Thread(target=self.receive_messages, daemon=True)
        receiver.start()

    def receive_messages(self) -> None:
        while self.connected and self.sock is not None:
            try:
                data = self.sock.recv(4096)
            except OSError:
                break

            if not data:
                break

            message = data.decode("utf-8").rstrip("\n")
            if message:
                print(f"\nPeer: {message}")
                print("You: ", end="", flush=True)

        self.connected = False
        print("\nConnection closed.")

    def chat_loop(self) -> None:
        print("Type a message and press Enter. Type /quit to leave.")
        while self.connected and self.sock is not None:
            try:
                message = input("You: ").strip()
            except EOFError:
                break

            if not message:
                continue

            if message.lower() == "/quit":
                self.send_message("/quit")
                break

            self.send_message(message)

        self.close_connection()

    def send_message(self, message: str) -> None:
        if self.sock is None:
            return

        try:
            self.sock.sendall(message.encode("utf-8") + b"\n")
        except OSError:
            self.connected = False

    def close_connection(self) -> None:
        if self.sock is not None:
            try:
                self.sock.shutdown(socket.SHUT_WR)
            except OSError:
                pass
            self.sock.close()
        self.sock = None
        self.connected = False

    def run(self) -> None:
        print("Welcome to your Wi-Fi console texting app!")
        while True:
            self.show_menu()
            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.start_server()
            elif choice == "2":
                host = input("Enter the host IP to connect to: ").strip() or "127.0.0.1"
                self.connect_to_server(host)
            elif choice == "3":
                print("Goodbye!")
                break
            else:
                print("Please choose a valid option.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple Wi-Fi console texting app")
    parser.add_argument("--server", action="store_true", help="start the chat server")
    parser.add_argument("--client", metavar="HOST", help="connect to a chat server")
    args = parser.parse_args()

    app = WifiTextingApp()
    if args.server:
        app.start_server()
    elif args.client:
        app.connect_to_server(args.client)
    else:
        app.run()
