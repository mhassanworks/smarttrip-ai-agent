from __future__ import annotations
import json
import socket
import threading

class AgentTCPServer:
    def __init__(self, host="127.0.0.1", port=8765, security=None):
        self.host = host
        self.port = port
        self.security = security
        self.running = False
        self.server = None
        self.thread = None
        self.log = []

    def start(self):
        if self.running:
            return
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        self.server.settimeout(0.5)
        self.running = True
        self.thread = threading.Thread(target=self._serve, daemon=True, name="agent-tcp-server")
        self.thread.start()

    def stop(self):
        self.running = False
        if self.server:
            self.server.close()

    def _serve(self):
        while self.running:
            try:
                conn, _ = self.server.accept()
            except (socket.timeout, OSError):
                continue
            with conn:
                conn.settimeout(3)
                data = b""
                while True:
                    chunk = conn.recv(4096)
                    if not chunk:
                        break
                    data += chunk
                    if b"\n" in data:
                        break
                try:
                    envelope = json.loads(data.decode("utf-8").strip())
                    valid = self.security.verify(envelope) if self.security else True
                    if valid:
                        payload = envelope["payload"] if isinstance(envelope, dict) and "payload" in envelope else envelope
                        response = {"accepted": True, "agent": "Agent B",
                                    "message": f"Received negotiation proposal for {payload.get('destination', 'trip')}"}
                        self.log.append({"direction": "A -> B", "status": "Accepted",
                                         "payload": payload, "response": response})
                    else:
                        response = {"accepted": False, "error": "Unauthorized or tampered message"}
                        self.log.append({"direction": "A -> B", "status": "Rejected",
                                         "payload": envelope, "response": response})
                except (json.JSONDecodeError, UnicodeDecodeError):
                    response = {"accepted": False, "error": "Invalid JSON"}
                    self.log.append({"direction": "A -> B", "status": "Rejected",
                                     "payload": None, "response": response})
                conn.sendall((json.dumps(response) + "\n").encode("utf-8"))

def send_signed_message(host, port, envelope):
    with socket.create_connection((host, port), timeout=3) as sock:
        sock.sendall((json.dumps(envelope) + "\n").encode("utf-8"))
        response = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response += chunk
            if b"\n" in response:
                break
    return json.loads(response.decode("utf-8").strip())
