import argparse
import socket
import threading
from typing import Optional


class RelayTextingApp:
    def __init__(self) -> None:
        self.sock: Optional[socket.socket] = None
        self.connected = False
        self.host = "0.0.0.0"
        self.port = 9000

    def show_menu(self) -> None:
        print("\n=== Cross-Network Console Chat ===")
        print("1. Start relay server")
        print("2. Connect to relay server")
        print("3. Exit")

    def get_public_ip(self) -> str:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as probe:
                probe.connect(("8.8.8.8", 80))
                return probe.getsockname()[0]
        except OSError:
            return "127.0.0.1"

    def start_relay_server(self) -> None:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(2)

        print(f"Relay server listening on {self.get_public_ip()}:{self.port}")
        print("Waiting for two clients to connect...")

        client_a, addr_a = server.accept()
        client_b, addr_b = server.accept()
        print(f"Connected clients: {addr_a[0]} and {addr_b[0]}")

        self._bridge_clients(client_a, client_b)
        server.close()

    def _bridge_clients(self, client_a: socket.socket, client_b: socket.socket) -> None:
        def forward(source: socket.socket, destination: socket.socket) -> None:
            while True:
                try:
                    data = source.recv(4096)
                except OSError:
                    break

                if not data:
                    break

                message = data.decode("utf-8").rstrip("\n")
                if not message:
                    continue

                if message == "/quit":
                    try:
                        destination.sendall(b"/quit\n")
                    except OSError:
                        pass
                    break

                print(f"\nPeer: {message}")
                print("You: ", end="", flush=True)
                try:
                    destination.sendall(data)
                except OSError:
                    break

            try:
                source.close()
            except OSError:
                pass
            try:
                destination.close()
            except OSError:
                pass

        thread_a = threading.Thread(target=forward, args=(client_a, client_b), daemon=True)
        thread_b = threading.Thread(target=forward, args=(client_b, client_a), daemon=True)
        thread_a.start()
        thread_b.start()
        thread_a.join()
        thread_b.join()

    def connect_to_relay(self, host: str) -> None:
        try:
            self.sock = socket.create_connection((host, self.port), timeout=10)
        except OSError as exc:
            print(f"Unable to connect to {host}:{self.port}: {exc}")
            return

        self.connected = True
        print(f"Connected to relay at {host}:{self.port}")
        self._chat_loop(self.sock)

    def _chat_loop(self, conn: socket.socket) -> None:
        print("Type a message and press Enter. Type /quit to leave.")
        while self.connected:
            try:
                message = input("You: ").strip()
            except EOFError:
                break

            if not message:
                continue

            if message.lower() == "/quit":
                try:
                    conn.sendall(b"/quit\n")
                except OSError:
                    pass
                break

            try:
                conn.sendall(message.encode("utf-8") + b"\n")
            except OSError:
                break

        self.close_connection(conn)

    def close_connection(self, conn: Optional[socket.socket] = None) -> None:
        target = conn if conn is not None else self.sock
        if target is not None:
            try:
                target.shutdown(socket.SHUT_WR)
            except OSError:
                pass
            try:
                target.close()
            except OSError:
                pass
        if conn is None:
            self.sock = None
        self.connected = False

    def run(self) -> None:
        print("Welcome to your cross-network console chat app!")
        while True:
            self.show_menu()
            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.start_relay_server()
            elif choice == "2":
                host = input("Enter the relay host IP or domain: ").strip() or "127.0.0.1"
                self.connect_to_relay(host)
            elif choice == "3":
                print("Goodbye!")
                break
            else:
                print("Please choose a valid option.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Console chat app that works across different Wi-Fi networks")
    parser.add_argument("--relay-server", action="store_true", help="start a relay server for two clients")
    parser.add_argument("--relay-client", metavar="HOST", help="connect to a relay server")
    parser.add_argument("--port", type=int, default=9000, help="relay port to use")
    args = parser.parse_args()

    app = RelayTextingApp()
    app.port = args.port
    if args.relay_server:
        app.start_relay_server()
    elif args.relay_client:
        app.connect_to_relay(args.relay_client)
    else:
        app.run()
