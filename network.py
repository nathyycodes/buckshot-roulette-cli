import socket
import json

class Network:
    def __init__(self, server_ip=None, port=5050, host=False):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if host:
            # Host mode
            self.sock.bind(("0.0.0.0", port))
            self.sock.listen()
            print(f"[HOST] Waiting for player on port {port}...")
            self.conn, self.addr = self.sock.accept()
            print(f"[CONNECTED] Player joined from {self.addr}")
        else:
            # Client mode
            self.sock.connect((server_ip, port))
            self.conn = self.sock

    def send(self, data: dict):
        message = json.dumps(data).encode()
        self.conn.send(message)

    def receive(self):
        data = self.conn.recv(2048).decode()
        return json.loads(data)
