import ast
import uuid
from http.client import HTTPConnection, BadStatusLine

HOST = "localhost"
PORT1 = 8000
PORT2 = 8001


class Client:
    def __init__(self, host, port1, port2):
        self.host = host
        self.port1 = port1
        self.port2 = port2
        self.uuid = str(uuid.uuid4())

    def request_unique(self):
        conn = HTTPConnection(self.host, self.port1)
        data = {"uuid": self.uuid}

        conn.request("POST", "/", body=str(data).encode("utf-8"))

        res = None
        try:
            res = conn.getresponse()
            res = res.read().decode("utf-8")
        except BadStatusLine as response:  # Version number exception HTTP/1.1
            res = ast.literal_eval(response.line)

        if res["success"]:
            self.unique = res["unique"]
            print("[*] Request to server for unique successfull")
        else:
            print(res["error"])

    def send_text(self, text):
        conn = HTTPConnection(self.host, self.port2)
        data = {"uuid": self.uuid, "unique": self.unique, "text": str(text)}

        conn.request("POST", "/", body=str(data).encode("utf-8"))

        res = None
        try:
            res = conn.getresponse()
            res = res.read().decode("utf-8")
        except BadStatusLine as response:  # Version number exception HTTP/1.1
            res = ast.literal_eval(response.line)

        if res["success"]:
            print("[*] Successfully stored text in log file")
        else:
            print(res["error"])


if __name__ == "__main__":
    clients = []
    for i in range(50):
        clients.append(Client(HOST, PORT1, PORT2))

    for i in range(50):
        clients[i].request_unique()
        clients[i].send_text(f"Text insertion for index {i}")
